# Sequence Package Generation

## Objective

Build one candidate Chromeleon sequence CMBX from controlled inputs:

1. a CM-exported, multi-slot sequence carrier;
2. one or more reviewed Method MD files compiled to standalone Instrument Method CMBX components;
3. one reviewed Report MD compiled to a standalone Report Template CMBX component.

The Web workflow exposes one Sequence with one Injection per selected Method MD and
one Report Template shared by the complete Sequence. Processing Method is intentionally
blank in the first version.

## Why A Carrier Is Required

An Instrument Method CMBX and a Report Template CMBX do not contain the complete
Chromeleon sequence DataContract. A runnable sequence also needs serialized object
identity, Injection bindings, Processing Method references, sequence metadata, and
CM-version-specific fields. These are retained from a real CM-exported carrier.

The first implementation therefore does not invent a sequence object from empty
bytes and does not concatenate ZIP entries. It edits a known-good serialized graph.

## Implemented Web Flow

```text
Step 1: Choose assets
  -> select multiple owned Method MD files
  -> select one owned shared Report MD
  -> optionally send all selected Method MD files to Report Generation
Step 2: Arrange injections
  -> one Injection row per Method MD
  -> edit Injection and Instrument Method names
  -> reorder or remove rows
Step 3: Review and generate
  -> preflight every Method MD and the Report MD
  -> compile standalone component CMBX files
  -> replace controlled carrier Method/Report CpXm bodies
  -> remove visible Processing Method bindings
  -> reopen output and validate Injection-to-Method and shared-report bindings
  -> compare embedded component payloads with their sources
```

The Web APIs are `/api/sequence/config`, `/api/sequence/preflight`, and
`/api/sequence/generate`. Access is controlled by the independent
`sequence_generate` permission.

## Command-Line Use

```powershell
python tools\build_sequence_package.py `
  <carrier.cmbx> `
  <method.cmbx> `
  <report.cmbx> `
  <output.cmbx> `
  --sequence-name "Generated Sequence" `
  --injection-name "Test Injection" `
  --method-name "GENERATED_METHOD" `
  --report-name "GENERATED_REPORT"
```

Core implementation:

- `sequence_package_builder.py`
- `tools/build_sequence_package.py`
- `tests/test_sequence_package_builder.py`

## Verified Local Probes

The builder was exercised with a selected TCC HeatUp/CoolDown sequence carrier,
the standalone `TEMP_HEAT_UP_DOWN_20_50_20` method, and a standalone generated
TCC report. The generated package passed these checks:

- sequence and injection names reopened correctly;
- Injection resolved to the renamed Instrument Method;
- Processing Method resolved to `No_Integration`;
- Method CpXm matched the standalone source byte-for-byte;
- Report CpXm matched the standalone source byte-for-byte.

One Method MD/CMBX may be assigned to multiple Injection rows. Sequence generation
creates separate Injection instances that reference one packaged Instrument Method
object when both the source CpXm and requested Method name are identical. The shared
Report Template is also packaged once. This mirrors native Chromeleon sequences and is
not a report contract error.

Standalone Report commands may contain metadata after their length-delimited CpXm
field. The extractor must use the protobuf field boundary; slicing from the `CpXm`
marker to end-of-file corrupts the payload and causes a false sequence validation
failure.

The controlled TCC Sequence command contains parallel field-18 type descriptors,
field-19 object values, and field-20 object metadata. A reduced Sequence must prune all
three arrays with the same mask. Removing objects only from `header.xml`, or pruning only
two arrays, leaves an invalid DataContract that the local parser may reopen while
Chromeleon rejects it during import. Multi-Injection generation now validates the three
array lengths and exact remaining object counts. Repeated Injection names are rewritten
one object at a time using their native Method binding; global name replacement is
forbidden. The Sequence URL and every child URL are also rewritten to the new Sequence
name so import does not target the carrier's original `.seq` name.

CM runtime testing showed that structural pruning of a completed FOQ Sequence is still
not a reliable carrier strategy because the command retains completed-run transaction
history and presentation objects. The production Web workflow therefore uses
`assets/sequence_carrier_native_test1.cmbx`, a CM-exported empty two-Injection Sequence
created by the user. Its native contract contains exactly one Sequence, two blank
Injection rows, one shared Instrument Method, and one Report Template, with no Signal,
Audit, Processing Method, or presentation-layout objects. Generation replaces only the
Method/Report CpXm bodies and names while preserving that CM-authored object graph.

Candidate output:

`outputs/sequence_package_probe/TCC_sequence_heatup_candidate.cmbx`

The multi-Injection writer was also exercised with two independently named Injection
rows. Both Injection-to-Method links reopened correctly, both embedded Method payloads
matched their standalone inputs, the shared Report payload matched, and the visible
Processing Method collection was empty.

## Current Boundaries

| Area | Current status |
|---|---|
| Instrument Method insertion | Implemented and payload-verified |
| Report Template insertion | Implemented and payload-verified |
| Injection-to-Method binding | Rewritten and parser-verified |
| Multiple Method MD inputs | Implemented; selected files form a Method asset pool |
| Custom Injection plan | Implemented; rows can be added, removed, reordered, and assigned to any selected Method |
| Editable names | Injection name only; Method/Report names are inherited and Sequence name is automatic |
| Shared Report MD | Implemented; Report Generation accepts the full Method MD collection |
| Processing Method | Intentionally blank; no IRC/integration/pass action |
| Injection sample fields | Preserved from carrier |
| Sequence variables | Preserved from carrier |
| Acquired raw/audit data | Removed from the visible selected Injection header |
| Hidden carrier objects | Detected and reported, not removed yet |
| CM version | Controlled carrier is currently a CM 7.3 candidate |
| CM runtime approval | Requires import/open/run verification in target CM configuration |
| Instrument Configuration | Not packaged or synthesized in this phase |

All selected Method/Report MD files are localized before compilation. Component CMBX
files and the final Sequence are built under the short local Web work root, then the
final candidate is copied into the managed local asset store. Sequence generation must
not bind directly to a nested OneDrive/SharePoint generation-project path.

## Next Evidence Needed

Export a deliberately minimal carrier from CM 7.2 and/or 7.3 containing:

- one idle `Unknown` Injection;
- one benign `No_Integration` Processing Method;
- one simple Instrument Method;
- one simple Report Template;
- only the sequence variables required by that Injection.

This will let the builder distinguish mandatory DataContract nodes from stale objects
in a copied production sequence. After that, the next work items are controlled
Processing Method binding, collapsing repeated Method assignments to one shared
packaged Method object instead of carrier slot instances, and an Instrument
Configuration compatibility manifest.
