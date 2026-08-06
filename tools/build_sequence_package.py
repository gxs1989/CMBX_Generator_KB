from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sequence_package_builder import (
    SequencePackageRequest,
    build_sequence_package,
    sequence_package_validation_text,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Package standalone Instrument Method and Report Template CMBX assets into one sequence carrier."
    )
    parser.add_argument("carrier_cmbx", type=Path)
    parser.add_argument("method_cmbx", type=Path)
    parser.add_argument("report_cmbx", type=Path)
    parser.add_argument("output_cmbx", type=Path)
    parser.add_argument("--sequence-name", required=True)
    parser.add_argument("--injection-name", required=True)
    parser.add_argument("--method-name", default="")
    parser.add_argument("--report-name", default="")
    args = parser.parse_args()
    validation = build_sequence_package(
        SequencePackageRequest(
            carrier_cmbx=args.carrier_cmbx,
            method_cmbx=args.method_cmbx,
            report_cmbx=args.report_cmbx,
            output_cmbx=args.output_cmbx,
            sequence_name=args.sequence_name,
            injection_name=args.injection_name,
            method_name=args.method_name,
            report_name=args.report_name,
        )
    )
    print(sequence_package_validation_text(validation))
    if not validation.passed:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
