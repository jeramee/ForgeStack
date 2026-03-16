from __future__ import annotations

import argparse

from forgestack.application.structured_apply import run_structured_apply


def register_ui_apply_command(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "ui-apply",
        help="Generate a project using the internal structured pipeline.",
    )
    parser.add_argument("config", help="Path to the project YAML file.")
    parser.add_argument(
        "--output",
        help="Optional output directory override.",
        default=None,
    )
    parser.add_argument(
        "--json-summary",
        action="store_true",
        help="Print model summary as JSON after generation.",
    )
    parser.set_defaults(handler=handle_ui_apply)


def handle_ui_apply(args: argparse.Namespace) -> int:
    run_structured_apply(
        config_path=args.config,
        output_dir=args.output,
        emit_summary=args.json_summary,
    )
    return 0