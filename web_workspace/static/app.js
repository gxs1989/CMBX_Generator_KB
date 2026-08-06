const state = {
  health: null, artifacts: [], library:{cmbx_source:[],method_md:[],report_md:[],active:"cmbx_source"}, jobs: [], activeView: "home", activeBranch: "", poll: null,
  foq: {config:null, scope:null, artifactIds:new Set(), sequenceKeys:new Set(), injections:{}, metrics:[], selectedMetrics:new Set(), result:null, results:[]},
  method: {config:null, modules:new Set(), package:null, mdArtifact:null, preflight:null, generationJob:null, route:"gpt", aiSettings:null},
  auth: null, adminAccounts: [], adminPermissions: [],
  analysis: {
    raw:{artifactIds:new Set(),catalog:null,selected:new Set(),filters:{package:"",sequence:"",injection:"",channel:""},step:1},
    chrom:{artifactIds:new Set(),catalog:null,selected:new Set(),filters:{package:"",sequence:"",injection:"",channel:""},step:1,plot:null,viewStack:[]},
    formula:{artifactIds:new Set(),catalog:null,formulas:[],selected:new Set(),injections:new Set(),results:[]}
  },
  report:{config:null,modules:new Set(),package:null,artifact:null,preflight:null,methodBases:new Map(),methods:[],step:1},
  sequence:{config:null,methods:[],reports:[],selectedMethods:new Map(),report:null,rows:[],preflight:null,step:1},
  quality:{config:null,catalog:null,result:null},
  single:{artifactIds:new Set(),catalog:null,traceKeys:new Set(),benchmarkKeys:new Set(),result:null,step:1,feature:""}
};

const api = async (url, options = {}) => {
  const timeoutMs = Number(options.timeoutMs || 15000);
  const requestOptions = {...options}; delete requestOptions.timeoutMs;
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);
  if (!requestOptions.signal) requestOptions.signal = controller.signal;
  let response;
  try { response = await fetch(url, requestOptions); }
  catch (error) {
    if (error.name === "AbortError") throw new Error("The service did not respond in time. Refresh the page or contact the administrator.");
    throw error;
  } finally { clearTimeout(timeout); }
  if (!response.ok) {
    let message = `${response.status} ${response.statusText}`;
    try { message = (await response.json()).detail || message; } catch (_) {}
    if (response.status === 401 && !url.startsWith("/api/auth/")) showLogin(message);
    throw new Error(message);
  }
  return response.status === 204 ? null : response.json();
};

const escapeHtml = (value) => String(value ?? "").replace(/[&<>'"]/g, ch => ({"&":"&amp;","<":"&lt;",">":"&gt;","'":"&#39;",'"':"&quot;"}[ch]));
const formatBytes = (value) => value >= 1024 * 1024 ? `${(value / 1024 / 1024).toFixed(1)} MB` : `${Math.max(0, value / 1024).toFixed(1)} KB`;
const toast = (message) => { const el = document.querySelector("#toast"); el.textContent = message; el.classList.add("show"); setTimeout(() => el.classList.remove("show"), 3400); };

function showLogin(message = "Sign in to continue.") {
  document.querySelector("#loginGate").hidden = false;
  document.querySelector("#loginStatus").textContent = message;
}

async function finishLogin(result) {
  const previousUser = state.auth?.user?.user || state.auth?.user_id || "";
  const nextUser = result.user?.user || result.user_id || "";
  if (previousUser !== nextUser) resetUserScopedState();
  state.auth = result;
  document.querySelector("#loginGate").hidden = true;
  document.querySelector("#identity").textContent = `${result.user?.user || result.user_id || "Signed in"} · ${result.user?.role || result.role || "analyst"}`;
  document.querySelector("#healthText").textContent = "Loading workspace";
  applyAccessPolicy();
  Promise.allSettled([refreshHealth(), refreshFileLibrary(), refreshJobs()]);
  if (!state.poll) state.poll = setInterval(() => { refreshJobs(); if (state.activeView === "admin") refreshAdmin(); }, 2500);
}

function resetUserScopedState() {
  state.artifacts = [];
  state.library = {cmbx_source:[],method_md:[],report_md:[],active:"cmbx_source"};
  state.method = {config:null,modules:new Set(),package:null,mdArtifact:null,preflight:null,generationJob:null,route:"gpt",aiSettings:null};
  state.report = {config:null,modules:new Set(),package:null,artifact:null,preflight:null,methodBases:new Map(),methods:[],step:1};
  state.sequence = {config:null,methods:[],reports:[],selectedMethods:new Map(),report:null,rows:[],preflight:null,step:1};
  state.foq = {config:null,scope:null,artifactIds:new Set(),sequenceKeys:new Set(),injections:{},metrics:[],selectedMetrics:new Set(),result:null,results:[]};
  state.analysis.raw = {artifactIds:new Set(),catalog:null,selected:new Set(),filters:{package:"",sequence:"",injection:"",channel:""},step:1};
  state.analysis.chrom = {artifactIds:new Set(),catalog:null,selected:new Set(),filters:{package:"",sequence:"",injection:"",channel:""},step:1,plot:null,viewStack:[]};
  state.analysis.formula = {artifactIds:new Set(),catalog:null,formulas:[],selected:new Set(),injections:new Set(),results:[]};
  state.quality = {config:null,catalog:null,result:null};
  state.single = {artifactIds:new Set(),catalog:null,traceKeys:new Set(),benchmarkKeys:new Set(),result:null,step:1,feature:""};
}

function applyAccessPolicy() {
  const identity=state.auth?.user||state.auth||{}, permissions=new Set(identity.permissions||[]);
  const admin=identity.role==="admin"||permissions.has("*"), allowed=(...items)=>admin||items.some(item=>permissions.has(item));
  const viewRules={
    method:allowed("instrument_method_generation","method_generate","method_manual_web_ai","method_deepseek"),
    report:allowed("report_generate"), sequence:allowed("sequence_generate"), raw:allowed("raw_export"),
    chrom:allowed("chromatogram_plot"), formula:allowed("direct_cm_formula"),
    foq:allowed("foq_check"), quality:allowed("database_read"), single:allowed("single_verification","leak_sensor_analysis"), admin,
  };
  Object.entries(viewRules).forEach(([view,visible])=>document.querySelectorAll(`[data-view="${view}"]`).forEach(item=>item.hidden=!visible));
  const moduleAliases={instrument_method_generation:["instrument_method_generation","method_generate","method_manual_web_ai","method_deepseek"]};
  document.querySelectorAll("[data-module-permission]").forEach(item=>{
    const required=moduleAliases[item.dataset.modulePermission]||[item.dataset.modulePermission];
    item.hidden=!allowed(...required);
  });
  const integrate=document.querySelector("#integrateChrom");if(integrate)integrate.hidden=!allowed("chromatogram_integrate");
}

async function initializeAuthentication() {
  showLogin("Enter your authorized account and password.");
  try {
    const options = await api("/api/auth/options", {timeoutMs:5000});
    state.auth = options;
    if (options.authenticated) return finishLogin(options);
    showLogin("Use an account created and enabled by the administrator.");
  } catch (error) { showLogin(error.message); }
}

async function windowsLogin() {
  try { await finishLogin(await api("/api/auth/windows-login", {method:"POST"})); }
  catch (error) { showLogin(error.message); }
}

async function developerLogin() {
  const email = document.querySelector("#developerEmail").value.trim();
  const password = document.querySelector("#developerPassword").value;
  try {
    await finishLogin(await api("/api/auth/developer-login", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({email,password})}));
    document.querySelector("#developerPassword").value = "";
  } catch (error) { showLogin(error.message); }
}

async function logout() {
  await api("/api/auth/logout", {method:"POST"});
  if (state.poll) clearInterval(state.poll); state.poll = null; state.health = null; state.auth = null; resetUserScopedState();
  showView("home"); showLogin("Signed out.");
}

function showView(name) {
  state.activeView = name;
  state.activeBranch = "";
  document.querySelectorAll(".view").forEach(el => el.classList.toggle("active", el.id === `view-${name}`));
  document.querySelectorAll(".nav-item").forEach(el => el.classList.toggle("active", el.dataset.view === name));
  document.querySelector(".map-branches")?.classList.remove("has-focus");
  document.querySelectorAll("[data-map-branch]").forEach(el => el.classList.remove("focused"));
  const labels = {home:"Home",method:"Instrument Method Generation",report:"Report Template Generation",sequence:"Sequence Generation",raw:"Batch Raw Data Export",chrom:"Chromatograms & Integration",formula:"Direct CM Formula Results",quality:"Quality Data & Database",workspace:"CMBX Workspace",foq:"FOQ Quick Check",single:"Single Verification",jobs:"Job Center",admin:"Admin Console"};
  document.querySelector("#breadcrumb").textContent = `Workspace / ${labels[name]}`;
  if (name === "workspace") refreshArtifacts();
  if (name === "home") refreshFileLibrary();
  if (name === "method") refreshMethodConfig();
  if (name === "foq") { refreshFoqArtifacts(); refreshFoqConfig(); }
  if (["raw","chrom","formula"].includes(name)) renderAnalysisSources(name);
  if (name === "report") refreshReportConfig();
  if (name === "sequence") refreshSequenceConfig();
  if (name === "quality") refreshQualityConfig();
  if (name === "single") closeLeakSensorAnalysis();
  if (name === "jobs") refreshJobs();
  if (name === "admin") refreshAdmin();
}

function methodLog(message) {
  const log = document.querySelector("#methodLog");
  const stamp = new Date().toLocaleTimeString();
  log.textContent = `[${stamp}] ${message}\n${log.textContent === "Ready." ? "" : log.textContent}`.trim();
}

function setMethodStep(step, message = "") {
  document.querySelectorAll("[data-method-step]").forEach(item => {
    const value = Number(item.dataset.methodStep);
    item.classList.toggle("active", value === step);
    item.classList.toggle("complete", value < step);
  });
  document.querySelectorAll("[data-method-panel]").forEach(item => item.classList.toggle("active", Number(item.dataset.methodPanel) === step));
  if (message) document.querySelector("#methodMessage").textContent = message;
}

async function refreshMethodConfig() {
  try {
    state.method.config = await api("/api/method/config");
    state.method.aiSettings = await api("/api/account/ai-settings");
    const routes = state.method.config.allowed_routes || {};
    if (!routes[state.method.route]) state.method.route = ["gpt","manual","deepseek"].find(route => routes[route]) || "gpt";
    document.querySelectorAll('input[name="methodRoute"]').forEach(input => {
      input.closest(".route-option").hidden = !routes[input.value];
      input.checked = input.value === state.method.route;
    });
    if (!state.method.modules.size && state.method.config.modules.includes("TCC")) state.method.modules.add("TCC");
    renderMethodModules();
    renderMethodRoute();
  } catch (error) { toast(error.message); }
}

function selectedProviderSetting(provider = state.method.route) {
  return (state.method.aiSettings?.providers || []).find(item => item.provider === provider);
}

function renderMethodRoute() {
  const automatic = state.method.route !== "manual";
  document.querySelectorAll(".manual-method-only").forEach(el => el.hidden = automatic);
  document.querySelector("#methodApiPanel").hidden = !automatic;
  document.querySelector("#automaticMethodActions").hidden = !automatic;
  document.querySelectorAll(".route-option").forEach(el => el.classList.toggle("active", el.querySelector("input")?.value === state.method.route));
  const allowedCount = Object.values(state.method.config?.allowed_routes || {}).filter(Boolean).length;
  document.querySelector("#methodRoutePicker").hidden = allowedCount <= 1;
  if (!automatic) {
    document.querySelector("#methodPackageStatus").textContent = "Build an evidence ZIP, use the web model, then import its Method MD.";
    return;
  }
  const setting = selectedProviderSetting();
  const quota = state.method.aiSettings?.quota || state.method.config?.quota || {};
  document.querySelector("#methodQuotaSummary").innerHTML = `<b>${escapeHtml(quota.remaining ?? 0)} of ${escapeHtml(quota.limit ?? 3)} automatic run(s) remaining today</b><span>${escapeHtml(quota.used ?? 0)} used${quota.granted_uses ? ` · ${escapeHtml(quota.granted_uses)} approved extra` : ""}${quota.pending_requests ? " · request pending" : ""}</span>`;
  document.querySelector("#methodApiSettingSummary").textContent = setting ? `${setting.label} · ${setting.model} · ${setting.api_key_configured ? "API key configured" : "API key required"}` : "Provider setting unavailable";
  document.querySelector("#methodPackageStatus").textContent = setting?.api_key_configured ? "Automatic generation is ready." : `Configure your ${setting?.label || state.method.route} API key before generation.`;
  document.querySelector("#autoGenerateMethod").disabled = !setting?.api_key_configured || Number(quota.remaining || 0) < 1;
  document.querySelector("#requestMethodQuota").disabled = Number(quota.pending_requests || 0) > 0;
}

function openAiSettings() {
  const provider = state.method.route === "manual" ? "gpt" : state.method.route;
  const setting = selectedProviderSetting(provider) || state.method.config?.providers?.[provider] || {};
  document.querySelector("#aiSettingsProvider").value = provider;
  document.querySelector("#aiSettingsBaseUrl").value = setting.base_url || "";
  document.querySelector("#aiSettingsModel").value = setting.model || "";
  document.querySelector("#aiSettingsApiKey").value = "";
  document.querySelector("#clearAiSettingsKey").checked = false;
  document.querySelector("#aiSettingsStatus").textContent = setting.api_key_configured ? "A key is saved." : "No key is saved.";
  document.querySelector("#aiSettingsDialog").showModal();
}

function syncAiSettingsProvider() {
  const provider = document.querySelector("#aiSettingsProvider").value;
  const setting = selectedProviderSetting(provider) || state.method.config?.providers?.[provider] || {};
  document.querySelector("#aiSettingsBaseUrl").value = setting.base_url || "";
  document.querySelector("#aiSettingsModel").value = setting.model || "";
  document.querySelector("#aiSettingsApiKey").value = "";
  document.querySelector("#clearAiSettingsKey").checked = false;
  document.querySelector("#aiSettingsStatus").textContent = setting.api_key_configured ? "A key is saved." : "No key is saved.";
}

async function saveAiSettings() {
  const provider = document.querySelector("#aiSettingsProvider").value;
  const button = document.querySelector("#saveAiSettings"); button.disabled = true;
  try {
    await api(`/api/account/ai-settings/${provider}`, {method:"PUT", headers:{"Content-Type":"application/json"}, body:JSON.stringify({
      base_url:document.querySelector("#aiSettingsBaseUrl").value,
      model:document.querySelector("#aiSettingsModel").value,
      api_key:document.querySelector("#aiSettingsApiKey").value,
      clear_api_key:document.querySelector("#clearAiSettingsKey").checked
    })});
    state.method.aiSettings = await api("/api/account/ai-settings");
    document.querySelector("#aiSettingsDialog").close(); renderMethodRoute(); toast("Personal AI settings saved.");
  } catch (error) { document.querySelector("#aiSettingsStatus").textContent = error.message; }
  finally { button.disabled = false; }
}

async function requestMethodQuota() {
  const requested = Number(prompt("How many additional automatic runs do you need today?", "3"));
  if (!Number.isFinite(requested) || requested < 1) return;
  const reason = prompt("Reason for the request:", "Additional method design work") || "";
  try {
    await api("/api/account/access-requests", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({requested_uses:requested, reason})});
    state.method.aiSettings = await api("/api/account/ai-settings"); renderMethodRoute(); toast("Request sent to the administrator.");
  } catch (error) { toast(error.message); }
}

async function autoGenerateMethod() {
  const request = document.querySelector("#methodIntent").value.trim();
  if (!state.method.modules.size) { toast("Choose at least one module."); return; }
  if (!request) { toast("Describe the test requirement first."); return; }
  const button = document.querySelector("#autoGenerateMethod"); button.disabled = true;
  document.querySelector("#autoMethodProgressBar").style.width = "3%";
  document.querySelector("#autoMethodRunStatus").textContent = "Queuing automatic generation...";
  document.querySelector("#autoMethodGenerationResult").innerHTML = "";
  methodLog(`${state.method.route.toUpperCase()} automatic generation queued.`);
  try {
    const job = await api("/api/method/auto-generate", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({
      provider:state.method.route, modules:[...state.method.modules], request,
      small_context:document.querySelector("#methodSmallContext").checked,
      asset_name:document.querySelector("#autoMethodAssetName").value || "AI Instrument Method",
      target_cm_version:document.querySelector("#autoMethodTargetVersion").value,
      md_only:true
    })});
    state.method.generationJob = job.id;
    while (true) {
      await new Promise(resolve => setTimeout(resolve, 700));
      const current = await api(`/api/jobs/${job.id}`);
      const percent = Math.round(100 * current.progress_current / Math.max(1, current.progress_total));
      document.querySelector("#autoMethodProgressBar").style.width = `${percent}%`;
      document.querySelector("#autoMethodRunStatus").textContent = current.message || current.stage;
      if (current.status === "completed") {
        const result = current.result || {};
        renderMethodPreflight({artifact:result.method_md_artifact, preflight:result.preflight});
        document.querySelector("#methodTargetVersion").value = document.querySelector("#autoMethodTargetVersion").value;
        const mdLink = document.querySelector("#autoMethodMdOnly").checked ? `<a class="secondary-button" href="${escapeHtml(result.method_md_download_url)}">Download Method MD</a>` : "";
        const links = `${mdLink}<button class="secondary-button" type="button" data-continue-method-report>Continue to Report</button>`;
        document.querySelector("#autoMethodGenerationResult").innerHTML = `<div class="generation-success"><strong>Method MD preview is ready.</strong><span>Review structural warnings before compiling CMBX.</span>${links}</div>`;
        document.querySelector("#methodGenerationResult").innerHTML = "";
        if(result.method_md_artifact)state.report.methodBases.set(result.method_md_artifact.id,result.method_md_artifact);
        document.querySelectorAll("[data-continue-method-report]").forEach(button => button.addEventListener("click", continueMethodToReport));
        setMethodStep(4, "Step 4: review every highlighted Method MD row, then compile the candidate CMBX.");
        methodLog("Automatic Method MD generation completed; CMBX compilation is awaiting review.");
        refreshFileLibrary();
        break;
      }
      if (current.status === "failed") throw new Error(current.error || current.message || "Automatic generation failed");
    }
  } catch (error) { toast(error.message); document.querySelector("#autoMethodRunStatus").textContent = error.message; methodLog(`Automatic generation failed: ${error.message}`); }
  finally { state.method.aiSettings = await api("/api/account/ai-settings").catch(() => state.method.aiSettings); renderMethodRoute(); refreshJobs(); }
}

function renderMethodModules() {
  const list = document.querySelector("#methodModuleList");
  const modules = state.method.config?.modules || [];
  list.innerHTML = modules.length ? modules.map(module => `<label class="module-option"><input type="checkbox" data-method-module="${escapeHtml(module)}" ${state.method.modules.has(module) ? "checked" : ""}><span>${escapeHtml(module)}</span></label>`).join("") : '<div class="empty-block">No online Method KB module is available.</div>';
  document.querySelector("#methodPackageSummary").innerHTML = state.method.modules.size
    ? `<strong>${state.method.modules.size} module(s) selected</strong><span>Each module contributes one SPEC, original-script collection, and interpreted summary.</span>`
    : '<div class="empty-block">Choose at least one module.</div>';
}

async function buildMethodPackage() {
  const button = document.querySelector("#buildMethodPackage");
  button.disabled = true;
  document.querySelector("#methodPackageStatus").textContent = "Building package...";
  methodLog("Preparing Method SPEC and KB package.");
  try {
    const result = await api("/api/method/ai-package", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({
      modules:[...state.method.modules], request:document.querySelector("#methodIntent").value,
      small_context:document.querySelector("#methodSmallContext").checked,
      optimize:document.querySelector("#methodOptimizePrompt").checked
    })});
    state.method.package = result;
    const link = document.querySelector("#downloadMethodPackage");
    link.href = result.download_url; link.classList.remove("disabled-link");
    document.querySelector("#methodPackageStatus").textContent = `${result.files.length} KB file(s) packaged. ${result.prompt_detail}`;
    document.querySelector("#methodPackageSummary").innerHTML = `<strong>Package ready</strong><span>${result.files.map(escapeHtml).join(" · ")}</span><details><summary>Review packaged prompt</summary><pre>${escapeHtml(result.prompt)}</pre></details>`;
    methodLog(`AI package ready with ${result.files.length} KB file(s).`);
  } catch (error) { toast(error.message); document.querySelector("#methodPackageStatus").textContent = error.message; methodLog(`Package failed: ${error.message}`); }
  finally { button.disabled = false; }
}

function renderMethodPreflight(payload) {
  const preflight = payload.preflight; state.method.preflight = preflight; state.method.mdArtifact = payload.artifact;
  const issueRows = new Map((preflight.issues || []).map(item => [String(item.row), item.severity]));
  document.querySelector("#methodPreviewRows").innerHTML = preflight.rows.length ? preflight.rows.map(row => {
    const kind = String(row.Kind || "Command"); const number = String(row["#"] ?? ""); const issue = issueRows.get(number) || "";
    return `<tr class="method-row kind-${escapeHtml(kind.toLowerCase())} ${issue ? `issue-${escapeHtml(issue)}` : ""}"><td>${escapeHtml(number)}</td><td>${escapeHtml(kind)}</td><td>${escapeHtml(row.Time)}</td><td>${escapeHtml(row.Command)}</td><td>${escapeHtml(row.Value)}</td><td>${escapeHtml(row.Comment)}</td></tr>`;
  }).join("") : '<tr><td colspan="6" class="empty">No method rows could be parsed.</td></tr>';
  const issues = preflight.issues || [];
  document.querySelector("#methodIssues").innerHTML = issues.length ? issues.map(item => `<div class="lint-item ${escapeHtml(item.severity)}"><b>${escapeHtml(item.severity.toUpperCase())} ${escapeHtml(item.code)}</b><span>Row ${escapeHtml(item.row)} · ${escapeHtml(item.message)}</span></div>`).join("") : '<div class="lint-ok">No structural issue detected.</div>';
  const errors = issues.filter(item => item.severity === "error").length || preflight.errors.length;
  const warnings = issues.filter(item => item.severity !== "error").length || preflight.warnings.length;
  document.querySelector("#methodPreflightStatus").textContent = preflight.ready ? `Ready to generate · ${warnings} warning(s).` : `Generation blocked · ${errors} error(s). Regenerate the MD or contact xiaoshu.guan@thermofisher.com.`;
  document.querySelector("#methodPreviewFooter").textContent = `${preflight.rows.length} row(s) · ${errors} error(s) · ${warnings} warning(s)`;
  document.querySelector("#generateMethod").disabled = !preflight.ready;
  document.querySelector("#methodAssetName").value = payload.artifact.original_name.replace(/\.(md|markdown)$/i, "");
  document.querySelector("#methodConfiguration").innerHTML = (preflight.configuration || []).map(item => `<div>${escapeHtml(item)}</div>`).join("");
  methodLog(`Preflight finished: ${preflight.rows.length} row(s), ${errors} error(s), ${warnings} warning(s).`);
}

async function uploadMethodMd(file) {
  const form = new FormData(); form.append("file", file);
  document.querySelector("#methodPreflightStatus").textContent = `Uploading and checking ${file.name}...`;
  methodLog(`Preflight started: ${file.name}`);
  try { renderMethodPreflight(await api("/api/artifacts/md-upload?kind=method_md", {method:"POST", body:form})); setMethodStep(4, "Step 4: review the imported Method MD, then compile the candidate CMBX."); refreshFileLibrary(); }
  catch (error) { toast(error.message); document.querySelector("#methodPreflightStatus").textContent = error.message; methodLog(`Preflight failed: ${error.message}`); }
}

async function generateMethod() {
  if (!state.method.mdArtifact || !state.method.preflight?.ready) { toast("Import a Method MD that passes preflight first."); return; }
  const button = document.querySelector("#generateMethod"); button.disabled = true;
  document.querySelector("#methodProgressBar").style.width = "4%"; document.querySelector("#methodRunStatus").textContent = "Queuing generation...";
  methodLog("Instrument method generation queued.");
  try {
    const job = await api("/api/method/generate", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({
      artifact_id:state.method.mdArtifact.id, asset_name:document.querySelector("#methodAssetName").value,
      target_cm_version:document.querySelector("#methodTargetVersion").value,
      family:[...state.method.modules].join(" + "), intent:document.querySelector("#methodIntent").value
    })});
    state.method.generationJob = job.id;
    while (true) {
      await new Promise(resolve => setTimeout(resolve, 600));
      const current = await api(`/api/jobs/${job.id}`);
      const percent = Math.round(100 * current.progress_current / Math.max(1, current.progress_total));
      document.querySelector("#methodProgressBar").style.width = `${percent}%`;
      document.querySelector("#methodRunStatus").textContent = current.message || current.stage;
      if (current.status === "completed") {
        const result = current.result || {};
        document.querySelector("#methodGenerationResult").innerHTML = `<div class="generation-success"><strong>${escapeHtml(result.project_name || "Instrument method")} is ready.</strong><span>Candidate CMBX compiled and stored with its source MD and manifest.</span><a class="primary-button" href="${escapeHtml(result.download_url)}">Download CMBX</a></div>`;
        methodLog("Generation completed and CMBX registered."); break;
      }
      if (current.status === "failed") throw new Error(current.error || current.message || "Generation failed");
    }
  } catch (error) { toast(error.message); document.querySelector("#methodRunStatus").textContent = error.message; methodLog(`Generation failed: ${error.message}`); }
  finally { button.disabled = false; refreshJobs(); }
}

function showBranch(branch) {
  showView("home");
  state.activeBranch = branch;
  const labels = {design:"Design & Generate",results:"Chromatograms & Results",quality:"Quality Control & Database"};
  document.querySelectorAll(".nav-item").forEach(el => el.classList.toggle("active", el.dataset.branch === branch));
  const branches = document.querySelector(".map-branches");
  branches?.classList.add("has-focus");
  document.querySelectorAll("[data-map-branch]").forEach(el => el.classList.toggle("focused", el.dataset.mapBranch === branch));
  document.querySelector("#breadcrumb").textContent = `Workspace / ${labels[branch]}`;
  document.querySelector(`[data-map-branch="${branch}"]`)?.scrollIntoView({behavior:"smooth", block:"center"});
}

async function refreshHealth() {
  try {
    state.health = await api("/api/health");
    document.querySelector("#healthDot").classList.add("ok");
    document.querySelector("#healthText").textContent = `Service ${state.health.version}`;
    document.querySelector("#identity").textContent = `${state.health.user.user} · ${state.health.user.role}`;
    document.querySelectorAll(".admin-only").forEach(el => el.hidden = state.health.user.role !== "admin");
    const requestedView = new URLSearchParams(window.location.search).get("view");
    if (requestedView === "admin" && state.health.user.role === "admin" && state.activeView !== "admin") showView("admin");
  } catch (error) {
    document.querySelector("#healthText").textContent = "Service unavailable";
    toast(error.message);
  }
}

async function uploadFiles(files) {
  const status = document.querySelector("#uploadStatus");
  for (let index = 0; index < files.length; index += 1) {
    const file = files[index];
    status.textContent = `Uploading ${index + 1}/${files.length}: ${file.name}`;
    const form = new FormData(); form.append("file", file);
    try { await api("/api/artifacts/upload", {method:"POST", body:form}); }
    catch (error) { toast(`${file.name}: ${error.message}`); }
  }
  status.textContent = `${files.length} file(s) processed.`;
  await refreshArtifacts();
  if (state.activeView === "foq") refreshFoqArtifacts();
}

async function refreshArtifacts() {
  try {
    state.artifacts = await api("/api/artifacts?kind=cmbx_source");
    const body = document.querySelector("#artifactRows");
    if (!state.artifacts.length) { body.innerHTML = '<tr><td colspan="6" class="empty">No CMBX uploaded.</td></tr>'; return; }
    body.innerHTML = state.artifacts.map(item => `<tr>
      <td><strong>${escapeHtml(item.original_name)}</strong><br><small>${escapeHtml(item.sha256.slice(0, 12))}</small></td>
      <td>${escapeHtml(item.owner)}</td><td>${formatBytes(item.size_bytes)}</td><td>${escapeHtml(item.created_at)}</td>
      <td><span class="pill">source</span></td>
      <td><button class="row-action" data-scan="${item.id}">Scan</button><button class="row-action" data-open="${item.id}">Open</button></td>
    </tr>`).join("");
  } catch (error) { toast(error.message); }
}

async function refreshFileLibrary() {
  try {
    const kinds = ["cmbx_source", "method_md", "report_md"];
    const values = await Promise.all(kinds.map(kind => api(`/api/artifacts?kind=${kind}`)));
    kinds.forEach((kind,index) => state.library[kind] = values[index]);
    state.artifacts = state.library.cmbx_source;
    renderFileLibrary();
    if (document.querySelector("#artifactRows")) refreshArtifacts();
  } catch (error) { toast(error.message); }
}

function renderFileLibrary() {
  const kind = state.library.active;
  document.querySelectorAll("[data-library-kind]").forEach(item => item.classList.toggle("active", item.dataset.libraryKind === kind));
  const label = document.querySelector("#homeFileUploadLabel");
  const input = document.querySelector("#homeFileUpload");
  if (!label || !input) return;
  label.textContent = kind === "cmbx_source" ? "Add CMBX" : kind === "method_md" ? "Add Method MD" : "Add Report MD";
  input.accept = kind === "cmbx_source" ? ".cmbx" : ".md,.markdown";
  input.multiple = kind === "cmbx_source";
  const labels = {cmbx_source:"CMBX",method_md:"Method MD",report_md:"Report MD"};
  const rows = state.library[kind] || [];
  document.querySelector("#homeFileRows").innerHTML = rows.length ? rows.map(item => {
    let use = "";
    if (kind === "method_md") use = `<button class="row-action" data-use-method="${item.id}">Use in Method</button><button class="row-action" data-use-report-basis="${item.id}">Use for Report</button>`;
    if (kind === "report_md") use = `<button class="row-action" data-use-report="${item.id}">Review</button>`;
    return `<tr><td><strong>${escapeHtml(item.original_name)}</strong></td><td>${labels[kind]}</td><td>${formatBytes(item.size_bytes)}</td><td>${escapeHtml(item.created_at)}</td><td>${use}<a class="row-action link-action" href="/api/artifacts/${item.id}/download">Download</a><button class="row-action danger-action" data-delete-artifact="${item.id}">Delete</button></td></tr>`;
  }).join("") : `<tr><td colspan="5" class="empty">No ${labels[kind]} file in your library.</td></tr>`;
}

async function uploadHomeFiles(files) {
  const kind = state.library.active;
  const status = document.querySelector("#homeFileStatus");
  for (const file of files) {
    status.textContent = `Adding ${file.name}...`;
    const form = new FormData(); form.append("file", file);
    const url = kind === "cmbx_source" ? "/api/artifacts/upload" : `/api/artifacts/md-upload?kind=${kind}`;
    try { await api(url, {method:"POST",body:form,timeoutMs:180000}); }
    catch (error) { toast(`${file.name}: ${error.message}`); }
  }
  status.textContent = "Library updated.";
  await refreshFileLibrary();
}

async function deleteLibraryArtifact(id) {
  if (!confirm("Delete this file from your managed library?")) return;
  try { await api(`/api/artifacts/${id}`, {method:"DELETE"}); await refreshFileLibrary(); toast("File deleted."); }
  catch (error) { toast(error.message); }
}

async function useManagedMd(id, target) {
  try {
    const payload = await api(`/api/artifacts/${id}/preflight`, {method:"POST",timeoutMs:180000});
    if (target === "method") { renderMethodPreflight(payload); showView("method"); setMethodStep(4,"Step 4: review the selected Method MD, then compile CMBX."); }
    if (target === "report-basis") { state.report.methodBases.set(payload.artifact.id,payload.artifact); showView("report"); await refreshReportConfig(); setReportStep(1,"Step 1: confirm the selected Method MD collection."); }
    if (target === "report") { renderReportPreflight(payload); showView("report"); setReportStep(4,"Step 4: review the selected Report MD, then compile CMBX."); }
  } catch (error) { toast(error.message); }
}

async function scanArtifact(id) {
  try { const job = await api(`/api/cmbx/${id}/scan`, {method:"POST"}); toast(`Inventory job queued: ${job.id.slice(0, 8)}`); showView("jobs"); }
  catch (error) { toast(error.message); }
}

async function openInventory(id) {
  try {
    const inventory = await api(`/api/cmbx/${id}/inventory`);
    renderInventory(inventory); showView("workspace");
  } catch (error) { toast(error.message); }
}

function renderInventory(inventory) {
  const labels = {sequences:"Sequences",injections:"Injections",channels:"Channels",audits:"Audit trails",instrument_methods:"Instrument methods",processing_methods:"Processing methods",report_templates:"Report templates",entries:"Package entries"};
  document.querySelector("#inventorySummary").innerHTML = Object.entries(inventory.summary).map(([key,value]) => `<div class="metric"><b>${value}</b><span>${labels[key] || key}</span></div>`).join("");
  const node = item => `<li><strong>${escapeHtml(item.name || "(unnamed)")}</strong> <span class="kind">${escapeHtml(item.kind)}</span>${item.children?.length ? `<ul>${item.children.map(node).join("")}</ul>` : ""}</li>`;
  document.querySelector("#inventoryTree").innerHTML = `<ul>${inventory.tree.map(node).join("")}</ul>`;
}

async function refreshJobs() {
  try {
    state.jobs = await api("/api/jobs?limit=100");
    const body = document.querySelector("#jobRows");
    if (!state.jobs.length) { body.innerHTML = '<tr><td colspan="6" class="empty">No jobs.</td></tr>'; return; }
    body.innerHTML = state.jobs.map(job => {
      const percent = Math.round(100 * job.progress_current / Math.max(1, job.progress_total));
      return `<tr><td>${escapeHtml(job.task_type)}</td><td>${escapeHtml(job.owner)}</td><td>${escapeHtml(job.stage)}</td>
        <td><div class="progress-track"><div class="progress-bar" style="width:${percent}%"></div></div><small>${percent}%</small></td>
        <td><span class="pill ${escapeHtml(job.status)}">${escapeHtml(job.status)}</span></td><td>${escapeHtml(job.message || job.error)}</td></tr>`;
    }).join("");
  } catch (error) { toast(error.message); }
}

async function refreshAdmin() {
  try {
    const [status, access, accounts] = await Promise.all([api("/api/admin/status"), api("/api/admin/access-requests"), api("/api/admin/developer-accounts")]);
    const values = [
      ["Service", `${status.service} · v${status.version}`, `${status.active_workers}/${status.worker_limit} active workers`],
      ["Authentication", status.authentication.mode, `${status.authentication.admin_users_configured} configured admin user(s)`],
      ["Shared storage", status.storage.shared_root, `${formatBytes(status.storage.free_bytes)} free`],
      ["Runtime state", status.storage.state_root, "SQLite, cache, temp and logs"],
      ["Jobs", Object.entries(status.jobs).map(([k,v]) => `${k}: ${v}`).join(" · ") || "No jobs", "Persistent after navigation"],
    ];
    document.querySelector("#adminGrid").innerHTML = values.map(([title,main,note]) => `<div class="admin-item"><h2>${escapeHtml(title)}</h2><p><strong>${escapeHtml(main)}</strong></p><p>${escapeHtml(note)}</p></div>`).join("");
    const requests = access.requests || [];
    document.querySelector("#adminAccessRows").innerHTML = requests.length ? requests.map(item => `<tr><td>${escapeHtml(item.user_id)}</td><td>${escapeHtml(item.quota_day)}</td><td>${escapeHtml(item.requested_uses)}</td><td>${escapeHtml(item.reason || "")}</td><td><span class="pill ${escapeHtml(item.status)}">${escapeHtml(item.status)}</span></td><td>${item.status === "pending" ? `<button class="row-action approve" data-access-decision="approved" data-access-id="${escapeHtml(item.id)}">Approve</button><button class="row-action reject" data-access-decision="rejected" data-access-id="${escapeHtml(item.id)}">Reject</button>` : escapeHtml(item.decision_note || item.decided_by || "-")}</td></tr>`).join("") : '<tr><td colspan="6" class="empty">No access request.</td></tr>';
    const usage = access.usage || [];
    document.querySelector("#adminUsageRows").innerHTML = usage.length ? usage.map(item => `<tr><td>${escapeHtml(item.user_id)}</td><td>${escapeHtml(item.provider)}</td><td>${escapeHtml(item.used)} / ${escapeHtml(item.base_limit ?? access.base_daily_limit)} base</td></tr>`).join("") : '<tr><td colspan="3" class="empty">No API generation has been used today.</td></tr>';
    state.adminAccounts = accounts.accounts || [];
    state.adminPermissions = accounts.known_permissions || [];
    document.querySelector("#developerAccountRows").innerHTML = state.adminAccounts.length ? state.adminAccounts.map(item => `<tr><td>${escapeHtml(item.email)}</td><td>${escapeHtml(item.role)}</td><td>${escapeHtml(item.daily_api_limit)}</td><td>${escapeHtml((item.permissions || []).join(", ") || "-")}</td><td>${item.enabled ? '<span class="pill completed">enabled</span>' : '<span class="pill failed">disabled</span>'}</td><td><button class="row-action" data-developer-email="${escapeHtml(item.email)}">Edit</button></td></tr>`).join("") : '<tr><td colspan="6" class="empty">No developer account.</td></tr>';
  } catch (error) { document.querySelector("#adminGrid").innerHTML = `<div class="empty-block">${escapeHtml(error.message)}</div>`; }
}

function openDeveloperAccount(email = "") {
  const account = state.adminAccounts.find(item => item.email === email);
  document.querySelector("#developerAccountEmail").value = account?.email || "";
  document.querySelector("#developerAccountEmail").readOnly = Boolean(account);
  document.querySelector("#developerAccountRole").value = account?.role || "developer";
  document.querySelector("#developerAccountLimit").value = account?.daily_api_limit ?? 10;
  const accountPermissions=account?.permissions||[];
  const selected=new Set(accountPermissions.includes("*")
    ? state.adminPermissions.map(item=>item.id)
    : (account ? accountPermissions : state.adminPermissions.filter(item=>item.default).map(item=>item.id)));
  state.adminPermissions.filter(item=>item.parent&&selected.has(item.id)).forEach(item=>selected.add(item.parent));
  const groups=[...new Set(state.adminPermissions.map(item=>item.group))];
  const permissionRoot=document.querySelector("#developerAccountPermissions");
  permissionRoot.innerHTML=groups.map(group=>{
    const roots=state.adminPermissions.filter(item=>item.group===group&&!item.parent);
    return `<section class="permission-branch"><h4>${escapeHtml(group)}</h4><div class="permission-feature-list">${roots.map(item=>{
      const children=state.adminPermissions.filter(child=>child.parent===item.id);
      return `<article class="permission-feature"><label class="permission-feature-main"><input type="checkbox" value="${escapeHtml(item.id)}" data-feature-id="${escapeHtml(item.id)}" ${selected.has(item.id)?"checked":""}><span><b>${escapeHtml(item.label)}</b>${item.description?`<small>${escapeHtml(item.description)}</small>`:""}</span></label>${children.length?`<div class="permission-suboptions"><span>Advanced permissions</span>${children.map(child=>`<label class="permission-option"><input type="checkbox" value="${escapeHtml(child.id)}" data-parent-permission="${escapeHtml(item.id)}" ${selected.has(child.id)?"checked":""}><span>${escapeHtml(child.label)}</span></label>`).join("")}</div>`:""}</article>`;
    }).join("")}</div></section>`;
  }).join("");
  const syncPermissionChildren=featureId=>{
    const parent=permissionRoot.querySelector(`[data-feature-id="${featureId}"]`);
    permissionRoot.querySelectorAll(`[data-parent-permission="${featureId}"]`).forEach(child=>{child.disabled=!parent.checked;if(!parent.checked)child.checked=false;});
  };
  permissionRoot.querySelectorAll("[data-feature-id]").forEach(parent=>syncPermissionChildren(parent.dataset.featureId));
  permissionRoot.onchange=event=>{
    const input=event.target;if(!(input instanceof HTMLInputElement))return;
    if(input.dataset.featureId)syncPermissionChildren(input.dataset.featureId);
    if(input.dataset.parentPermission&&input.checked){const parent=permissionRoot.querySelector(`[data-feature-id="${input.dataset.parentPermission}"]`);if(parent){parent.checked=true;syncPermissionChildren(input.dataset.parentPermission);}}
  };
  document.querySelector("#developerAccountPassword").value = "";
  document.querySelector("#developerAccountEnabled").checked = account?.enabled ?? true;
  document.querySelector("#developerAccountStatus").textContent = account ? "Leave password blank to keep it." : "Temporary password defaults to 000000.";
  document.querySelector("#developerAccountDialog").showModal();
}

async function saveDeveloperAccount() {
  const email = document.querySelector("#developerAccountEmail").value.trim();
  const existing = state.adminAccounts.some(item => item.email === email);
  const passwordInput = document.querySelector("#developerAccountPassword").value;
  const payload = {
    email,
    role:document.querySelector("#developerAccountRole").value,
    daily_api_limit:Number(document.querySelector("#developerAccountLimit").value || 0),
    permissions:[...document.querySelectorAll("#developerAccountPermissions input:checked")].map(input=>input.value),
    password:passwordInput || (existing ? "" : "000000"),
    enabled:document.querySelector("#developerAccountEnabled").checked,
  };
  try {
    await api("/api/admin/developer-accounts", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(payload)});
    document.querySelector("#developerAccountDialog").close(); toast(`Saved developer account ${email}.`); await refreshAdmin();
  } catch (error) { document.querySelector("#developerAccountStatus").textContent = error.message; }
}

async function decideAccessRequest(id, decision) {
  const note = prompt(`${decision === "approved" ? "Approval" : "Rejection"} note:`, decision === "approved" ? "Approved for today's work" : "Please contact the administrator") || "";
  try {
    await api(`/api/admin/access-requests/${id}/decision`, {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({decision, note})});
    toast(`Request ${decision}.`); await refreshAdmin();
  } catch (error) { toast(error.message); }
}

function setFoqStep(step, message = "") {
  document.querySelectorAll("[data-foq-panel]").forEach(el => el.classList.toggle("active", Number(el.dataset.foqPanel) === step));
  document.querySelectorAll("[data-foq-step]").forEach(el => {
    const value = Number(el.dataset.foqStep);
    el.classList.toggle("active", value === step);
    el.classList.toggle("complete", value < step);
  });
  if (message) document.querySelector("#foqMessage").textContent = message;
  document.querySelector("#view-foq").scrollIntoView({behavior:"smooth", block:"start"});
}

async function refreshFoqConfig() {
  if (!state.foq.config) {
    try { state.foq.config = await api("/api/foq/config"); }
    catch (error) { toast(error.message); return; }
  }
  const config = state.foq.config;
  const database = config.database || {};
  const sourceSelect = document.querySelector("#foqDbSource");
  sourceSelect.innerHTML = (database.sources || []).map(source => `<option value="${escapeHtml(source.id)}">${escapeHtml(source.label)}</option>`).join("") || '<option value="">Not configured</option>';
  sourceSelect.value = database.default_source || database.sources?.[0]?.id || "";
  const selectedSource = (database.sources || []).find(source => source.id === sourceSelect.value) || database;
  document.querySelector("#foqDbTable").value = selectedSource.table || "AUTO";
  document.querySelector("#foqDbStatus").textContent = config.mapping_available
    ? `FOQ Location ready. ${database.configured ? "Historical database is available when enabled." : "Database history is not configured; SPEC-only check remains available."}`
    : "FOQ Location mapping is unavailable on the service host.";
}

async function refreshFoqArtifacts() {
  if (!state.artifacts.length) await refreshArtifacts();
  const list = document.querySelector("#foqArtifactList");
  if (!state.artifacts.length) { list.innerHTML = '<div class="empty-block">Add one or more completed CMBX files.</div>'; return; }
  if (!state.foq.artifactIds.size && state.artifacts.length === 1) state.foq.artifactIds.add(state.artifacts[0].id);
  list.innerHTML = state.artifacts.map(item => `<label class="selection-item"><input type="checkbox" data-foq-artifact="${item.id}" ${state.foq.artifactIds.has(item.id) ? "checked" : ""}><strong>${escapeHtml(item.original_name)}</strong><small>${formatBytes(item.size_bytes)} · ${escapeHtml(item.owner)}</small></label>`).join("");
}

async function waitForJob(jobId, onUpdate) {
  for (let count = 0; count < 1800; count += 1) {
    const job = await api(`/api/jobs/${jobId}`);
    if (onUpdate) onUpdate(job);
    if (job.status === "completed") return job.result;
    if (job.status === "failed") throw new Error(job.error || job.message || "Job failed");
    await new Promise(resolve => setTimeout(resolve, 500));
  }
  throw new Error("The job did not finish within the expected time");
}

async function inspectFoqScope() {
  const ids = [...state.foq.artifactIds];
  if (!ids.length) { toast("Choose at least one CMBX file."); return; }
  const button = document.querySelector("#inspectFoq"); button.disabled = true;
  document.querySelector("#foqScopeStatus").textContent = "Preparing sequence scope...";
  try {
    const job = await api("/api/foq/inspect", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({artifact_ids:ids})});
    state.foq.scope = await waitForJob(job.id, update => {
      const percent = Math.round(100 * update.progress_current / Math.max(1, update.progress_total));
      document.querySelector("#foqScopeStatus").textContent = `${percent}% · ${update.message}`;
    });
    state.foq.sequenceKeys = new Set(state.foq.scope.sequences.filter(item => item.default_selected).map(item => item.key));
    state.foq.injections = {};
    state.foq.scope.sequences.forEach(item => { state.foq.injections[item.key] = new Set(item.injections.filter(injection => injection.default_selected).map(injection => injection.id)); });
    state.foq.metrics = state.foq.scope.metrics || [];
    state.foq.selectedMetrics = new Set(state.foq.metrics);
    renderFoqScope();
  } catch (error) { toast(error.message); document.querySelector("#foqScopeStatus").textContent = error.message; }
  finally { button.disabled = false; }
}

function unresolvedFoqDuplicates() {
  const unresolved = [];
  for (const item of state.foq.scope?.sequences || []) {
    if (!state.foq.sequenceKeys.has(item.key)) continue;
    const selected = state.foq.injections[item.key] || new Set();
    const groups = {};
    item.injections.forEach(injection => { const key = injection.name.toLowerCase(); (groups[key] ||= []).push(injection); });
    Object.values(groups).forEach(group => { if (group.length > 1 && !group.some(injection => selected.has(injection.id))) unresolved.push(`${item.sequence} / ${group[0].name}`); });
  }
  return unresolved;
}

function renderFoqScope() {
  const rows = document.querySelector("#foqScopeRows");
  const sequences = state.foq.scope?.sequences || [];
  if (!sequences.length) { rows.innerHTML = '<tr><td colspan="5" class="empty">No sequence found.</td></tr>'; return; }
  rows.innerHTML = sequences.map(item => {
    const enabled = item.eligible;
    const checked = state.foq.sequenceKeys.has(item.key);
    const head = `<tr class="${enabled ? "" : "scope-support"}"><td><input type="checkbox" data-foq-sequence="${escapeHtml(item.key)}" ${checked ? "checked" : ""} ${enabled ? "" : "disabled"}></td><td><strong>${escapeHtml(item.package)}</strong><br>${escapeHtml(item.sequence)}</td><td>${escapeHtml(item.device)}</td><td>${escapeHtml(item.report_template || "-")}</td><td>${escapeHtml(item.reason)}</td></tr>`;
    if (!enabled) return head;
    const groups = {};
    item.injections.forEach(injection => { const key = injection.name.toLowerCase(); (groups[key] ||= []).push(injection); });
    const children = item.injections.map(injection => {
      const selected = (state.foq.injections[item.key] || new Set()).has(injection.id);
      const duplicate = groups[injection.name.toLowerCase()].length > 1;
      const type = duplicate ? "radio" : "checkbox";
      const name = duplicate ? `dup-${btoa(unescape(encodeURIComponent(item.key + injection.name))).replace(/=/g,"")}` : "";
      const detail = duplicate ? `Occurrence ${injection.occurrence}/${injection.occurrence_total}` : "Injection";
      return `<tr class="scope-injection"><td><input type="${type}" ${name ? `name="${name}"` : ""} data-foq-injection="${escapeHtml(injection.id)}" data-sequence-key="${escapeHtml(item.key)}" ${selected ? "checked" : ""} ${checked ? "" : "disabled"}></td><td>${escapeHtml(injection.name)} <small>${detail}</small></td><td></td><td></td><td>${selected ? "Selected" : ""}</td></tr>`;
    }).join("");
    return head + children;
  }).join("");
  const selected = state.foq.sequenceKeys.size;
  const unresolved = unresolvedFoqDuplicates();
  document.querySelector("#foqScopeStatus").textContent = `${selected} sequence(s) selected${unresolved.length ? ` · ${unresolved.length} duplicate choice(s) unresolved` : ""}.`;
  document.querySelector("#confirmFoqScope").disabled = !selected || unresolved.length > 0;
}

async function refreshFoqMetrics() {
  const devices = [...new Set((state.foq.scope?.sequences || []).filter(item => state.foq.sequenceKeys.has(item.key)).map(item => item.device))];
  if (!devices.length) { state.foq.metrics = []; state.foq.selectedMetrics.clear(); renderFoqMetrics(); return; }
  try {
    const result = await api("/api/foq/metrics", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({devices})});
    const previous = state.foq.selectedMetrics;
    state.foq.metrics = result.metrics;
    state.foq.selectedMetrics = new Set(result.metrics.filter(metric => previous.has(metric)));
    if (!state.foq.selectedMetrics.size) state.foq.selectedMetrics = new Set(result.metrics);
    renderFoqMetrics();
  } catch (error) { toast(error.message); }
}

function metricPresets() { try { return JSON.parse(localStorage.getItem("cmbx.foq.metricPresets") || "{}"); } catch (_) { return {}; } }
function refreshMetricPresetList() { const presets = metricPresets(); document.querySelector("#foqMetricPreset").innerHTML = '<option value="">Saved metric set</option>' + Object.keys(presets).sort().map(name => `<option>${escapeHtml(name)}</option>`).join(""); }
function renderFoqMetrics() {
  const query = document.querySelector("#foqMetricSearch").value.trim().toLowerCase();
  const visible = state.foq.metrics.filter(metric => metric.toLowerCase().includes(query));
  document.querySelector("#foqMetricList").innerHTML = visible.length ? visible.map(metric => `<label class="metric-option"><input type="checkbox" data-foq-metric="${escapeHtml(metric)}" ${state.foq.selectedMetrics.has(metric) ? "checked" : ""}><span>${escapeHtml(metric)}</span></label>`).join("") : '<div class="empty-block">No matching metric.</div>';
  document.querySelector("#foqMetricStatus").textContent = `${state.foq.selectedMetrics.size} of ${state.foq.metrics.length} metric(s) selected.`;
  document.querySelector("#confirmFoqMetrics").disabled = !state.foq.selectedMetrics.size;
  refreshMetricPresetList();
}

function selectedFoqSequencesPayload() {
  const payload = {};
  state.foq.sequenceKeys.forEach(key => { payload[key] = [...(state.foq.injections[key] || new Set())]; });
  return payload;
}

async function runFoqCheck() {
  const button = document.querySelector("#runFoqCheck"); button.disabled = true;
  const historyEnabled = document.querySelector("#foqUseHistory").checked;
  const history = {enabled:historyEnabled, source_id:document.querySelector("#foqDbSource").value, table:document.querySelector("#foqDbTable").value.trim() || "AUTO", limit:Number(document.querySelector("#foqHistoryLimit").value || 5000), filters:{model:document.querySelector("#foqDbModels").value, date_from:document.querySelector("#foqDateFrom").value, date_to:document.querySelector("#foqDateTo").value}};
  try {
    const job = await api("/api/foq/run", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({artifact_ids:[...state.foq.artifactIds], selected_sequences:selectedFoqSequencesPayload(), metrics:[...state.foq.selectedMetrics], history})});
    const result = await waitForJob(job.id, update => {
      const percent = Math.round(100 * update.progress_current / Math.max(1, update.progress_total));
      document.querySelector("#foqProgressBar").style.width = `${percent}%`;
      document.querySelector("#foqRunStatus").textContent = `${percent}% · ${update.message}`;
    });
    state.foq.result = result;
    state.foq.results = result.rows || [];
    renderFoqResults(result);
    document.querySelector("#foqRunStatus").textContent = `Complete · ${result.summary.total} mapped value(s)`;
  } catch (error) { toast(error.message); document.querySelector("#foqRunStatus").textContent = error.message; }
  finally { button.disabled = false; }
}

function displayValue(value) { return typeof value === "number" ? Number(value.toPrecision(8)).toString() : String(value ?? ""); }

const TCC_QC_SUMMARY_COLUMNS = [
  {label:"Module", aliases:["ModelNo"], fallback:group=>group[0]?.device},
  {label:"SN", aliases:["Serial"], fallback:group=>group[0]?.sequence},
  {label:"Trial"}, {label:"FW Rev.", aliases:["Firmware"]}, {label:"Test Stand", aliases:["TimeBase"]}, {label:"DVT No."},
  {label:"FOQ Date", aliases:["TestDate","SubmitDate"]}, {label:"Overall result", derive:"overall"}, {label:"QC Comment[Xiaoshu]"},
  {label:"Heat Up Time", aliases:["HeatUp_Time_20to50"]}, {label:"Cool Down Time", aliases:["CoolDown_Time_50to20"]},
  {label:"Ripple No. Precision >0.03℃"}, {label:"Overshoot ℃ (0.00)"}, {label:"Precision", aliases:["TempPrecision"]},
  {label:"Accuracy MAX", derive:"accuracy_max"}, {label:"Stability", aliases:["TempStability"]}, {label:"Accuracy total time/min"},
  {label:"Preheater Simulator Box Test", derive:"preheater_result"}, {label:"Valve"}, {label:"Column ID", derive:"column_id_result"}, {label:"Fan"},
  {label:"Accruacy 10", aliases:["TempAcc10"]}, {label:"Accruacy 20", aliases:["TempAcc20"]}, {label:"Accruacy 40", aliases:["TempAcc40"]},
  {label:"Accruacy 60", aliases:["TempAcc60"]}, {label:"Accruacy 85", aliases:["TempAcc85"]}, {label:"Leak sensor"},
  {label:"Distribution Test Result"}, {label:"Stress Test Result"},
  {label:"Preheater temperature up", aliases:["Diff_PhLeft_HtTmp"]}, {label:"right", aliases:["Diff_PhRight_HtTmp"]},
  {label:"preheater noise", aliases:["Noise_PrehtLeft_Temp"]}, {label:"right", aliases:["Noise_PrehtRight_Temp"]},
  {label:"Preheater tempstep"}, {label:"right"}, {label:"Keyboard"},
  {label:"Upper_Valve precision 6_1"}, {label:"Upper_Valve precision 1_2"}, {label:"Upper_Valve precision 6_1"},
  {label:"Lower_Valve precision 6_1"}, {label:"Lower_Valve precision 1_2"}, {label:"Lower_Valve precision 6_1"},
];

function foqSequenceGroups() {
  const groups = new Map();
  state.foq.results.forEach(row => {
    const key = `${row.package}\u0000${row.sequence}\u0000${row.device}`;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(row);
  });
  return [...groups.values()];
}

function foqMetricValue(group, aliases=[]) {
  const wanted = new Set(aliases.map(value => value.toLowerCase()));
  const row = group.find(item => wanted.has(String(item.db_field).toLowerCase()));
  return row ? displayValue(row.value) : "";
}

function foqAggregateResult(rows) {
  if (!rows.length) return "";
  const ownValues = rows.map(row => String(row.value ?? "").toLowerCase());
  const statuses = rows.map(row => String(row.spec_status || "").toLowerCase());
  if (statuses.includes("fail") || ownValues.some(value => ["fail","failed","test failed","false","no","not ok"].includes(value))) return "Fail";
  if (statuses.includes("review") || statuses.includes("not_evaluated")) return "Review";
  return statuses.includes("pass") || ownValues.some(value => ["ok","pass","passed","test passed","true","yes"].includes(value)) ? "Pass" : "";
}

function foqSummaryValue(group, column) {
  if (column.aliases) {
    const value = foqMetricValue(group, column.aliases);
    if (value !== "") return value;
  }
  if (column.derive === "overall") return foqAggregateResult(group);
  if (column.derive === "accuracy_max") {
    const values = group.filter(row => /^TempAcc(10|20|40|60|80|85|120)$/i.test(row.db_field)).map(row => Number(row.value)).filter(Number.isFinite);
    return values.length ? displayValue(Math.max(...values.map(Math.abs))) : "";
  }
  if (column.derive === "preheater_result") return foqAggregateResult(group.filter(row => /^RES_Preheater_/i.test(row.db_field)));
  if (column.derive === "column_id_result") return foqAggregateResult(group.filter(row => /^RES_ColumnID_/i.test(row.db_field)));
  return column.fallback ? displayValue(column.fallback(group)) : "";
}

function currentFoqOutput() {
  const layout = document.querySelector("#foqOutputLayout")?.value || "metric";
  if (layout === "tcc_qc_summary") {
    return {headers:TCC_QC_SUMMARY_COLUMNS.map(column=>column.label), rows:foqSequenceGroups().map(group=>TCC_QC_SUMMARY_COLUMNS.map(column=>foqSummaryValue(group,column))), name:"TCC_QC_Summary"};
  }
  const metric = document.querySelector("#foqChartMetric")?.value || "";
  const rows = state.foq.results.filter(row => row.db_field === metric);
  return {headers:["Module","CMBX","Sequence","Injection","Metric","Value","Unit","SPEC","History status","History mean","Delta","Z score"], rows:rows.map(row=>[row.device,row.package,row.sequence,row.injection,row.db_field,displayValue(row.value),row.unit,row.spec_status,row.history_status,row.history?.mean == null ? "" : displayValue(row.history.mean),row.history_delta == null ? "" : displayValue(row.history_delta),row.history_z == null ? "" : displayValue(row.history_z)]), name:metric || "FOQ_metric"};
}

function renderFoqOutput() {
  const output = currentFoqOutput();
  document.querySelector("#foqOutputHead").innerHTML = `<tr>${output.headers.map(value=>`<th>${escapeHtml(value)}</th>`).join("")}</tr>`;
  document.querySelector("#foqOutputRows").innerHTML = output.rows.length ? output.rows.map(row=>`<tr>${row.map(value=>`<td>${escapeHtml(displayValue(value))}</td>`).join("")}</tr>`).join("") : `<tr><td colspan="${output.headers.length}" class="empty">No matching sequence result.</td></tr>`;
  const layout = document.querySelector("#foqOutputLayout").value;
  document.querySelector("#foqOutputStatus").textContent = layout === "metric" ? `${output.rows.length} sequence result(s) for the selected chart metric.` : `${output.rows.length} sequence row(s). Columns without a verified FOQ Location mapping remain blank.`;
}

function foqOutputTsv() {
  const output=currentFoqOutput();
  const clean=value=>String(value??"").replace(/\t/g," ").replace(/[\r\n]+/g," ");
  return [output.headers,...output.rows].map(row=>row.map(clean).join("\t")).join("\r\n");
}

async function copyFoqOutput() {
  const text=foqOutputTsv();
  try { await navigator.clipboard.writeText(text); toast("FOQ result table copied."); }
  catch (_error) { const area=document.createElement("textarea"); area.value=text; document.body.append(area); area.select(); document.execCommand("copy"); area.remove(); toast("FOQ result table copied."); }
}

function downloadFoqOutput() {
  const output=currentFoqOutput(); const blob=new Blob(["\ufeff",foqOutputTsv()],{type:"text/tab-separated-values;charset=utf-8"});
  const link=document.createElement("a"); link.href=URL.createObjectURL(blob); link.download=`${output.name.replace(/[^A-Za-z0-9_.-]+/g,"_")}.tsv`; link.click(); setTimeout(()=>URL.revokeObjectURL(link.href),1000);
}

function renderFoqResults(result) {
  const summary = result.summary || {};
  document.querySelector("#foqSummary").innerHTML = [["Total",summary.total,""],["Pass",summary.pass,"pass"],["Fail",summary.fail,"fail"],["Review",summary.review,""],["Not evaluated",summary.not_evaluated,""]].map(([label,value,kind]) => `<div class="metric ${kind}"><b>${value || 0}</b><span>${label}</span></div>`).join("");
  document.querySelector("#foqResultRows").innerHTML = state.foq.results.length ? state.foq.results.map(row => {
    const history = row.history?.count ? `N=${row.history.count}; z=${row.history_z == null ? "-" : Number(row.history_z).toFixed(2)}<br>${escapeHtml(row.history_status)}` : "Not loaded";
    return `<tr><td><strong>${escapeHtml(row.package)}</strong><br>${escapeHtml(row.sequence)}</td><td><strong>${escapeHtml(row.db_field)}</strong><br><small>${escapeHtml(row.description)}</small></td><td>${escapeHtml(displayValue(row.value))} ${escapeHtml(row.unit)}</td><td class="spec-${escapeHtml(row.spec_status)}">${escapeHtml(row.spec_status)}<br><small>${escapeHtml(row.spec_evidence)}</small></td><td>${history}</td><td>${escapeHtml(row.report_sheet)}!${escapeHtml(row.report_cell)}<br><small>${escapeHtml(row.calculation_status)}</small></td><td>${escapeHtml(row.injection)}</td></tr>`;
  }).join("") : '<tr><td colspan="7" class="empty">No mapped result was returned.</td></tr>';
  const metrics = [...new Set(state.foq.results.map(row => row.db_field))];
  const select = document.querySelector("#foqChartMetric"); select.innerHTML = '<option value="">Choose a result metric</option>' + metrics.map(metric => `<option>${escapeHtml(metric)}</option>`).join("");
  if (metrics.length) { select.value = metrics[0]; renderFoqChart(metrics[0]); }
  renderFoqOutput();
  document.querySelector("#foqResultStatus").textContent = `${result.history?.enabled ? `${result.history.count} historical row(s) compared` : "SPEC-only comparison"}.`;
}

function renderFoqChart(metric) {
  renderFoqOutput();
  const rows = state.foq.results.filter(row => row.db_field === metric && Number.isFinite(Number(row.value)));
  const chart = document.querySelector("#foqChart");
  if (!rows.length) { chart.innerHTML = '<div class="empty-block">No numeric value is available for this metric.</div>'; return; }
  const samples = state.foq.result?.history_samples || {};
  const historical = rows.flatMap(row => samples[`${row.device}|${row.db_field}`] || []);
  const references = rows.flatMap(row => [row.history?.mean,row.history?.ucl,row.history?.lcl].filter(value => Number.isFinite(Number(value))).map(Number));
  const values = rows.map(row => Number(row.value)); const all = values.concat(historical, references); let min = Math.min(...all), max = Math.max(...all); if (min === max) { min -= 1; max += 1; } const pad = (max-min)*.12; min -= pad; max += pad;
  const width=900,height=250,left=62,right=28,top=22,bottom=55; const y=value => top+(max-value)/(max-min)*(height-top-bottom); const x=index => left+(index+1)*(width-left-right)/(rows.length+1);
  const reference = rows.find(row => row.history?.count)?.history || {};
  const lines = [[reference.ucl,"UCL","#b66a00"],[reference.mean,"Mean","#536273"],[reference.lcl,"LCL","#b66a00"]].filter(([value]) => Number.isFinite(Number(value))).map(([value,label,color]) => `<line x1="${left}" y1="${y(Number(value))}" x2="${width-right}" y2="${y(Number(value))}" stroke="${color}" stroke-dasharray="4 3"/><text x="${width-right-4}" y="${y(Number(value))-5}" text-anchor="end" fill="${color}" font-size="12">${label} ${Number(value).toPrecision(5)}</text>`).join("");
  const historyPoints = historical.map((value,index) => { const hx=left+((index+.5)/Math.max(1,historical.length))*(width-left-right); return `<circle cx="${hx}" cy="${y(Number(value))}" r="2.2" fill="#aeb8c4" opacity=".8"/>`; }).join("");
  const points = rows.map((row,index) => { const color=row.spec_status==="fail"?"#d9272e":"#2878d0"; return `<circle cx="${x(index)}" cy="${y(Number(row.value))}" r="7" fill="#fff" stroke="${color}" stroke-width="4"/><text x="${x(index)}" y="${y(Number(row.value))-13}" text-anchor="middle" font-size="12">${escapeHtml(displayValue(row.value))}</text><text x="${x(index)}" y="${height-22}" text-anchor="middle" font-size="11" fill="#536273">${escapeHtml(row.sequence.slice(0,18))}</text>`; }).join("");
  chart.innerHTML = `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="${escapeHtml(metric)} comparison"><line x1="${left}" y1="${top}" x2="${left}" y2="${height-bottom}" stroke="#9aa5b1"/><line x1="${left}" y1="${height-bottom}" x2="${width-right}" y2="${height-bottom}" stroke="#9aa5b1"/>${lines}${historyPoints}${points}<text x="${left}" y="15" font-size="14" font-weight="700">${escapeHtml(metric)} | ${historical.length} historical / ${rows.length} current</text></svg>`;
}

function renderAnalysisSources(kind) {
  const model = state.analysis[kind];
  const root = document.querySelector(`[data-analysis-source="${kind}"]`);
  if (!root) return;
  const sources = state.artifacts.filter(item => item.kind === "cmbx_source");
  root.innerHTML = `<div class="section-heading"><div><h2>CMBX sources</h2><p>Uploaded sources are shared across analysis workflows.</p></div><label class="secondary-button">Add CMBX<input type="file" accept=".cmbx" multiple data-analysis-upload="${kind}" hidden></label></div>` + (sources.length ? `<div class="source-chip-list">${sources.map(item => `<label class="source-chip"><input type="checkbox" data-analysis-artifact="${kind}" value="${item.id}" ${model.artifactIds.has(item.id)?"checked":""}><span>${escapeHtml(item.original_name)}</span></label>`).join("")}</div>` : '<div class="empty-block">Add one or more CMBX files.</div>');
}

function analysisFilters(kind) {
  return state.analysis[kind].filters;
}

function visibleChannels(kind) {
  const catalog=state.analysis[kind].catalog; if(!catalog) return [];
  const f=analysisFilters(kind);
  return catalog.channels.filter(row => Object.entries(f).every(([key,value]) => !value || String(row[key])===value));
}

function setAnalysisStep(kind,step){const model=state.analysis[kind];model.step=step;document.querySelectorAll(`[data-${kind}-step]`).forEach(item=>{const value=Number(item.dataset[`${kind}Step`]);item.classList.toggle("active",value===step);item.classList.toggle("complete",value<step);});document.querySelectorAll(`[data-${kind}-panel]`).forEach(item=>item.classList.toggle("active",Number(item.dataset[`${kind}Panel`])===step));document.querySelector(`#view-${kind}`).scrollIntoView({behavior:"smooth",block:"start"});}

function populateAnalysisFilters(kind,changed=""){
  const model=state.analysis[kind],rows=model.catalog?.channels||[],order=["package","sequence","injection","channel"];
  const changedIndex=order.indexOf(changed);if(changedIndex>=0)order.slice(changedIndex+1).forEach(key=>model.filters[key]="");
  order.forEach((key,index)=>{
    const eligible=rows.filter(row=>order.slice(0,index).every(previous=>!model.filters[previous]||String(row[previous])===model.filters[previous]));
    const values=[...new Set(eligible.map(row=>String(row[key]||"")).filter(Boolean))].sort((a,b)=>a.localeCompare(b));
    if(model.filters[key]&&!values.includes(model.filters[key]))model.filters[key]="";
    const select=document.querySelector(`#view-${kind} [data-filter="${key}"]`);if(select)select.innerHTML=`<option value="">All ${key}s</option>`+values.map(value=>`<option value="${escapeHtml(value)}" ${model.filters[key]===value?"selected":""}>${escapeHtml(value)}</option>`).join("");
  });
}

function renderChannelPicker(kind) {
  const rows=visibleChannels(kind), selected=state.analysis[kind].selected;
  document.querySelector(`#${kind}ChannelList`).innerHTML=rows.length?`<div class="channel-list-head"><span>Use</span><span>Channel</span><span>Package</span><span>Sequence</span><span>Injection</span></div>${rows.map(row=>`<label class="channel-list-row"><span><input type="checkbox" data-analysis-channel="${kind}" value="${escapeHtml(row.key)}" ${selected.has(row.key)?"checked":""}></span><strong>${escapeHtml(row.channel)}</strong><span title="${escapeHtml(row.package)}">${escapeHtml(row.package)}</span><span title="${escapeHtml(row.sequence)}">${escapeHtml(row.sequence)}</span><span title="${escapeHtml(row.injection)}">${escapeHtml(row.injection)}</span></label>`).join("")}`:'<div class="empty-block">No channel matches the four filters.</div>';
  const status=document.querySelector(`#${kind}SelectionStatus`);if(status)status.textContent=`${selected.size} channel(s) selected.`;
}

async function loadAnalysisCatalog(kind) {
  const model=state.analysis[kind]; if(!model.artifactIds.size) return toast("Choose at least one CMBX source.");
  try { model.catalog=await api("/api/analysis/catalog",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({artifact_ids:[...model.artifactIds]}),timeoutMs:120000});model.selected.clear();model.filters={package:"",sequence:"",injection:"",channel:""};populateAnalysisFilters(kind);renderChannelPicker(kind);setAnalysisStep(kind,2);toast(`${model.catalog.channels.length} channel context(s) loaded.`); }
  catch(error){toast(error.message);}
}

function reviewRawSelection(){const model=state.analysis.raw,lookup=new Map((model.catalog?.channels||[]).map(row=>[row.key,row])),rows=[...model.selected].map(key=>lookup.get(key)).filter(Boolean);if(!rows.length)return toast("Choose channels to export.");document.querySelector("#rawPreviewRows").innerHTML=rows.map(row=>`<tr><td>${escapeHtml(row.package)}</td><td>${escapeHtml(row.sequence)}</td><td>${escapeHtml(row.injection)}</td><td>${escapeHtml(row.channel)}</td></tr>`).join("");setAnalysisStep("raw",3);}

async function exportRawData() {
  const model=state.analysis.raw; if(!model.selected.size) return toast("Choose channels to export.");
  try { const job=await api("/api/raw/export",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({artifact_ids:[...model.artifactIds],channel_keys:[...model.selected]})}); const result=await waitForJob(job.id); document.querySelector("#rawResult").innerHTML=`<div class="generation-success"><span>${result.exported} trace(s) exported.</span><a class="primary-button" href="${result.download_url}">Download ZIP</a></div>`; }
  catch(error){toast(error.message);}
}

async function requestChromatograms(performIntegration=false) {
  const model=state.analysis.chrom; if(!model.selected.size) return toast("Choose at least one trace.");
  const integration={smoothing_width_s:Number(document.querySelector("#intSmooth").value),noise_multiplier:Number(document.querySelector("#intNoise").value),minimum_height:Number(document.querySelector("#intHeight").value),minimum_area:Number(document.querySelector("#intArea").value),minimum_width_s:Number(document.querySelector("#intWidth").value)};
  try {document.querySelector("#chromStatus").textContent=performIntegration?"Integrating full-resolution traces...":"Loading trace points...";model.plot=await api("/api/chromatograms/query",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({artifact_ids:[...model.artifactIds],channel_keys:[...model.selected],integration,perform_integration:performIntegration}),timeoutMs:180000});model.viewStack=[];setAnalysisStep("chrom",3);renderChromChart();renderPeakRows();document.querySelector("#chromStatus").textContent=performIntegration?`${model.plot.peaks.length} peak(s) integrated.`:"Traces plotted. Adjust parameters, then integrate.";}
  catch(error){toast(error.message);}
}

const plotChromatograms=()=>requestChromatograms(false);
const integrateChromatograms=()=>requestChromatograms(true);

const TRACE_COLORS=["#2478c7","#d9272e","#07856d","#a05a00","#7847a8","#007a99","#cf5c00","#526273"];
function renderChromChart(domain=null) {
  const model=state.analysis.chrom, root=document.querySelector("#chromChart"), traces=model.plot?.traces||[]; if(!traces.length){root.innerHTML='<div class="empty-block">No traces plotted.</div>';return;}
  const layout=document.querySelector("#chromLayout").value, width=1000, rowH=layout==="separate"?210:430, height=layout==="separate"?rowH*traces.length:430, left=64,right=22,top=24,bottom=38;
  let xmin=domain?.xmin??Math.min(...traces.map(t=>t.min_time)),xmax=domain?.xmax??Math.max(...traces.map(t=>t.max_time));
  const panels=traces.map((trace,index)=>{
    const values=trace.points.filter(p=>p[0]>=xmin&&p[0]<=xmax); const ymin=domain?.ymin??Math.min(...values.map(p=>p[1])), ymax0=domain?.ymax??Math.max(...values.map(p=>p[1])); const ymax=ymax0===ymin?ymin+1:ymax0; const panelTop=layout==="separate"?index*rowH+top:top, panelBottom=layout==="separate"?(index+1)*rowH-bottom:height-bottom; const x=v=>left+(v-xmin)/(xmax-xmin)*(width-left-right), y=v=>panelBottom-(v-ymin)/(ymax-ymin)*(panelBottom-panelTop); const path=values.map((p,i)=>`${i?"L":"M"}${x(p[0]).toFixed(2)},${y(p[1]).toFixed(2)}`).join(" "); const peaks=(model.plot.peaks||[]).filter(p=>p.trace_key===trace.key&&p.start_min>=xmin&&p.end_min<=xmax).map(p=>`<line x1="${x(p.start_min)}" y1="${y(p.baseline_start)}" x2="${x(p.end_min)}" y2="${y(p.baseline_end)}" stroke="#d9272e" stroke-width="3"/><circle cx="${x(p.apex_min)}" cy="${y(p.baseline_start+p.height)}" r="3" fill="#d9272e"/>`).join(""); return `<g><path d="${path}" fill="none" stroke="${TRACE_COLORS[index%TRACE_COLORS.length]}" stroke-width="2"/>${peaks}<text x="${left+5}" y="${panelTop+15}" font-size="12" fill="${TRACE_COLORS[index%TRACE_COLORS.length]}">${escapeHtml(trace.label)}</text></g>`;}).join("");
  root.innerHTML=`<svg viewBox="0 0 ${width} ${height}" data-xmin="${xmin}" data-xmax="${xmax}"><rect x="${left}" y="${top}" width="${width-left-right}" height="${height-top-bottom}" fill="#fff" stroke="#ccd4de"/>${panels}<text x="${width/2}" y="${height-8}" text-anchor="middle" font-size="12">Time (min)</text><rect class="zoom-box" fill="rgba(40,120,208,.12)" stroke="#2878d0" hidden/></svg>`; bindChromInteractions(root.querySelector("svg"),{xmin,xmax});
}

function bindChromInteractions(svg,domain){let start=null,panning=false;svg.addEventListener("mousedown",e=>{const box=svg.getBoundingClientRect(),x=(e.clientX-box.left)/box.width*1000;start={x,clientX:e.clientX};panning=e.buttons===1&&window.__spaceDown;});svg.addEventListener("mousemove",e=>{if(!start)return;const box=svg.getBoundingClientRect(),x=(e.clientX-box.left)/box.width*1000;if(panning)return;const rect=svg.querySelector(".zoom-box");rect.hidden=false;rect.setAttribute("x",Math.min(start.x,x));rect.setAttribute("y",24);rect.setAttribute("width",Math.abs(x-start.x));rect.setAttribute("height",Number(svg.viewBox.baseVal.height)-62);});svg.addEventListener("mouseup",e=>{if(!start)return;const box=svg.getBoundingClientRect(),x=(e.clientX-box.left)/box.width*1000,span=domain.xmax-domain.xmin;if(panning){const shift=(start.clientX-e.clientX)/box.width*span;state.analysis.chrom.viewStack.push(domain);renderChromChart({xmin:domain.xmin+shift,xmax:domain.xmax+shift});}else if(Math.abs(x-start.x)>8){state.analysis.chrom.viewStack.push(domain);const a=domain.xmin+(Math.min(start.x,x)-64)/(1000-86)*span,b=domain.xmin+(Math.max(start.x,x)-64)/(1000-86)*span;renderChromChart({xmin:Math.max(domain.xmin,a),xmax:Math.min(domain.xmax,b)});}start=null;});svg.addEventListener("contextmenu",e=>{e.preventDefault();const previous=state.analysis.chrom.viewStack.pop();renderChromChart(previous||null);});}
window.addEventListener("keydown",e=>{if(e.code==="Space")window.__spaceDown=true;});window.addEventListener("keyup",e=>{if(e.code==="Space")window.__spaceDown=false;});
function renderPeakRows(){const traces=Object.fromEntries((state.analysis.chrom.plot?.traces||[]).map(t=>[t.key,t.label]));const peaks=state.analysis.chrom.plot?.peaks||[];document.querySelector("#peakRows").innerHTML=peaks.length?peaks.map(p=>`<tr><td>${escapeHtml(traces[p.trace_key]||p.trace_key)}</td><td>${p.peak_index}</td><td>${p.start_min.toFixed(4)}</td><td>${p.apex_min.toFixed(4)}</td><td>${p.end_min.toFixed(4)}</td><td>${displayValue(p.height)}</td><td>${displayValue(p.area)}</td><td>${p.width_s.toFixed(2)}</td></tr>`).join(""):`<tr><td colspan="8" class="empty">${state.analysis.chrom.plot?.integrated?"No peak met the integration settings.":"Plot ready. Click Integrate plotted traces when ready."}</td></tr>`;}

async function scanFormulas(){const model=state.analysis.formula;if(!model.artifactIds.size)return toast("Choose CMBX sources.");try{const job=await api("/api/formulas/scan",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({artifact_ids:[...model.artifactIds]})});const result=await waitForJob(job.id,j=>document.querySelector("#formulaProgress").textContent=`${j.progress_current}/${j.progress_total} · ${j.message}`);model.formulas=result.formulas||[];model.catalog=await api("/api/analysis/catalog",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({artifact_ids:[...model.artifactIds]}),timeoutMs:120000});renderFormulaList();renderFormulaInjections();document.querySelector("#formulaProgress").textContent=`${model.formulas.length} Direct CM formula(s).`;}catch(error){toast(error.message);}}
function renderFormulaList(){const q=document.querySelector("#formulaSearch").value.toLowerCase(),model=state.analysis.formula,rows=model.formulas.filter(f=>JSON.stringify(f).toLowerCase().includes(q));document.querySelector("#formulaList").innerHTML=rows.length?rows.map(f=>`<label class="formula-option"><input type="checkbox" data-formula-key="${escapeHtml(f.key)}" ${model.selected.has(f.key)?"checked":""}><span><b>${escapeHtml(f.formula)}</b><small>${escapeHtml(f.report)} / ${escapeHtml(f.sheet)} / ${escapeHtml(f.cell)} · ${escapeHtml(f.meaning)}</small></span></label>`).join(""):'<div class="empty-block">No matching formula.</div>';}
function renderFormulaInjections(){const model=state.analysis.formula,rows=model.catalog?.injections||[];document.querySelector("#formulaInjectionList").innerHTML=rows.length?rows.map(r=>`<label class="channel-option"><input type="checkbox" data-formula-injection="${escapeHtml(r.key)}" ${model.injections.has(r.key)?"checked":""}><span><b>${escapeHtml(r.injection)}</b><small>${escapeHtml(r.package)} / ${escapeHtml(r.sequence)}</small></span></label>`).join(""):'<div class="empty-block">No injection context.</div>';}
async function evaluateFormulas(){const model=state.analysis.formula,requested=model.formulas.filter(f=>model.selected.has(f.key));if(!requested.length)return toast("Choose formulas.");if(!model.injections.size)return toast("Choose injection contexts.");try{const job=await api("/api/formulas/evaluate",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({artifact_ids:[...model.artifactIds],injection_keys:[...model.injections],formulas:requested})});const result=await waitForJob(job.id);model.results=result.results||[];document.querySelector("#formulaResultRows").innerHTML=model.results.map(r=>`<tr><td>${escapeHtml(r.package)} / ${escapeHtml(r.sequence)} / ${escapeHtml(r.injection)}</td><td>${escapeHtml(r.formula)}</td><td>${escapeHtml(r.fixed_channel)}</td><td>${escapeHtml(displayValue(r.value))}</td><td>${escapeHtml(r.status)}</td><td>${escapeHtml(r.detail)}</td></tr>`).join("")||'<tr><td colspan="6" class="empty">No result.</td></tr>';}catch(error){toast(error.message);}}

function setReportStep(step,message=""){
  state.report.step=step;
  document.querySelectorAll("[data-report-step]").forEach(item=>{const value=Number(item.dataset.reportStep);item.classList.toggle("active",value===step);item.classList.toggle("complete",value<step);});
  document.querySelectorAll("[data-report-panel]").forEach(item=>item.classList.toggle("active",Number(item.dataset.reportPanel)===step));
  if(message)document.querySelector("#reportMessage").textContent=message;
}
function renderReportMethodBasis(){const root=document.querySelector("#reportMethodBasis");if(!root)return;const rows=[...state.report.methodBases.values()];root.innerHTML=rows.length?`<strong>${rows.length} selected Method MD file(s)</strong><span>${rows.map(item=>escapeHtml(item.original_name)).join(" · ")}</span>`:"No Method MD selected.";document.querySelector("#reportToDesign").disabled=!rows.length;}
function renderReportMethodChoices(){const root=document.querySelector("#reportMethodList");if(!root)return;root.innerHTML=state.report.methods.length?state.report.methods.map(item=>`<label class="selection-item"><input type="checkbox" data-report-method="${escapeHtml(item.id)}" ${state.report.methodBases.has(item.id)?"checked":""}><strong>${escapeHtml(item.original_name)}</strong><small>${escapeHtml(item.created_at||"")}</small></label>`).join(""):'<div class="empty-block">No Method MD is available. Generate and review Method MD files first.</div>';renderReportMethodBasis();}
async function uploadReportMethodBasis(file){const form=new FormData();form.append("file",file);try{const payload=await api("/api/artifacts/md-upload?kind=method_md",{method:"POST",body:form,timeoutMs:180000});state.report.methodBases.set(payload.artifact.id,payload.artifact);await refreshFileLibrary();await refreshReportConfig();renderReportMethodBasis();toast("Method MD added to My files and selected.");}catch(error){toast(error.message);}}
function continueMethodToReport(){
  if(state.method.mdArtifact)state.report.methodBases.set(state.method.mdArtifact.id,state.method.mdArtifact);
  state.report.modules=new Set(state.method.modules);
  document.querySelector("#reportIntent").value=document.querySelector("#methodIntent").value;
  showView("report"); setReportStep(1,"Step 1: confirm the Method MD that defines the report's runtime evidence.");
}
async function refreshReportConfig(){try{state.report.config=await api("/api/report/config");state.report.methods=await api("/api/artifacts?kind=method_md");state.method.aiSettings=await api("/api/account/ai-settings");if(!state.report.modules.size&&state.report.config.modules.includes("TCC"))state.report.modules.add("TCC");document.querySelector("#reportModuleList").innerHTML=state.report.config.modules.map(m=>`<label class="module-option"><input type="checkbox" data-report-module="${escapeHtml(m)}" ${state.report.modules.has(m)?"checked":""}><span>${escapeHtml(m)}</span></label>`).join("");document.querySelectorAll(".manual-report-only").forEach(item=>item.hidden=!state.report.config.manual_web_ai);const gpt=(state.method.aiSettings?.providers||[]).find(item=>item.provider==="gpt");const quota=state.method.aiSettings?.quota||state.report.config.quota||{};document.querySelector("#reportQuotaSummary").innerHTML=`<b>${escapeHtml(quota.remaining??0)} of ${escapeHtml(quota.limit??3)} automatic run(s) remaining today</b><span>${escapeHtml(quota.used??0)} used</span>`;document.querySelector("#reportApiSettingSummary").textContent=gpt?`GPT · ${gpt.model} · ${gpt.api_key_configured?"API key configured":"API key required"}`:"GPT setting unavailable";document.querySelector("#autoGenerateReport").disabled=!gpt?.api_key_configured||Number(quota.remaining||0)<1;renderReportMethodChoices();}catch(error){toast(error.message);}}
function reportLog(message){const el=document.querySelector("#reportLog");el.textContent=`[${new Date().toLocaleTimeString()}] ${message}\n${el.textContent==="Ready."?"":el.textContent}`.trim();}
async function buildReportPackage(){if(!state.report.modules.size)return toast("Choose modules.");if(!state.report.methodBases.size)return toast("Choose Method MD files.");try{const result=await api("/api/report/ai-package",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({modules:[...state.report.modules],request:document.querySelector("#reportIntent").value,small_context:document.querySelector("#reportSmallContext").checked,method_md_artifact_ids:[...state.report.methodBases.keys()]})});const link=document.querySelector("#downloadReportPackage");link.href=result.download_url;link.classList.remove("disabled-link");link.textContent="Download ZIP";reportLog(`AI package ready: ${result.files.length} file(s); ${result.method_bases?.length||0} Method MD contract(s) included.`);}catch(error){toast(error.message);}}
function renderReportPreflight(payload){state.report.artifact=payload.artifact;state.report.preflight=payload.preflight;const p=payload.preflight,s=p.summary||{};document.querySelector("#reportPreflight").classList.remove("empty-block");document.querySelector("#reportPreflight").innerHTML=`<strong>${p.ready?"Ready to generate":"Blocked"}</strong><p>${s.sheets||0} sheet(s), ${s.cm_formulas||0} CM formula(s), ${s.workbook_cells||0} workbook cell(s), ${s.dynamic_tables||0} dynamic table(s).</p>${[...(p.errors||[]),...(p.warnings||[])].map(x=>`<div>${escapeHtml(x)}</div>`).join("")}`;document.querySelector("#generateReport").disabled=!p.ready;document.querySelector("#reportReviewStatus").textContent=p.ready?"Report MD passed structural preflight.":"Resolve Report MD errors before compilation.";document.querySelector("#reportFinalAssetName").value=document.querySelector("#reportAssetName").value||payload.artifact?.original_name?.replace(/\.(md|markdown)$/i,"")||"Report Template";reportLog(`Preflight: ${(p.errors||[]).length} error(s), ${(p.warnings||[]).length} warning(s).`);}
async function uploadReportMd(file){const form=new FormData();form.append("file",file);try{renderReportPreflight(await api("/api/artifacts/md-upload?kind=report_md",{method:"POST",body:form,timeoutMs:180000}));setReportStep(4,"Step 4: review the imported Report MD and compile the candidate CMBX.");refreshFileLibrary();}catch(error){toast(error.message);}}
async function autoGenerateReport(){if(!state.report.methodBases.size)return toast("Choose at least one Method MD basis first.");if(!state.report.modules.size)return toast("Choose related modules.");const request=document.querySelector("#reportIntent").value.trim();if(!request)return toast("Describe the report requirement.");const button=document.querySelector("#autoGenerateReport");button.disabled=true;document.querySelector("#reportAiProgressBar").style.width="3%";document.querySelector("#reportAiRunStatus").textContent="Queuing Report MD generation...";try{const job=await api("/api/report/auto-generate",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({method_md_artifact_ids:[...state.report.methodBases.keys()],modules:[...state.report.modules],request,small_context:document.querySelector("#reportSmallContext").checked,asset_name:document.querySelector("#reportAssetName").value||"AI Report Template"})});const result=await waitForJob(job.id,current=>{const percent=Math.round(100*current.progress_current/Math.max(1,current.progress_total));document.querySelector("#reportAiProgressBar").style.width=`${percent}%`;document.querySelector("#reportAiRunStatus").textContent=current.message||current.stage;});renderReportPreflight({artifact:result.report_md_artifact,preflight:result.preflight});document.querySelector("#reportTargetVersion").value=document.querySelector("#reportOptionTargetVersion").value;document.querySelector("#reportAiResult").innerHTML=`<div class="generation-success"><span>Report MD generated from ${state.report.methodBases.size} selected Method MD file(s).</span>${document.querySelector("#reportKeepMd").checked?`<a class="secondary-button" href="${escapeHtml(result.report_md_download_url)}">Download Report MD</a>`:""}</div>`;setReportStep(4,"Step 4: review the generated Report MD and compile the candidate CMBX.");refreshFileLibrary();}catch(error){toast(error.message);reportLog(`Automatic Report generation failed: ${error.message}`);}finally{button.disabled=false;refreshReportConfig();}}
async function generateReport(){if(!state.report.artifact)return;try{const job=await api("/api/report/generate",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({artifact_id:state.report.artifact.id,asset_name:document.querySelector("#reportFinalAssetName").value||document.querySelector("#reportAssetName").value||"Report_Template",target_cm_version:document.querySelector("#reportTargetVersion").value,family:[...state.report.modules].join(" + "),intent:document.querySelector("#reportIntent").value})});const result=await waitForJob(job.id,j=>reportLog(j.message));document.querySelector("#reportGenerationResult").innerHTML=`<div class="generation-success"><span>Report template CMBX is ready.</span><a class="primary-button" href="${result.download_url}">Download CMBX</a></div>`;}catch(error){toast(error.message);}}

function setSequenceStep(step,message=""){
  state.sequence.step=step;
  document.querySelectorAll("[data-sequence-step]").forEach(item=>{const value=Number(item.dataset.sequenceStep);item.classList.toggle("active",value===step);item.classList.toggle("complete",value<step);});
  document.querySelectorAll("[data-sequence-panel]").forEach(item=>item.classList.toggle("active",Number(item.dataset.sequencePanel)===step));
  if(message)document.querySelector("#sequenceMessage").textContent=message;
}
function sequenceLog(message){const el=document.querySelector("#sequenceLog");el.textContent=`[${new Date().toLocaleTimeString()}] ${message}\n${el.textContent==="Ready."?"":el.textContent}`.trim();}
function renderSequenceAssets(){
  const methodRoot=document.querySelector("#sequenceMethodList"),reportRoot=document.querySelector("#sequenceReportList");
  methodRoot.innerHTML=state.sequence.methods.length?state.sequence.methods.map(item=>`<label class="selection-item"><input type="checkbox" data-sequence-method="${escapeHtml(item.id)}" ${state.sequence.selectedMethods.has(item.id)?"checked":""}><strong>${escapeHtml(item.original_name)}</strong><small>${escapeHtml(item.created_at||"")}</small></label>`).join(""):'<div class="empty-block">No Method MD is available.</div>';
  reportRoot.innerHTML=state.sequence.reports.length?state.sequence.reports.map(item=>`<label class="selection-item"><input type="radio" name="sequenceReport" data-sequence-report="${escapeHtml(item.id)}" ${state.sequence.report?.id===item.id?"checked":""}><strong>${escapeHtml(item.original_name)}</strong><small>${escapeHtml(item.created_at||"")}</small></label>`).join(""):'<div class="empty-block">No Report MD is available. Generate one shared report from the selected methods first.</div>';
  document.querySelector("#sequenceAssetStatus").textContent=`${state.sequence.selectedMethods.size} Method MD file(s) · ${state.sequence.report?"1 shared Report MD":"no Report MD"}`;
}
function sequenceAssetName(artifact){return artifact?.asset_name||artifact?.original_name?.replace(/\.(md|markdown)$/i,"")||"Unnamed asset";}
function newSequenceRow(artifact,index=0){return {id:`injection-${Date.now()}-${Math.random().toString(16).slice(2)}`,artifact_id:artifact.id,injection_name:`Injection ${index+1}`};}
function buildSequenceRows(){
  const available=new Set(state.sequence.selectedMethods.keys());
  state.sequence.rows=state.sequence.rows.filter(row=>available.has(row.artifact_id));
  if(!state.sequence.rows.length)state.sequence.rows=[...state.sequence.selectedMethods.values()].map((artifact,index)=>newSequenceRow(artifact,index));
  renderSequenceRows();
}
function addSequenceInjection(){
  const methods=[...state.sequence.selectedMethods.values()];
  if(!methods.length)return toast("Choose at least one Method MD first.");
  const limit=state.sequence.config?.max_injections||10;
  if(state.sequence.rows.length>=limit)return toast(`This carrier supports at most ${limit} Injections.`);
  state.sequence.rows.push(newSequenceRow(methods[0],state.sequence.rows.length));
  renderSequenceRows();
}
function renderSequenceRows(){
  const root=document.querySelector("#sequenceInjectionRows"),methods=[...state.sequence.selectedMethods.values()];
  root.innerHTML=state.sequence.rows.length?state.sequence.rows.map((row,index)=>{const artifact=state.sequence.selectedMethods.get(row.artifact_id)||methods[0];return `<tr><td>${index+1}</td><td><input data-sequence-injection-index="${index}" value="${escapeHtml(row.injection_name)}" aria-label="Injection name ${index+1}"></td><td><select data-sequence-row-method-index="${index}" aria-label="Assigned Method ${index+1}">${methods.map(item=>`<option value="${escapeHtml(item.id)}" ${item.id===row.artifact_id?"selected":""}>${escapeHtml(sequenceAssetName(item))}</option>`).join("")}</select></td><td><span class="sequence-source-name" title="${escapeHtml(artifact?.original_name||"")}">${escapeHtml(artifact?.original_name||"")}</span></td><td><button class="row-action" data-sequence-move="up" data-sequence-index="${index}" ${index===0?"disabled":""}>Up</button><button class="row-action" data-sequence-move="down" data-sequence-index="${index}" ${index===state.sequence.rows.length-1?"disabled":""}>Down</button><button class="row-action" data-sequence-remove="${index}">Remove</button></td></tr>`;}).join(""):'<tr><td colspan="5" class="empty">Add an Injection and assign a Method MD.</td></tr>';
  const reportIdentity=document.querySelector("#sequenceReportIdentity");if(reportIdentity)reportIdentity.textContent=state.sequence.report?sequenceAssetName(state.sequence.report):"Choose a Report MD";
  const status=document.querySelector("#sequenceInjectionStatus");if(status)status.textContent=`${state.sequence.rows.length} of ${state.sequence.config?.max_injections||10} Injection row(s).`;
  const add=document.querySelector("#sequenceAddInjection");if(add)add.disabled=!methods.length||state.sequence.rows.length>=(state.sequence.config?.max_injections||10);
}
function sequencePayload(){return {target_cm_version:document.querySelector("#sequenceTargetVersion").value,report_md_artifact_id:state.sequence.report?.id||"",injections:state.sequence.rows.map(row=>({method_md_artifact_id:row.artifact_id,injection_name:row.injection_name}))};}
async function refreshSequenceConfig(){
  try{state.sequence.config=await api("/api/sequence/config");state.sequence.methods=state.sequence.config.method_md||[];state.sequence.reports=state.sequence.config.report_md||[];const methodIds=new Set(state.sequence.methods.map(item=>item.id));state.sequence.selectedMethods=new Map([...state.sequence.selectedMethods].filter(([id])=>methodIds.has(id)).map(([id])=>[id,state.sequence.methods.find(item=>item.id===id)]));if(state.sequence.report)state.sequence.report=state.sequence.reports.find(item=>item.id===state.sequence.report.id)||null;const target=document.querySelector("#sequenceTargetVersion"),current=target.value;target.innerHTML=(state.sequence.config.target_versions||[]).map(value=>`<option value="${escapeHtml(value)}">${escapeHtml(value)}</option>`).join("");if((state.sequence.config.target_versions||[]).includes(current))target.value=current;renderSequenceAssets();renderSequenceRows();document.querySelector("#sequenceCarrierStatus").textContent=state.sequence.config.carrier_available?`Controlled TCC carrier available · ${(state.sequence.config.target_versions||[]).join(" / ")}`:"Controlled carrier is unavailable on this host";}catch(error){toast(error.message);}
}
async function uploadSequenceMethods(files){
  const chosen=[...files];if(!chosen.length)return;
  sequenceLog(`Uploading ${chosen.length} Method MD file(s)...`);
  for(const file of chosen){
    const form=new FormData();form.append("file",file);
    try{const payload=await api("/api/artifacts/md-upload?kind=method_md",{method:"POST",body:form,timeoutMs:180000});state.sequence.selectedMethods.set(payload.artifact.id,payload.artifact);sequenceLog(`Method MD ready: ${payload.artifact.original_name}`);}catch(error){sequenceLog(`Method MD upload failed (${file.name}): ${error.message}`);toast(error.message);}
  }
  await refreshSequenceConfig();await refreshFileLibrary();renderSequenceAssets();
}
async function uploadSequenceReport(file){
  if(!file)return;sequenceLog(`Uploading shared Report MD: ${file.name}`);
  const form=new FormData();form.append("file",file);
  try{const payload=await api("/api/artifacts/md-upload?kind=report_md",{method:"POST",body:form,timeoutMs:180000});state.sequence.report=payload.artifact;await refreshSequenceConfig();await refreshFileLibrary();renderSequenceAssets();sequenceLog(`Shared Report MD ready: ${payload.artifact.original_name}`);}catch(error){sequenceLog(`Report MD upload failed: ${error.message}`);toast(error.message);}
}
function continueSequenceAssets(){if(!state.sequence.selectedMethods.size)return toast("Choose at least one Method MD.");if(!state.sequence.report)return toast("Choose one shared Report MD.");buildSequenceRows();setSequenceStep(2,"Step 2: add Injection rows, edit Injection names, and assign reviewed Methods.");}
async function preflightSequence(){
  if(!state.sequence.rows.length)return toast("Add at least one Injection.");
  try{sequenceLog("Checking Method MD, Report MD, and sequence bindings...");const result=await api("/api/sequence/preflight",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(sequencePayload()),timeoutMs:180000});state.sequence.preflight=result;const items=[...result.methods.map(item=>`<div class="contract-row ${item.ready?"pass":"fail"}"><strong>${escapeHtml(item.injection)}</strong><span>${escapeHtml(item.method)}</span><b>${item.ready?"Ready":"Blocked"}</b>${[...(item.errors||[]),...(item.warnings||[])].map(value=>`<small>${escapeHtml(value)}</small>`).join("")}</div>`),`<div class="contract-row ${result.report.ready?"pass":"fail"}"><strong>Shared report</strong><span>${escapeHtml(result.report.name)}</span><b>${result.report.ready?"Ready":"Blocked"}</b>${[...(result.report.errors||[]),...(result.report.warnings||[])].map(value=>`<small>${escapeHtml(value)}</small>`).join("")}</div>`];document.querySelector("#sequencePreflight").innerHTML=items.join("")+result.warnings.map(value=>`<div class="sequence-warning">${escapeHtml(value)}</div>`).join("");document.querySelector("#generateSequence").disabled=!result.ready;setSequenceStep(3,result.ready?"Step 3: contracts are ready. Generate and runtime-check the candidate Sequence CMBX.":"Step 3: resolve the blocked Method or Report MD contract before generation.");sequenceLog(result.ready?"Preflight passed.":"Preflight blocked.");}catch(error){toast(error.message);sequenceLog(`Preflight failed: ${error.message}`);}
}
async function generateSequence(){
  const button=document.querySelector("#generateSequence");button.disabled=true;document.querySelector("#sequenceProgressBar").style.width="3%";
  try{const job=await api("/api/sequence/generate",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(sequencePayload()),timeoutMs:180000});const result=await waitForJob(job.id,current=>{const percent=Math.round(100*current.progress_current/Math.max(1,current.progress_total));document.querySelector("#sequenceProgressBar").style.width=`${percent}%`;document.querySelector("#sequenceRunStatus").textContent=current.message||current.stage;sequenceLog(current.message||current.stage);});document.querySelector("#sequenceGenerationResult").innerHTML=`<div class="generation-success"><span>${escapeHtml(result.sequence_name)} · ${result.injections.length} Injection(s) · Processing Method blank</span><a class="primary-button" href="${escapeHtml(result.download_url)}">Download Sequence CMBX</a></div>${(result.warnings||[]).map(value=>`<div class="sequence-warning">${escapeHtml(value)}</div>`).join("")}`;document.querySelector("#sequenceProgressBar").style.width="100%";document.querySelector("#sequenceRunStatus").textContent="Candidate Sequence CMBX is ready.";refreshFileLibrary();}catch(error){toast(error.message);sequenceLog(`Generation failed: ${error.message}`);button.disabled=false;}
}

async function refreshQualityConfig(){try{state.quality.config=await api("/api/quality/config");const sources=state.quality.config.sources||[];document.querySelector("#qualitySource").innerHTML=sources.map(s=>`<option value="${escapeHtml(s.id)}">${escapeHtml(s.label)}</option>`).join("");if(state.quality.config.default_source)document.querySelector("#qualitySource").value=state.quality.config.default_source;}catch(error){toast(error.message);}}
async function loadQualityTables(){try{const result=await api("/api/quality/catalog",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({source_id:document.querySelector("#qualitySource").value}),timeoutMs:60000});state.quality.catalog=result;document.querySelector("#qualityTable").innerHTML=result.tables.map(t=>`<option>${escapeHtml(t)}</option>`).join("");toast(`${result.tables.length} table(s) loaded.`);}catch(error){toast(error.message);}}
async function runQuality(){const table=document.querySelector("#qualityTable").value;if(!table)return toast("Load and choose a table.");try{const job=await api("/api/quality/query",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({source_id:document.querySelector("#qualitySource").value,table,metric:document.querySelector("#qualityMetric").value,filters:{model:document.querySelector("#qualityModel").value,date_from:document.querySelector("#qualityDateFrom").value,date_to:document.querySelector("#qualityDateTo").value},limit:5000})});const result=await waitForJob(job.id);state.quality.result=result;renderQuality(result);}catch(error){toast(error.message);}}
function renderQuality(r){document.querySelector("#qualityMetric").innerHTML='<option value="">Auto detect</option>'+r.numeric_metrics.map(m=>`<option ${m===r.metric?"selected":""}>${escapeHtml(m)}</option>`).join("");document.querySelector("#qualityModel").innerHTML='<option value="">All models</option>'+r.choices.models.map(m=>`<option>${escapeHtml(m)}</option>`).join("");const s=r.summary||{};document.querySelector("#qualitySummary").innerHTML=[["N",s.count||0],["Mean",displayValue(s.mean)],["SD",displayValue(s.stdev)],["UCL",displayValue(s.ucl)],["LCL",displayValue(s.lcl)]].map(([a,b])=>`<div class="metric"><b>${escapeHtml(b)}</b><span>${a}</span></div>`).join("");renderQualityChart(r);document.querySelector("#qualityHead").innerHTML='<tr>'+r.display_columns.map(c=>`<th>${escapeHtml(c)}</th>`).join("")+'</tr>';document.querySelector("#qualityRows").innerHTML=r.rows.map(row=>'<tr>'+r.display_columns.map(c=>`<td>${escapeHtml(displayValue(row[c]))}</td>`).join("")+'</tr>').join("")||'<tr><td class="empty">No rows match the filter.</td></tr>';}
function renderQualityChart(r){const root=document.querySelector("#qualityChart"),values=r.samples||[];if(!values.length){root.innerHTML='<div class="empty-block">No numeric samples.</div>';return;}const refs=[r.summary.lcl,r.summary.ucl,r.summary.mean].filter(Number.isFinite),all=values.concat(refs);let min=Math.min(...all),max=Math.max(...all);if(min===max){min--;max++;}const w=1000,h=300,l=55,t=20,b=35,y=v=>t+(max-v)/(max-min)*(h-t-b),x=i=>l+i/(Math.max(1,values.length-1))*(w-l-20);const lines=[[r.summary.ucl,"UCL","#b66a00"],[r.summary.mean,"Mean","#526273"],[r.summary.lcl,"LCL","#b66a00"]].filter(a=>Number.isFinite(a[0])).map(a=>`<line x1="${l}" y1="${y(a[0])}" x2="${w-20}" y2="${y(a[0])}" stroke="${a[2]}" stroke-dasharray="4 3"/><text x="${w-24}" y="${y(a[0])-5}" text-anchor="end" fill="${a[2]}">${a[1]} ${displayValue(a[0])}</text>`).join("");root.innerHTML=`<svg viewBox="0 0 ${w} ${h}">${lines}${values.map((v,i)=>`<circle cx="${x(i)}" cy="${y(v)}" r="2.5" fill="#8794a5"/>`).join("")}<text x="${l}" y="15" font-weight="700">${escapeHtml(r.metric)} · ${r.count} row(s)</text></svg>`;}

function setSingleStep(step,message=""){
  state.single.step=step;
  document.querySelectorAll("[data-single-step]").forEach(item=>{const value=Number(item.dataset.singleStep);item.classList.toggle("active",value===step);item.classList.toggle("complete",value<step);});
  document.querySelectorAll("[data-single-panel]").forEach(item=>item.classList.toggle("active",Number(item.dataset.singlePanel)===step));
  if(message)document.querySelector("#singleMessage").textContent=message;
  document.querySelector("#view-single").scrollIntoView({behavior:"smooth",block:"start"});
}
async function refreshSingleSources(){
  try{
    state.artifacts=await api("/api/artifacts?kind=cmbx_source");
    const available=new Set(state.artifacts.map(item=>item.id));state.single.artifactIds=new Set([...state.single.artifactIds].filter(id=>available.has(id)));
    document.querySelector("#singleSourceList").innerHTML=state.artifacts.length?state.artifacts.map(item=>`<label class="source-chip"><input type="checkbox" data-single-artifact="${item.id}" value="${item.id}" ${state.single.artifactIds.has(item.id)?"checked":""}><span><strong>${escapeHtml(item.original_name)}</strong><small>${formatBytes(item.size_bytes)} · ${escapeHtml(item.created_at)}</small></span></label>`).join(""):'<div class="empty-block">No CMBX file in your library. Add one from Home / My files first.</div>';
    renderSingleSourceStatus();
  }catch(error){toast(error.message);}
}
function renderSingleSourceStatus(){document.querySelector("#singleSourceStatus").textContent=`${state.single.artifactIds.size} CMBX file(s) selected.`;}
async function openLeakSensorAnalysis(){
  state.single.feature="leak_sensor_analysis";
  document.querySelector("#singleCatalog").hidden=true;
  document.querySelector("#leakSensorWorkflow").hidden=false;
  setSingleStep(1,"Step 1: choose one or more completed CMBX files from your personal library.");
  await refreshSingleSources();
}
function closeLeakSensorAnalysis(){
  state.single.feature="";
  document.querySelector("#singleCatalog").hidden=false;
  document.querySelector("#leakSensorWorkflow").hidden=true;
}
function renderSingleTraceRows(){
  const rows=state.single.catalog||[];
  document.querySelector("#singleTraceRows").innerHTML=rows.length?rows.map(row=>`<tr><td><input type="checkbox" data-single-trace="${escapeHtml(row.key)}" ${state.single.traceKeys.has(row.key)?"checked":""}></td><td><input type="checkbox" data-single-benchmark="${escapeHtml(row.key)}" ${state.single.benchmarkKeys.has(row.key)?"checked":""}></td><td>${escapeHtml(row.package)}</td><td>${escapeHtml(row.sequence)}</td><td>${escapeHtml(row.injection)}</td><td>${escapeHtml(row.channel)}</td><td>${escapeHtml(row.liquid||"not identified")}</td><td>${escapeHtml(row.temperature_c||"not identified")}</td></tr>`).join(""):'<tr><td colspan="8" class="empty">No LeakDiff raw channel was found in the selected CMBX files.</td></tr>';
  document.querySelector("#singleTraceStatus").textContent=`${rows.length} curve(s) found; ${state.single.traceKeys.size} selected; ${state.single.benchmarkKeys.size} benchmark(s).`;
}
async function loadSingleCatalog(){
  if(!state.single.artifactIds.size)return toast("Choose at least one CMBX source.");
  document.querySelector("#singleSourceStatus").textContent="Decoding LeakDiff channel inventory...";
  try{
    const result=await api("/api/single-verification/leak-sensor/catalog",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({artifact_ids:[...state.single.artifactIds]}),timeoutMs:180000});
    state.single.catalog=result.traces||[];
    const available=new Set(state.single.catalog.map(row=>row.key));
    state.single.traceKeys=new Set([...state.single.traceKeys].filter(key=>available.has(key)));
    state.single.benchmarkKeys=new Set([...state.single.benchmarkKeys].filter(key=>available.has(key)));
    if(!state.single.traceKeys.size)state.single.catalog.forEach(row=>state.single.traceKeys.add(row.key));
    renderSingleTraceRows();
    setSingleStep(2,`Step 2: ${state.single.catalog.length} LeakDiff curve(s) found. Choose analysis curves and optional benchmark curves.`);
  }catch(error){toast(error.message);renderSingleSourceStatus();}
}
async function runSingleVerification(){
  if(!state.single.traceKeys.size)return toast("Choose at least one LeakDiff curve to analyze.");
  setSingleStep(3,"Step 3: applying the established Leak Sensor Analyzer algorithm to decoded CMBX raw points.");
  const button=document.querySelector("#rerunSingleVerification");button.disabled=true;document.querySelector("#singleProgressBar").style.width="3%";document.querySelector("#singleRunStatus").textContent="Queued...";
  try{
    const job=await api("/api/single-verification/leak-sensor",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({artifact_ids:[...state.single.artifactIds],trace_keys:[...state.single.traceKeys],benchmark_keys:[...state.single.benchmarkKeys]})});
    const result=await waitForJob(job.id,current=>{const percent=Math.round(100*current.progress_current/Math.max(1,current.progress_total));document.querySelector("#singleProgressBar").style.width=`${percent}%`;document.querySelector("#singleRunStatus").textContent=`${percent}% · ${current.message}`;});
    state.single.result=result;renderSingleResults(result);document.querySelector("#singleRunStatus").textContent=`Complete · ${result.summary.total} curve(s) · ${result.algorithm||"Leak Sensor Analyzer"}`;
  }catch(error){toast(error.message);document.querySelector("#singleRunStatus").textContent=error.message;}finally{button.disabled=false;}
}
function renderSingleResults(result){
  const summary=result.summary||{};
  (result.rows||[]).forEach(row=>{if(Number.isFinite(Number(row.delta_diff)))row.delta_diff=Number(row.delta_diff).toFixed(0);});
  document.querySelector("#singleSummary").innerHTML=[["Curves",summary.total,""],["Benchmark",summary.benchmark,""],["Better",summary.better,"pass"],["Mixed",summary.mixed,""] ,["Worse",summary.worse,"fail"],["Unmatched",summary.unmatched,""]].map(([label,value,kind])=>`<div class="metric ${kind}"><b>${value||0}</b><span>${label}</span></div>`).join("");
  document.querySelector("#singleResultRows").innerHTML=(result.rows||[]).map(row=>`<tr><td><strong>${escapeHtml(row.package)}</strong><br><small>${escapeHtml(row.sequence)} / ${escapeHtml(row.injection)}</small></td><td>${escapeHtml(row.benchmark_ref||"not assigned")}</td><td>${escapeHtml(displayValue(row.diff_start))}</td><td>${escapeHtml(displayValue(row.diff_peak))}</td><td>${escapeHtml(displayValue(row.delta_diff))}</td><td>${escapeHtml(displayValue(row.t0))}</td><td>${escapeHtml(displayValue(row.t50))}</td><td>${escapeHtml(displayValue(row.t90))}</td><td>${escapeHtml(Number(row.response_t90).toFixed(2))}</td><td>${escapeHtml(displayValue(row.response_peak))}</td><td>${escapeHtml(displayValue(row.rise_slope))}</td><td class="spec-${row.evaluation==="BETTER"?"pass":row.evaluation==="WORSE"?"fail":"review"}">${escapeHtml(row.evaluation||"NO BENCHMARK")}</td></tr>`).join("")||'<tr><td colspan="12" class="empty">No LeakDiff curve result was returned.</td></tr>';
  renderSingleChart(result);
  renderSingleMetricChart(result);
  renderSingleT90Chart(result);
}
function selectedLeakChartRatio(){
  const ratio=Number(document.querySelector("#singleChartRatio")?.value||1.5);
  return Number.isFinite(ratio)&&ratio>0?ratio:1.5;
}
function selectedLeakChartFontPoints(){
  const points=Number(document.querySelector("#singleChartFontSize")?.value||9);
  return Number.isFinite(points)?Math.max(8,Math.min(16,points)):9;
}
function singleCurveSvg(curves,title){
  const allPoints=curves.flatMap(curve=>curve.points||[]);if(!allPoints.length)return '<div class="empty-block">No decoded points.</div>';
  let xmin=Math.min(...allPoints.map(p=>p[0])),xmax=Math.max(...allPoints.map(p=>p[0])),ymin=Math.min(...allPoints.map(p=>p[1])),ymax=Math.max(...allPoints.map(p=>p[1]));if(xmin===xmax)xmax=xmin+1;if(ymin===ymax)ymax=ymin+1;const ypad=(ymax-ymin)*.08;ymin-=ypad;ymax+=ypad;const w=920,h=Math.round(w/selectedLeakChartRatio()),l=62,r=20,t=34,b=44+Math.max(0,selectedLeakChartFontPoints()-9)*3,x=v=>l+(v-xmin)/(xmax-xmin)*(w-l-r),y=v=>t+(ymax-v)/(ymax-ymin)*(h-t-b),sampleColors=["#ed7d31","#d94841","#7a57ad","#07845f","#b16000"];
  let sampleIndex=0;const colorFor=curve=>curve.is_benchmark?"#2369c8":sampleColors[(sampleIndex++)%sampleColors.length];
  const colored=curves.map(curve=>({curve,color:colorFor(curve)}));
  const paths=colored.map(({curve,color})=>`<path d="${(curve.points||[]).map((p,i)=>`${i?"L":"M"}${x(p[0]).toFixed(2)},${y(p[1]).toFixed(2)}`).join(" ")}" fill="none" stroke="${color}" stroke-width="${curve.is_benchmark?3.4:2.4}" ${curve.is_benchmark?'stroke-dasharray="8 4"':""}/>`).join("");
  const markers=colored.flatMap(({curve,color})=>(curve.markers||[]).filter(m=>Number.isFinite(m.x)&&Number.isFinite(m.y)).map(m=>`<circle cx="${x(m.x)}" cy="${y(m.y)}" r="3.5" fill="#fff" stroke="${color}" stroke-width="2"/><text x="${x(m.x)+5}" y="${y(m.y)-6}" fill="#263746">${escapeHtml(m.label)}</text>`)).join("");
  const labels=colored.map(({curve,color},index)=>`<span><i style="background:${color}"></i>${curve.is_benchmark?"Benchmark ":""}${escapeHtml(curve.injection||curve.label)}</span>`).join("");
  return `<article class="leak-chart-panel"><div class="leak-chart-heading"><h4>${escapeHtml(title)}</h4><button class="chart-copy-button" data-copy-chart type="button">Copy chart</button></div><div class="leak-chart-legend">${labels}</div><svg class="excel-chart" viewBox="0 0 ${w} ${h}" role="img" aria-label="${escapeHtml(title)} LeakDiff curves"><line x1="${l}" y1="${t}" x2="${l}" y2="${h-b}" stroke="#9aa5b1"/><line x1="${l}" y1="${h-b}" x2="${w-r}" y2="${h-b}" stroke="#9aa5b1"/>${paths}${markers}<text x="${w-r}" y="${h-10}" text-anchor="end" fill="#536273">Time (min)</text></svg></article>`;
}
function renderSingleChart(result){
  const curves=result.curves||[],root=document.querySelector("#singleChart");if(!curves.length){root.innerHTML='<div class="empty-block">No decoded LeakDiff response curve was returned.</div>';return;}
  const mode=document.querySelector("#singleOverlayMode")?.value||"condition";let groups=[];
  if(mode==="overlay")groups=[["All selected curves",curves]];
  else if(mode==="separate")groups=curves.map(curve=>[`${curve.group_key} · ${curve.injection}`, [curve]]);
  else{const map=new Map();curves.forEach(curve=>{const key=curve.group_key||"Unidentified condition";if(!map.has(key))map.set(key,[]);map.get(key).push(curve);});groups=[...map.entries()];}
  root.innerHTML=`<div class="leak-chart-grid ${mode}">${groups.map(([title,items])=>singleCurveSvg(items,title)).join("")}</div>`;
}
function renderSingleMetricChart(result){
  renderLeakBarChart({rootId:"singleMetricChart",rows:result.group_summaries||[],benchmarkField:"benchmark_delta_mean",selectedField:"selected_delta_mean",ariaLabel:"Delta Diff benchmark comparison",benchmarkLabel:"ΔDiff [Benchmark mean]",selectedLabel:"ΔDiff [Selected mean]",empty:"No condition has numeric ΔDiff data.",decimals:0});
}
function renderSingleT90Chart(result){
  renderLeakBarChart({rootId:"singleT90Chart",rows:result.group_summaries||[],benchmarkField:"benchmark_t90_mean",selectedField:"selected_t90_mean",ariaLabel:"T90 benchmark comparison",benchmarkLabel:"T90 [Benchmark mean]",selectedLabel:"T90 [Selected mean]",empty:"No condition has a valid T90 result.",decimals:2});
}
function renderLeakBarChart({rootId,rows,benchmarkField,selectedField,ariaLabel,benchmarkLabel,selectedLabel,empty,decimals=null}){
  rows=rows.filter(row=>Number.isFinite(row[benchmarkField])||Number.isFinite(row[selectedField]));const root=document.querySelector(`#${rootId}`);if(!rows.length){root.innerHTML=`<div class="empty-block">${escapeHtml(empty)}</div>`;return;}
  const format=value=>decimals===null?displayValue(value):Number(value).toFixed(decimals),values=rows.flatMap(row=>[row[benchmarkField],row[selectedField]]).filter(Number.isFinite),max=Math.max(...values,Number.EPSILON)*1.12,w=Math.max(760,rows.length*145+90),h=Math.round(w/selectedLeakChartRatio()),l=58,r=20,t=30,b=90+Math.max(0,selectedLeakChartFontPoints()-9)*5,y=v=>t+(max-v)/max*(h-t-b),groupWidth=(w-l-r)/rows.length,barWidth=Math.min(32,groupWidth*.25);
  const grid=[0,.25,.5,.75,1].map(part=>{const value=max*part;return `<line x1="${l}" y1="${y(value)}" x2="${w-r}" y2="${y(value)}" stroke="#d9dee5"/><text x="${l-8}" y="${y(value)+4}" text-anchor="end" fill="#536273">${escapeHtml(format(value))}</text>`;}).join("");
  const bars=rows.map((row,index)=>{const center=l+groupWidth*(index+.5),benchmark=Number(row[benchmarkField]),selected=Number(row[selectedField]),benchmarkBar=Number.isFinite(benchmark)?`<rect x="${center-barWidth-3}" y="${y(benchmark)}" width="${barWidth}" height="${h-b-y(benchmark)}" fill="#5b9bd5"/><text x="${center-barWidth/2-3}" y="${y(benchmark)-7}" text-anchor="middle">${escapeHtml(format(benchmark))}</text>`:"",selectedBar=Number.isFinite(selected)?`<rect x="${center+3}" y="${y(selected)}" width="${barWidth}" height="${h-b-y(selected)}" fill="#ed7d31"/><text x="${center+barWidth/2+3}" y="${y(selected)-7}" text-anchor="middle">${escapeHtml(format(selected))}</text>`:"";return `${benchmarkBar}${selectedBar}<text x="${center}" y="${h-b+22}" text-anchor="middle" fill="#465363">${escapeHtml(row.group_key.replace(" | ","_"))}</text>`;}).join("");
  root.innerHTML=`<div class="leak-chart-heading"><span></span><button class="chart-copy-button" data-copy-chart type="button">Copy chart</button></div><svg class="excel-chart" viewBox="0 0 ${w} ${h}" role="img" aria-label="${escapeHtml(ariaLabel)}">${grid}<line x1="${l}" y1="${h-b}" x2="${w-r}" y2="${h-b}" stroke="#9aa5b1"/>${bars}<g transform="translate(${l},${h-28})"><rect width="12" height="12" fill="#5b9bd5"/><text x="18" y="11">${escapeHtml(benchmarkLabel)}</text><rect x="210" width="12" height="12" fill="#ed7d31"/><text x="228" y="11">${escapeHtml(selectedLabel)}</text></g></svg>`;
}

function leakChartPng(svg){
  const viewBox=(svg.getAttribute("viewBox")||"0 0 920 600").split(/\s+/).map(Number),width=Math.max(1,Math.round(viewBox[2]||920)),height=Math.max(1,Math.round(viewBox[3]||600));
  const clone=svg.cloneNode(true),computed=getComputedStyle(svg);clone.setAttribute("xmlns","http://www.w3.org/2000/svg");clone.setAttribute("width",String(width));clone.setAttribute("height",String(height));clone.style.fontFamily="Aptos, Calibri, sans-serif";clone.style.fontSize=computed.fontSize||"12px";clone.style.background="#fff";
  const source=new XMLSerializer().serializeToString(clone),url=URL.createObjectURL(new Blob([source],{type:"image/svg+xml;charset=utf-8"}));
  return new Promise((resolve,reject)=>{const image=new Image();image.onload=()=>{try{const canvas=document.createElement("canvas");canvas.width=width;canvas.height=height;const context=canvas.getContext("2d");context.fillStyle="#fff";context.fillRect(0,0,width,height);context.drawImage(image,0,0,width,height);canvas.toBlob(blob=>blob?resolve({blob,canvas}):reject(new Error("PNG conversion failed")),"image/png");}catch(error){reject(error);}finally{URL.revokeObjectURL(url);}};image.onerror=()=>{URL.revokeObjectURL(url);reject(new Error("SVG rendering failed"));};image.src=url;});
}
function legacyCopyChart(canvas){
  const dataUrl=canvas.toDataURL("image/png"),onCopy=event=>{event.clipboardData.setData("text/html",`<img src="${dataUrl}">`);event.preventDefault();};document.addEventListener("copy",onCopy);const copied=document.execCommand("copy");document.removeEventListener("copy",onCopy);return copied;
}
async function copyLeakChart(button){
  const scope=button.closest(".leak-chart-panel,.single-metric-chart"),svg=scope?.querySelector("svg");
  if(!svg)return toast("Chart not found.");
  const pngPromise=leakChartPng(svg);
  try{
    if(navigator.clipboard&&window.ClipboardItem){await navigator.clipboard.write([new ClipboardItem({"image/png":pngPromise.then(result=>result.blob)})]);}
    else{const result=await pngPromise;if(!legacyCopyChart(result.canvas))throw new Error("Clipboard image API unavailable");}
    button.textContent="Copied";setTimeout(()=>button.textContent="Copy chart",1400);
  }catch(error){try{const result=await pngPromise;if(!legacyCopyChart(result.canvas))throw error;button.textContent="Copied";setTimeout(()=>button.textContent="Copy chart",1400);}catch(fallbackError){toast(`Could not copy chart: ${fallbackError.message}`);}}
}

document.addEventListener("click", event => {
  const copyChart=event.target.closest("[data-copy-chart]");if(copyChart){copyLeakChart(copyChart);return;}
  const branch = event.target.closest("[data-branch]")?.dataset.branch; if (branch) { showBranch(branch); return; }
  const view = event.target.closest("[data-view]")?.dataset.view; if (view) showView(view);
  const scan = event.target.closest("[data-scan]")?.dataset.scan; if (scan) scanArtifact(scan);
  const open = event.target.closest("[data-open]")?.dataset.open; if (open) openInventory(open);
  const libraryKind=event.target.closest("[data-library-kind]")?.dataset.libraryKind;if(libraryKind){state.library.active=libraryKind;renderFileLibrary();return;}
  const deleteArtifact=event.target.closest("[data-delete-artifact]")?.dataset.deleteArtifact;if(deleteArtifact){deleteLibraryArtifact(deleteArtifact);return;}
  const useMethod=event.target.closest("[data-use-method]")?.dataset.useMethod;if(useMethod){useManagedMd(useMethod,"method");return;}
  const useReportBasis=event.target.closest("[data-use-report-basis]")?.dataset.useReportBasis;if(useReportBasis){useManagedMd(useReportBasis,"report-basis");return;}
  const useReport=event.target.closest("[data-use-report]")?.dataset.useReport;if(useReport){useManagedMd(useReport,"report");return;}
  const back = event.target.closest("[data-foq-back]")?.dataset.foqBack; if (back) setFoqStep(Number(back));
  const methodBack = event.target.closest("[data-method-back]")?.dataset.methodBack; if (methodBack) setMethodStep(Number(methodBack));
  const sequenceBack=event.target.closest("[data-sequence-back]")?.dataset.sequenceBack;if(sequenceBack){setSequenceStep(Number(sequenceBack));return;}
  const sequenceMove=event.target.closest("[data-sequence-move]");if(sequenceMove){const index=Number(sequenceMove.dataset.sequenceIndex),target=sequenceMove.dataset.sequenceMove==="up"?index-1:index+1;if(target>=0&&target<state.sequence.rows.length){[state.sequence.rows[index],state.sequence.rows[target]]=[state.sequence.rows[target],state.sequence.rows[index]];renderSequenceRows();}return;}
  const sequenceRemove=event.target.closest("[data-sequence-remove]")?.dataset.sequenceRemove;if(sequenceRemove!==undefined){state.sequence.rows.splice(Number(sequenceRemove),1);renderSequenceRows();return;}
  const singleBack=event.target.closest("[data-single-back]")?.dataset.singleBack;if(singleBack){setSingleStep(Number(singleBack));return;}
  if(event.target.closest("#openLeakSensorAnalysis")){openLeakSensorAnalysis();return;}
  if(event.target.closest("#backToSingleCatalog")){closeLeakSensorAnalysis();return;}
  const accessButton = event.target.closest("[data-access-decision]"); if (accessButton) decideAccessRequest(accessButton.dataset.accessId, accessButton.dataset.accessDecision);
  const developerButton = event.target.closest("[data-developer-email]"); if (developerButton) openDeveloperAccount(developerButton.dataset.developerEmail);
  if(event.target.closest("#rawLoadCatalog")){loadAnalysisCatalog("raw");return;}
  if(event.target.closest("#rawReview")){reviewRawSelection();return;}
  const rawBack=event.target.closest("[data-raw-back]")?.dataset.rawBack;if(rawBack){setAnalysisStep("raw",Number(rawBack));return;}
  if(event.target.closest("#chromLoadCatalog")){loadAnalysisCatalog("chrom");return;}
  const chromBack=event.target.closest("[data-chrom-back]")?.dataset.chromBack;if(chromBack){setAnalysisStep("chrom",Number(chromBack));return;}
  const selectVisible=event.target.closest("[data-select-visible]")?.dataset.selectVisible;if(selectVisible){visibleChannels(selectVisible).forEach(r=>state.analysis[selectVisible].selected.add(r.key));renderChannelPicker(selectVisible);}
  const clearChannels=event.target.closest("[data-clear-channels]")?.dataset.clearChannels;if(clearChannels){state.analysis[clearChannels].selected.clear();renderChannelPicker(clearChannels);}
});
document.addEventListener("change",async event=>{
  const singleArtifact=event.target.dataset.singleArtifact;if(singleArtifact){event.target.checked?state.single.artifactIds.add(singleArtifact):state.single.artifactIds.delete(singleArtifact);renderSingleSourceStatus();return;}
  const singleTrace=event.target.dataset.singleTrace;if(singleTrace){event.target.checked?state.single.traceKeys.add(singleTrace):state.single.traceKeys.delete(singleTrace);if(!event.target.checked)state.single.benchmarkKeys.delete(singleTrace);renderSingleTraceRows();return;}
  const singleBenchmark=event.target.dataset.singleBenchmark;if(singleBenchmark){if(event.target.checked){state.single.benchmarkKeys.add(singleBenchmark);state.single.traceKeys.add(singleBenchmark);}else state.single.benchmarkKeys.delete(singleBenchmark);renderSingleTraceRows();return;}
  const artifactKind=event.target.dataset.analysisArtifact;if(artifactKind){event.target.checked?state.analysis[artifactKind].artifactIds.add(event.target.value):state.analysis[artifactKind].artifactIds.delete(event.target.value);return;}
  const channelKind=event.target.dataset.analysisChannel;if(channelKind){event.target.checked?state.analysis[channelKind].selected.add(event.target.value):state.analysis[channelKind].selected.delete(event.target.value);renderChannelPicker(channelKind);return;}
  const filterKey=event.target.dataset.filter;if(filterKey){const kind=event.target.closest("#view-raw")?"raw":event.target.closest("#view-chrom")?"chrom":"";if(kind){state.analysis[kind].filters[filterKey]=event.target.value;populateAnalysisFilters(kind,filterKey);renderChannelPicker(kind);}return;}
  const uploadKind=event.target.dataset.analysisUpload;if(uploadKind){await uploadFiles([...event.target.files]);renderAnalysisSources(uploadKind);return;}
  const formulaKey=event.target.dataset.formulaKey;if(formulaKey){event.target.checked?state.analysis.formula.selected.add(formulaKey):state.analysis.formula.selected.delete(formulaKey);return;}
  const injectionKey=event.target.dataset.formulaInjection;if(injectionKey){event.target.checked?state.analysis.formula.injections.add(injectionKey):state.analysis.formula.injections.delete(injectionKey);return;}
  const reportModule=event.target.dataset.reportModule;if(reportModule){event.target.checked?state.report.modules.add(reportModule):state.report.modules.delete(reportModule);return;}
  const reportMethod=event.target.dataset.reportMethod;if(reportMethod){const item=state.report.methods.find(row=>row.id===reportMethod);if(event.target.checked&&item)state.report.methodBases.set(reportMethod,item);else state.report.methodBases.delete(reportMethod);renderReportMethodBasis();return;}
  const sequenceMethod=event.target.dataset.sequenceMethod;if(sequenceMethod){const item=state.sequence.methods.find(row=>row.id===sequenceMethod);if(event.target.checked&&item)state.sequence.selectedMethods.set(sequenceMethod,item);else state.sequence.selectedMethods.delete(sequenceMethod);renderSequenceAssets();return;}
  const sequenceReport=event.target.dataset.sequenceReport;if(sequenceReport){state.sequence.report=state.sequence.reports.find(row=>row.id===sequenceReport)||null;renderSequenceAssets();renderSequenceRows();return;}
  const sequenceRowMethod=event.target.dataset.sequenceRowMethodIndex;if(sequenceRowMethod!==undefined&&state.sequence.rows[Number(sequenceRowMethod)]){state.sequence.rows[Number(sequenceRowMethod)].artifact_id=event.target.value;renderSequenceRows();return;}
});
document.addEventListener("input",event=>{
  const injectionIndex=event.target.dataset.sequenceInjectionIndex;if(injectionIndex!==undefined&&state.sequence.rows[Number(injectionIndex)])state.sequence.rows[Number(injectionIndex)].injection_name=event.target.value;
});
document.querySelector("#developerLogin").addEventListener("click", developerLogin);
document.querySelector("#developerPassword").addEventListener("keydown", event => { if (event.key === "Enter") developerLogin(); });
document.querySelector("#logoutButton").addEventListener("click", logout);
document.querySelector("#newDeveloperAccount").addEventListener("click", () => openDeveloperAccount());
document.querySelector("#saveDeveloperAccount").addEventListener("click", saveDeveloperAccount);
document.querySelector("#methodRoutePicker").addEventListener("change", event => { if (!event.target.name || event.target.name !== "methodRoute") return; state.method.route = event.target.value; renderMethodRoute(); });
document.querySelector("#methodModuleList").addEventListener("change", event => {
  const module = event.target.dataset.methodModule;
  if (!module) return;
  event.target.checked ? state.method.modules.add(module) : state.method.modules.delete(module);
  renderMethodModules();
});
document.querySelector("#buildMethodPackage").addEventListener("click", buildMethodPackage);
document.querySelector("#openAiSettings").addEventListener("click", openAiSettings);
document.querySelector("#aiSettingsProvider").addEventListener("change", syncAiSettingsProvider);
document.querySelector("#saveAiSettings").addEventListener("click", saveAiSettings);
document.querySelector("#requestMethodQuota").addEventListener("click", requestMethodQuota);
document.querySelector("#autoGenerateMethod").addEventListener("click", autoGenerateMethod);
document.querySelector("#methodToIntent").addEventListener("click", () => {if(!state.method.modules.size)return toast("Choose at least one module.");setMethodStep(2,"Step 2: describe the required test in natural language.");});
document.querySelector("#methodToOptions").addEventListener("click", () => {if(!document.querySelector("#methodIntent").value.trim())return toast("Describe the test requirement.");setMethodStep(3,"Step 3: choose generation options and create the Method MD preview.");});
document.querySelector("#methodMdFile").addEventListener("change", event => { const file = event.target.files?.[0]; if (file) uploadMethodMd(file); });
document.querySelector("#generateMethod").addEventListener("click", generateMethod);
document.querySelector("#refreshFileLibrary").addEventListener("click",refreshFileLibrary);
document.querySelector("#homeFileUpload").addEventListener("change",event=>uploadHomeFiles([...event.target.files]));
document.querySelector("#cmbxFiles").addEventListener("change", event => uploadFiles([...event.target.files]));
document.querySelector("#refreshArtifacts").addEventListener("click", refreshArtifacts);
document.querySelector("#foqFiles").addEventListener("change", async event => { await uploadFiles([...event.target.files]); state.foq.artifactIds = new Set(state.artifacts.slice(0, event.target.files.length).map(item => item.id)); refreshFoqArtifacts(); });
document.querySelector("#foqArtifactList").addEventListener("change", event => { const id=event.target.dataset.foqArtifact; if (!id) return; event.target.checked ? state.foq.artifactIds.add(id) : state.foq.artifactIds.delete(id); });
document.querySelector("#inspectFoq").addEventListener("click", inspectFoqScope);
document.querySelector("#foqScopeRows").addEventListener("change", async event => {
  const sequenceKey=event.target.dataset.foqSequence;
  if (sequenceKey) { event.target.checked ? state.foq.sequenceKeys.add(sequenceKey) : state.foq.sequenceKeys.delete(sequenceKey); renderFoqScope(); return; }
  const injectionId=event.target.dataset.foqInjection; const parentKey=event.target.dataset.sequenceKey;
  if (!injectionId || !parentKey) return;
  const selected=state.foq.injections[parentKey] ||= new Set();
  const sequence=state.foq.scope.sequences.find(item => item.key===parentKey); const injection=sequence?.injections.find(item => item.id===injectionId);
  if (event.target.type==="radio" && injection) sequence.injections.filter(item => item.name.toLowerCase()===injection.name.toLowerCase()).forEach(item => selected.delete(item.id));
  event.target.checked ? selected.add(injectionId) : selected.delete(injectionId); renderFoqScope();
});
document.querySelector("#confirmFoqScope").addEventListener("click", async () => {
  await refreshFoqMetrics();
  const models=[...new Set(state.foq.scope.sequences.filter(item => state.foq.sequenceKeys.has(item.key)).map(item => item.device))];
  document.querySelector("#foqDbModels").value=models.join(",");
  setFoqStep(2,"Step 2: choose the mapped numeric results required for this review.");
});
document.querySelector("#foqMetricSearch").addEventListener("input", renderFoqMetrics);
document.querySelector("#foqMetricList").addEventListener("change", event => { const metric=event.target.dataset.foqMetric; if (!metric) return; event.target.checked ? state.foq.selectedMetrics.add(metric) : state.foq.selectedMetrics.delete(metric); renderFoqMetrics(); });
document.querySelector("#selectAllMetrics").addEventListener("click", () => { state.foq.selectedMetrics=new Set(state.foq.metrics); renderFoqMetrics(); });
document.querySelector("#clearAllMetrics").addEventListener("click", () => { state.foq.selectedMetrics.clear(); renderFoqMetrics(); });
document.querySelector("#loadMetricPreset").addEventListener("click", () => { const name=document.querySelector("#foqMetricPreset").value; const fields=metricPresets()[name] || []; state.foq.selectedMetrics=new Set(fields.filter(field => state.foq.metrics.includes(field))); renderFoqMetrics(); });
document.querySelector("#saveMetricPreset").addEventListener("click", () => { const name=prompt("Metric set name:"); if (!name?.trim()) return; const presets=metricPresets(); presets[name.trim()]=[...state.foq.selectedMetrics].sort(); localStorage.setItem("cmbx.foq.metricPresets",JSON.stringify(presets)); refreshMetricPresetList(); document.querySelector("#foqMetricPreset").value=name.trim(); toast(`Saved metric set: ${name.trim()}`); });
document.querySelector("#confirmFoqMetrics").addEventListener("click", () => setFoqStep(3,"Step 3: keep SPEC-only mode, or enable the configured historical database comparison."));
document.querySelector("#foqUseHistory").addEventListener("change", event => { const database=state.foq.config?.database || {}; document.querySelector("#foqDbStatus").textContent=event.target.checked ? (database.configured ? "History will load in the background when Run check starts." : "Historical database is not configured on this host; disable history to continue with SPEC only.") : "Database history is disabled; the check will use report/Definitions SPEC only."; });
document.querySelector("#foqDbSource").addEventListener("change", event => {
  const database = state.foq.config?.database || {};
  const source = (database.sources || []).find(item => item.id === event.target.value);
  if (!source) return;
  document.querySelector("#foqDbTable").value = source.table || "AUTO";
  document.querySelector("#foqDbStatus").textContent = `${source.label}: ${source.source}${source.database ? ` / ${source.database}` : ""}. Credentials are stored with Windows DPAPI.`;
});
document.querySelector("#confirmFoqHistory").addEventListener("click", () => { if (document.querySelector("#foqUseHistory").checked && !state.foq.config?.database?.configured) { toast("Historical database is not configured. Disable history or ask the administrator to configure it."); return; } setFoqStep(4,"Step 4: run the mapped calculation and review SPEC/history evidence."); });
document.querySelector("#runFoqCheck").addEventListener("click", runFoqCheck);
document.querySelector("#foqChartMetric").addEventListener("change", event => renderFoqChart(event.target.value));
document.querySelector("#foqOutputLayout").addEventListener("change", renderFoqOutput);
document.querySelector("#copyFoqOutput").addEventListener("click", copyFoqOutput);
document.querySelector("#downloadFoqOutput").addEventListener("click", downloadFoqOutput);
document.querySelector("#refreshAdminAccess").addEventListener("click", refreshAdmin);
document.querySelector("#exportRaw").addEventListener("click",exportRawData);
document.querySelector("#plotChrom").addEventListener("click",plotChromatograms);
document.querySelector("#integrateChrom").addEventListener("click",integrateChromatograms);
document.querySelector("#chromLayout").addEventListener("change",()=>renderChromChart());
document.querySelector("#scanFormulas").addEventListener("click",scanFormulas);
document.querySelector("#formulaSearch").addEventListener("input",renderFormulaList);
document.querySelector("#formulaList").addEventListener("change",()=>{});
document.querySelector("#evaluateFormulas").addEventListener("click",evaluateFormulas);
document.querySelector("#buildReportPackage").addEventListener("click",buildReportPackage);
document.querySelector("#reportMdFile").addEventListener("change",event=>{const file=event.target.files?.[0];if(file)uploadReportMd(file);});
document.querySelector("#reportMethodMdFile").addEventListener("change",event=>{const file=event.target.files?.[0];if(file)uploadReportMethodBasis(file);});
document.querySelector("#reportToDesign").addEventListener("click",()=>setReportStep(2,"Step 2: choose related modules and let the backend AI generate the matching Report MD."));
document.querySelector("#reportToOptions").addEventListener("click",()=>{if(!state.report.modules.size)return toast("Choose related modules.");if(!document.querySelector("#reportIntent").value.trim())return toast("Describe the report requirement.");setReportStep(3,"Step 3: choose output options and generate the Report MD preview.");});
document.querySelector("#autoGenerateReport").addEventListener("click",autoGenerateReport);
document.querySelector("#openReportAiSettings").addEventListener("click",()=>{openAiSettings();document.querySelector("#aiSettingsProvider").value="gpt";syncAiSettingsProvider();});
document.querySelectorAll("[data-report-back]").forEach(button=>button.addEventListener("click",()=>setReportStep(Number(button.dataset.reportBack))));
document.querySelector("#generateReport").addEventListener("click",generateReport);
document.querySelector("#sequenceToArrange").addEventListener("click",continueSequenceAssets);
document.querySelector("#sequenceToReview").addEventListener("click",preflightSequence);
document.querySelector("#sequenceAddInjection").addEventListener("click",addSequenceInjection);
document.querySelector("#generateSequence").addEventListener("click",generateSequence);
document.querySelector("#sequenceRefreshAssets").addEventListener("click",refreshSequenceConfig);
document.querySelector("#sequenceUploadMethods").addEventListener("click",()=>document.querySelector("#sequenceMethodFiles").click());
document.querySelector("#sequenceMethodFiles").addEventListener("change",async event=>{await uploadSequenceMethods(event.target.files||[]);event.target.value="";});
document.querySelector("#sequenceUploadReport").addEventListener("click",()=>document.querySelector("#sequenceReportFile").click());
document.querySelector("#sequenceReportFile").addEventListener("change",async event=>{await uploadSequenceReport(event.target.files?.[0]);event.target.value="";});
document.querySelector("#sequenceGenerateReport").addEventListener("click",()=>{state.report.methodBases=new Map(state.sequence.selectedMethods);showView("report");setReportStep(1,"All Sequence Method MD files are selected. Generate one shared Report MD, then return to Sequence Generation.");});
document.querySelector("#qualityConnect").addEventListener("click",loadQualityTables);
document.querySelector("#qualityRun").addEventListener("click",runQuality);
document.querySelector("#qualityMetric").addEventListener("change",runQuality);
document.querySelector("#refreshSingleSources").addEventListener("click",refreshSingleSources);
document.querySelector("#singleToBenchmark").addEventListener("click",loadSingleCatalog);
document.querySelector("#runSingleVerification").addEventListener("click",runSingleVerification);
document.querySelector("#rerunSingleVerification").addEventListener("click",runSingleVerification);
document.querySelector("#singleOverlayMode").addEventListener("change",()=>{if(state.single.result)renderSingleChart(state.single.result);});
document.querySelector("#singleChartFontSize").addEventListener("change",event=>{
  const points=Math.max(8,Math.min(16,Number(event.target.value)||9));
  document.querySelector("#leakSensorWorkflow").style.setProperty("--leak-chart-font-size",`${points*4/3}px`);
});
document.querySelector("#singleChartRatio").addEventListener("change",()=>{
  if(state.single.result){renderSingleChart(state.single.result);renderSingleMetricChart(state.single.result);renderSingleT90Chart(state.single.result);}
});

initializeAuthentication();
