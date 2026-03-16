from __future__ import annotations

import argparse

from forgestack.application.legacy_apply import run_legacy_apply


def register_apply_command(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "apply",
        help="Generate a project using the stable legacy pipeline.",
    )
    parser.add_argument("config", help="Path to the project YAML file.")
    parser.add_argument(
        "--output",
        help="Optional output directory override.",
        default=None,
    )
    parser.set_defaults(handler=handle_apply)


def handle_apply(args: argparse.Namespace) -> int:
    run_legacy_apply(
        config_path=args.config,
        output_dir=args.output,
    )
    return 0