from __future__ import annotations

import argparse
from collections import defaultdict
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from cmbx_container import load_cmbx_package
from export_service import evaluate_foq_contract_values


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate selected FOQ DB fields for preview.")
    parser.add_argument("--package")
    parser.add_argument("--mapping", required=True)
    parser.add_argument("--device")
    parser.add_argument("--sequence-key")
    parser.add_argument("--report-template", default="")
    parser.add_argument("--fields-json", required=True)
    parser.add_argument("--jobs-json")
    parser.add_argument("--jobs-file")
    args = parser.parse_args(argv)

    fields = json.loads(args.fields_json)
    if args.jobs_json or args.jobs_file:
        return _run_batch(args, fields)
    if not args.package or not args.device or not args.sequence_key:
        parser.error("--package, --device, and --sequence-key are required without --jobs-json")
    package = load_cmbx_package(Path(args.package))
    sequence = _find_sequence(package, args.sequence_key)
    if sequence is None:
        raise ValueError(f"Sequence was not found: {args.sequence_key}")

    _mapping_sheet, contract_values = evaluate_foq_contract_values(
        package,
        Path(args.mapping),
        args.device,
        report_template_name=args.report_template,
        db_field_filter=fields,
        sequence=sequence,
    )
    values = {row.location.db_field: row.value for row in contract_values}
    statuses = {row.location.db_field: row.status for row in contract_values}
    print(json.dumps({"values": values, "statuses": statuses}, ensure_ascii=False, default=str))
    return 0


def _run_batch(args: argparse.Namespace, fields: list[str]) -> int:
    if args.jobs_file:
        jobs = json.loads(Path(args.jobs_file).read_text(encoding="utf-8"))["jobs"]
    else:
        jobs = json.loads(args.jobs_json)
    jobs_by_package: dict[str, list[dict[str, str]]] = defaultdict(list)
    for job in jobs:
        jobs_by_package[str(job["package"])].append(job)

    rows: list[dict[str, object]] = []
    total_jobs = len(jobs)
    completed = 0
    _emit("log", message=f"Preview worker received {total_jobs} sequence job(s) in {len(jobs_by_package)} CMBX package(s).")
    for package_index, (package_path, package_jobs) in enumerate(jobs_by_package.items(), start=1):
        package_name = Path(package_path).name
        _emit("log", message=f"Loading package {package_index}/{len(jobs_by_package)}: {package_name}")
        package = load_cmbx_package(Path(package_path))
        report_count = len([item for item in package.methods_and_reports if item.kind == "report_template"])
        _emit("log", message=f"Loaded {package_name}: {len(package.sequences)} sequence(s), {report_count} report template(s).")
        for job in package_jobs:
            completed += 1
            sequence_name = job.get("sequence_name") or job.get("sequence_key") or ""
            device = job.get("device", "")
            report_template = job.get("report_template", "")
            _emit("log", message=f"Evaluating {completed}/{total_jobs}: {sequence_name} | {device} | {report_template or 'auto report'}")
            try:
                sequence = _find_sequence(package, job["sequence_key"])
                if sequence is None:
                    raise ValueError(f"Sequence was not found: {job['sequence_key']}")
                _mapping_sheet, contract_values = evaluate_foq_contract_values(
                    package,
                    Path(args.mapping),
                    device,
                    report_template_name=report_template,
                    db_field_filter=fields,
                    sequence=sequence,
                )
                values = {row.location.db_field: row.value for row in contract_values}
                statuses = {row.location.db_field: row.status for row in contract_values}
                missing = [field for field in fields if field not in values]
                if missing:
                    _emit("log", message=f"{sequence.name}: missing {len(missing)} selected field(s): {', '.join(missing[:6])}")
            except Exception as exc:
                values = {field: f"ERROR: {exc}" for field in fields}
                statuses = {field: "error" for field in fields}
                _emit("log", message=f"{sequence_name}: ERROR: {exc}")
            rows.append(
                {
                    "sequence": sequence_name,
                    "device": device,
                    "report_template": report_template,
                    "values": values,
                    "statuses": statuses,
                }
            )
    _emit("result", rows=rows)
    return 0


def _emit(event_type: str, **payload: object) -> None:
    print(json.dumps({"type": event_type, **payload}, ensure_ascii=False, default=str), flush=True)


def _find_sequence(package, key: str):
    for sequence in package.sequences:
        if key in {sequence.id, sequence.url, sequence.name}:
            return sequence
    return None


if __name__ == "__main__":
    raise SystemExit(main())
