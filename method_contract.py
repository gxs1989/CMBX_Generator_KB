from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class MethodContract:
    method_name: str
    stages: tuple[str, ...]
    set_symbols: tuple[str, ...]
    run_commands: tuple[str, ...]
    acquisition_on: tuple[str, ...]
    acquisition_off: tuple[str, ...]
    ret_time_initializations: tuple[str, ...]
    ret_time_emissions: tuple[str, ...]
    logged_properties: tuple[str, ...]
    wait_conditions: tuple[str, ...]
    trigger_definitions: tuple[str, ...]
    temperature_setpoints: tuple[str, ...]
    required_symbol_roots: tuple[str, ...]


def build_method_contract_from_flow_tsv(path: str | Path) -> MethodContract:
    return build_method_contract_from_flow_rows(_read_flow_rows(path))


def build_method_contract_from_flow_rows(rows: Iterable[dict[str, str]]) -> MethodContract:
    row_list = list(rows)
    method_name = _first_nonempty(row.get("Method", "") for row in row_list)
    stages: list[str] = []
    set_symbols: list[str] = []
    run_commands: list[str] = []
    acquisition_on: list[str] = []
    acquisition_off: list[str] = []
    ret_time_initializations: list[str] = []
    ret_time_emissions: list[str] = []
    logged_properties: list[str] = []
    wait_conditions: list[str] = []
    trigger_definitions: list[str] = []
    temperature_setpoints: list[str] = []
    symbol_roots: list[str] = []

    for row in row_list:
        action = row.get("Action", "")
        stage = row.get("Stage", "")
        target = row.get("Target", "")
        value = row.get("Value", "")
        if stage:
            stages.append(stage)
        if action == "SET" and target:
            set_symbols.append(target)
            symbol_roots.append(_symbol_root(target))
            if target.startswith("RetTimes."):
                if value == "0":
                    ret_time_initializations.append(target)
                elif "System.Retention" in value:
                    ret_time_emissions.append(target)
            if "Temperature.Nominal" in target:
                temperature_setpoints.append(f"{target}={value}")
        elif action == "RUN" and target:
            run_commands.append(target)
            symbol_roots.append(_symbol_root(target))
            if target.endswith(".AcqOn"):
                acquisition_on.append(target.removesuffix(".AcqOn"))
            elif target.endswith(".AcqOff"):
                acquisition_off.append(target.removesuffix(".AcqOff"))
            elif target == "Log" and value:
                logged_properties.append(value)
                symbol_roots.append(_symbol_root(value))
            elif target == "Wait" and value:
                wait_conditions.append(value)
            elif target == "System.Trigger":
                trigger_definitions.append(value)

    return MethodContract(
        method_name=method_name,
        stages=_unique_in_order(stages),
        set_symbols=_unique_in_order(set_symbols),
        run_commands=_unique_in_order(run_commands),
        acquisition_on=_unique_in_order(acquisition_on),
        acquisition_off=_unique_in_order(acquisition_off),
        ret_time_initializations=_unique_in_order(ret_time_initializations),
        ret_time_emissions=_unique_in_order(ret_time_emissions),
        logged_properties=_unique_in_order(logged_properties),
        wait_conditions=_unique_in_order(wait_conditions),
        trigger_definitions=_unique_in_order(trigger_definitions),
        temperature_setpoints=_unique_in_order(temperature_setpoints),
        required_symbol_roots=_unique_in_order(symbol for symbol in symbol_roots if symbol),
    )


def method_contract_summary_text(contract: MethodContract) -> str:
    sections = [
        ("Method", (contract.method_name,)),
        ("Stages", contract.stages),
        ("Required Symbol Roots", contract.required_symbol_roots),
        ("Set Symbols", contract.set_symbols),
        ("Run Commands", contract.run_commands),
        ("Acquisition On", contract.acquisition_on),
        ("RetTime Initializations", contract.ret_time_initializations),
        ("RetTime Emissions", contract.ret_time_emissions),
        ("Logged Properties", contract.logged_properties),
        ("Wait Conditions", contract.wait_conditions),
        ("Trigger Definitions", contract.trigger_definitions),
        ("Temperature Setpoints", contract.temperature_setpoints),
    ]
    lines: list[str] = []
    for title, values in sections:
        lines.append(title)
        lines.append("-" * len(title))
        lines.extend(values or ("(none)",))
        lines.append("")
    return "\n".join(lines).rstrip()


def method_contracts_tsv(contracts: Iterable[MethodContract]) -> str:
    lines = [
        "\t".join(
            [
                "Method",
                "Stages",
                "RequiredSymbolRoots",
                "AcquisitionOn",
                "RetTimeEmissions",
                "LoggedProperties",
                "WaitConditions",
                "TriggerCount",
                "TemperatureSetpoints",
            ]
        )
    ]
    for contract in contracts:
        lines.append(
            "\t".join(
                [
                    contract.method_name,
                    ", ".join(contract.stages),
                    ", ".join(contract.required_symbol_roots),
                    ", ".join(contract.acquisition_on),
                    ", ".join(contract.ret_time_emissions),
                    ", ".join(contract.logged_properties),
                    " | ".join(contract.wait_conditions),
                    str(len(contract.trigger_definitions)),
                    " | ".join(contract.temperature_setpoints),
                ]
            )
        )
    return "\n".join(lines)


def _read_flow_rows(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _symbol_root(symbol: str) -> str:
    if not symbol:
        return ""
    if symbol.startswith(("Variables.", "RetTimes.", "StabVars.", "TempVars.")):
        return symbol.split(".", 1)[0]
    if "." not in symbol:
        return symbol
    return symbol.split(".", 1)[0]


def _first_nonempty(values: Iterable[str]) -> str:
    for value in values:
        if value:
            return value
    return ""


def _unique_in_order(values: Iterable[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return tuple(result)
