# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Wrap user-authored fields in API responses with untrusted content markers.

When --wrap-untrusted is active, free-text fields that come from the Fabric API
(displayName, description, etc.) are wrapped with sentinel markers so that AI
agents consuming the output can distinguish trusted CLI output from potentially
malicious user-authored content.

This prevents indirect prompt injection attacks where an attacker sets a Fabric
item's displayName or description to text that impersonates system instructions.
"""

import re
import secrets
from typing import Any

# Fields where Fabric tenant users can inject arbitrary text.
# System-generated fields (id, type, workspaceId, etc.) are NOT wrapped.
UNTRUSTED_FIELDS: frozenset[str] = frozenset(
    {
        "displayName",
        "description",
        "name",
        "message",
        "commitMessage",
        "notes",
    }
)

# LLM special tokens to neutralize inside untrusted content.
# Prevents low-level tokenizer manipulation if attacker embeds these.
_SPECIAL_TOKENS: list[str] = [
    # OpenAI ChatML
    "<|im_start|>",
    "<|im_end|>",
    "<|endoftext|>",
    # Llama 3
    "<|begin_of_text|>",
    "<|end_of_text|>",
    "<|start_header_id|>",
    "<|end_header_id|>",
    "<|eot_id|>",
    # Llama 2
    "[INST]",
    "[/INST]",
    "<<SYS>>",
    "<</SYS>>",
    # Gemma
    "<start_of_turn>",
    "<end_of_turn>",
]

_MARKER_SPOOF_RE = re.compile(
    r"<<<(?:END_)?UNTRUSTED(?:\s+id=\"[^\"]*\")?\s*>>>",
    re.IGNORECASE,
)


def _sanitize_content(text: str) -> str:
    """Strip LLM special tokens and neutralize spoofed fence markers."""
    for token in _SPECIAL_TOKENS:
        text = text.replace(token, "[REMOVED_SPECIAL_TOKEN]")
    text = _MARKER_SPOOF_RE.sub("[MARKER_SANITIZED]", text)
    return text


def _wrap_string(text: str) -> str:
    """Wrap a single string value with untrusted content markers."""
    marker_id = secrets.token_hex(8)
    sanitized = _sanitize_content(text)
    return (
        f'<<<UNTRUSTED id="{marker_id}">>>'
        f"{sanitized}"
        f'<<<END_UNTRUSTED id="{marker_id}">>>'
    )


def wrap_untrusted_fields(value: Any) -> Any:
    """Recursively wrap user-controlled string fields in a JSON structure.

    Only fields in UNTRUSTED_FIELDS are wrapped. System-generated fields
    (id, type, workspaceId, etc.) pass through unmodified.

    Args:
        value: A dict, list, or scalar value from an API response.

    Returns:
        The same structure with untrusted string fields wrapped in
        <<<UNTRUSTED id="...">>>...<<<END_UNTRUSTED id="...">>> markers.
    """
    if isinstance(value, dict):
        result = {}
        for key, val in value.items():
            if key in UNTRUSTED_FIELDS and isinstance(val, str):
                result[key] = _wrap_string(val)
            else:
                result[key] = wrap_untrusted_fields(val)
        return result
    elif isinstance(value, list):
        return [wrap_untrusted_fields(item) for item in value]
    else:
        return value
