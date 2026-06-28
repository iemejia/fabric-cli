# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os


def add_global_flags(parser) -> None:
    """
    Add global flags that apply to all commands.

    Args:
        parser: The argparse parser to add flags to.
    """
    # Add help flag
    parser.add_argument("-help", action="help")

    # Add format flag to override output format
    parser.add_argument(
        "--output_format",
        required=False,
        choices=["json", "text"],
        help="Override output format type. Optional",
    )

    # Agent safety: wrap untrusted content in output
    parser.add_argument(
        "--wrap-untrusted",
        action="store_true",
        default=os.environ.get("FAB_WRAP_UNTRUSTED", "").lower()
        in ("1", "true", "yes"),
        help=(
            "Wrap user-authored API fields (displayName, description) with "
            "untrusted content markers. Use when fabric-cli output is consumed "
            "by AI agents to prevent indirect prompt injection. "
            "Can also be set via FAB_WRAP_UNTRUSTED=1 environment variable."
        ),
    )
