"""Minimal command-line interface for reproducible QuantumSec runs."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from experiments.export import export_csv, export_json, load_config_json, load_configs_json
from experiments.runner import ExperimentRunner, run_batch
from experiments.runtime import ExperimentRuntimeFactory
from pqc.errors import PQCError


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m experiments.cli")
    commands = parser.add_subparsers(dest="command", required=True)

    run = commands.add_parser("run", help="execute one ExperimentConfig JSON object")
    run.add_argument("config", help="input configuration JSON")
    run.add_argument("--output", required=True, help="output ExperimentRecord JSON")

    batch = commands.add_parser("batch", help="execute an array of ExperimentConfig objects")
    batch.add_argument("configs", help="input configuration JSON array")
    batch.add_argument("--json", dest="json_output", help="output record array JSON")
    batch.add_argument("--csv", dest="csv_output", help="output analysis-ready CSV")
    batch.add_argument("--shuffle", action="store_true", help="shuffle conditions reproducibly")
    batch.add_argument("--order-seed", type=int, help="seed for order randomization only")
    batch.add_argument("--warmup-runs", type=int, default=0, help="discarded runs before recording")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    runner = ExperimentRunner(ExperimentRuntimeFactory())
    try:
        if args.command == "run":
            record = runner.run(load_config_json(args.config))
            export_json(record, args.output)
            return 0
        if not args.json_output and not args.csv_output:
            parser.error("batch requires at least one of --json or --csv")
        records = run_batch(
            load_configs_json(args.configs),
            runner,
            shuffle=args.shuffle,
            order_seed=args.order_seed,
            warmup_runs=args.warmup_runs,
        )
        if args.json_output:
            export_json(records, args.json_output)
        if args.csv_output:
            export_csv(records, args.csv_output)
        return 0
    except (OSError, PQCError, TypeError, ValueError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
