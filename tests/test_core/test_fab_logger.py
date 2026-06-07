# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import json
import logging
import os
import platform
import time
from unittest.mock import patch

import pytest
from requests import RequestException

from fabric_cli.core import fab_logger as logger
from fabric_cli.core import fab_state_config
from fabric_cli.core.fab_exceptions import FabricCLIError


def test_log_warning():
    logger.log_warning("This is a warning message")

    logger.log_warning("This is a warning message with a command", "command")


def test_log_debug():
    logger.log_debug("This is a debug message")


def test_log_info():
    logger.log_info("This is an info message")


def test_log_progress(monkeypatch):
    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "1")
    logger.log_progress("This is a progress message")

    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "0")
    logger.log_progress("This is a progress message")


def test_log_debug_http_request(monkeypatch):
    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "1")
    logger.log_debug_http_request("GET", "http://example.com", {}, 10)

    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "0")
    logger.log_debug_http_request("GET", "http://example.com", {}, 10)


def test_log_debug_http_request_json(monkeypatch):
    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "1")
    logger.log_debug_http_request(
        "GET", "http://example.com", {}, 10, json={"key": "value"}
    )

    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "0")
    logger.log_debug_http_request(
        "GET", "http://example.com", {}, 10, json={"key": "value"}
    )


def test_log_debug_http_request_data(monkeypatch):
    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "1")
    logger.log_debug_http_request(
        "GET", "http://example.com", {}, 10, data={"key": "value"}
    )

    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "0")
    logger.log_debug_http_request(
        "GET", "http://example.com", {}, 10, data={"key": "value"}
    )


def test_log_debug_http_request_files(monkeypatch):
    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "1")
    logger.log_debug_http_request(
        "GET", "http://example.com", {}, 10, files={"key": "value"}
    )

    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "0")
    logger.log_debug_http_request(
        "GET", "http://example.com", {}, 10, files={"key": "value"}
    )


def test_log_debug_http_request_attempt(monkeypatch):
    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "1")
    logger.log_debug_http_request("GET", "http://example.com", {}, 10, attempt=2)

    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "0")
    logger.log_debug_http_request("GET", "http://example.com", {}, 10, attempt=2)


def test_log_debug_http_request_user_agent(monkeypatch):
    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "1")
    logger.log_debug_http_request(
        "GET", "http://example.com", {"User-Agent": "value"}, 10
    )

    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "0")
    logger.log_debug_http_request(
        "GET", "http://example.com", {"User-Agent": "value"}, 10
    )


def test_log_debug_http_request_authorization(monkeypatch):
    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "1")
    logger.log_debug_http_request(
        "GET", "http://example.com", {"Authorization": "value"}, 10
    )

    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "0")
    logger.log_debug_http_request(
        "GET", "http://example.com", {"Authorization": "value"}, 10
    )


def test_log_debug_http_request_sample_header(monkeypatch):
    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "1")
    logger.log_debug_http_request(
        "GET", "http://example.com", {"Some-Header": "value"}, 10
    )

    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "0")
    logger.log_debug_http_request(
        "GET", "http://example.com", {"Some-Header": "value"}, 10
    )


def test_log_debug_http_response(monkeypatch):
    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "1")
    logger.log_debug_http_response(200, {}, "Response text", time.time())

    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "0")
    logger.log_debug_http_response(200, {}, "Response text", time.time())


def test_log_debug_http_response_sample_header(monkeypatch):
    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "1")
    logger.log_debug_http_response(
        200, {"Some-Header": "value"}, "Response text", time.time()
    )

    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "0")
    logger.log_debug_http_response(
        200, {"Some-Header": "value"}, "Response text", time.time()
    )


def test_log_debug_http_response_json(monkeypatch):
    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "1")
    logger.log_debug_http_response(
        200,
        {"Content-Type": "application/json"},
        json.dumps({"key": "value"}),
        time.time(),
    )

    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "0")
    logger.log_debug_http_response(
        200,
        {"Content-Type": "application/json"},
        json.dumps({"key": "value"}),
        time.time(),
    )


def test_log_debug_http_response_bad_json(monkeypatch):
    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "1")
    logger.log_debug_http_response(
        200, {"Content-Type": "application/json"}, "{ bad json", time.time()
    )


def test_log_debug_http_request_exception(monkeypatch):
    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "1")
    logger.log_debug_http_request_exception(RequestException("This is an exception"))

    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "0")
    logger.log_debug_http_request_exception(RequestException("This is an exception"))


def test_get_logger():
    assert logger.get_logger() is not None
    assert logger.get_logger().name == "FabricCLI"
    assert logger.get_logger().level == logging.DEBUG
    assert (
        logger.get_logger().handlers[0].formatter._fmt
        == "%(asctime)s - %(levelname)s - %(message)s"
    )
    assert logger.log_file_path is not None


def test_get_log_file_path(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    assert_log_file_path("\\AppData\\Local")
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    # Simulate realpath returns a different path (sandbox)
    monkeypatch.setattr("os.path.realpath", lambda x: x + "_sandbox")
    assert_log_file_path("\\AppData\\Local", True)
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    assert_log_file_path("/Library/Logs")
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setattr(os, "environ", {})
    assert_log_file_path("/.local/state")
    monkeypatch.setattr(os, "environ", {"XDG_STATE_HOME": "/tmp"})
    assert_log_file_path("/tmp")


def assert_log_file_path(base_dir: str, is_sandbox=False):
    log_file_path = logger._get_log_file_path()
    assert log_file_path is not None
    assert log_file_path.endswith("fabcli_debug.log")
    assert base_dir in log_file_path
    if is_sandbox:
        assert "_sandbox" in log_file_path


def test_print_log_file_path_debug_enabled_success(
    mock_get_log_file_path, mock_log_warning, monkeypatch
):
    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "true")

    mock_get_log_file_path.return_value = "/fake/path/fabcli_debug.log"

    logger.print_log_file_path()

    mock_get_log_file_path.assert_called_once()
    mock_log_warning.assert_called_once()


def test_print_log_file_path_debug_disabled_success(
    mock_get_log_file_path, mock_log_warning, monkeypatch
):
    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "false")

    logger.print_log_file_path()

    mock_get_log_file_path.assert_not_called()
    mock_log_warning.assert_not_called()


@pytest.fixture
def mock_log_warning():
    with patch("fabric_cli.core.fab_logger.log_warning") as mock:
        yield mock


@pytest.fixture
def mock_get_log_file_path():
    with patch("fabric_cli.core.fab_logger.get_log_file_path") as mock:
        yield mock


# ── Security: log directory and file permissions ─────────────────────────────

_skip_on_windows = pytest.mark.skipif(
    os.name == "nt", reason="POSIX permission tests not applicable on Windows"
)


@_skip_on_windows
def test_get_log_file_path_creates_directory_with_restricted_permissions_success(
    monkeypatch, tmp_path
):
    """Verify log directory is created with mode 0o700 (owner-only)."""
    log_dir = tmp_path / "fabric-cli" / "log"
    monkeypatch.setattr(logger, "user_log_dir", lambda app_name: str(log_dir))

    result = logger._get_log_file_path()
    assert result.endswith("fabcli_debug.log")
    assert log_dir.exists()

    mode = oct(log_dir.stat().st_mode & 0o777)
    assert mode == "0o700", f"Log directory has mode {mode}, expected 0o700"


@_skip_on_windows
def test_log_file_created_with_restricted_permissions_success(monkeypatch, tmp_path):
    """Verify log file is created with mode 0o600 and is readable by the owner."""
    log_dir = tmp_path / "fabric-cli" / "log"
    log_dir.mkdir(parents=True, mode=0o700)
    monkeypatch.setattr(logger, "user_log_dir", lambda app_name: str(log_dir))

    # Reset singleton so _setup_logger creates a fresh handler
    monkeypatch.setattr(logger, "_logger_instance", None)

    log_file = log_dir / "fabcli_debug.log"
    log_instance = logger._setup_logger(str(log_file))

    # Write something to ensure the file exists
    log_instance.debug("permission test entry")

    assert log_file.exists()
    mode = oct(log_file.stat().st_mode & 0o777)
    assert mode == "0o600", f"Log file has mode {mode}, expected 0o600"

    # Verify the owner can still read the file
    content = log_file.read_text()
    assert "permission test entry" in content

    # Cleanup: remove handlers to avoid accumulation on the global singleton
    for handler in log_instance.handlers[:]:
        log_instance.removeHandler(handler)
        handler.close()


@_skip_on_windows
def test_log_file_rotation_preserves_restricted_permissions_success(
    monkeypatch, tmp_path
):
    """Verify rotated log files maintain 0o600 permissions."""
    log_dir = tmp_path / "fabric-cli" / "log"
    log_dir.mkdir(parents=True, mode=0o700)
    log_file = log_dir / "fabcli_debug.log"

    # Create a handler with a small maxBytes to force rotation quickly
    handler = logger._RestrictedRotatingFileHandler(
        str(log_file),
        maxBytes=100,  # Very small to trigger rotation
        backupCount=2,
    )
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)

    test_logger = logging.getLogger("FabricCLI_rotation_test")
    test_logger.setLevel(logging.DEBUG)
    test_logger.addHandler(handler)

    # Write enough data to trigger at least one rotation
    for i in range(20):
        test_logger.debug(f"rotation test entry {i} with padding to exceed limit")

    # Check that at least one rotated file was created
    rotated_file_1 = log_dir / "fabcli_debug.log.1"
    assert rotated_file_1.exists(), "Expected at least one rotated log file"

    # Verify permissions on the base log file
    mode = oct(log_file.stat().st_mode & 0o777)
    assert mode == "0o600", f"Base log file has mode {mode}, expected 0o600"

    # Verify permissions on the rotated file
    mode = oct(rotated_file_1.stat().st_mode & 0o777)
    assert mode == "0o600", f"Rotated log file has mode {mode}, expected 0o600"

    # Cleanup
    test_logger.removeHandler(handler)
    handler.close()


# ── Security: response header masking tests ──────────────────────────────────


def test_log_debug_http_response_masks_set_cookie(monkeypatch):
    """Verify Set-Cookie response headers are masked to prevent credential leakage."""
    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "true")

    captured = []
    test_logger = logger.get_logger()
    original_debug = test_logger.debug
    test_logger.debug = lambda msg: captured.append(msg)

    try:
        logger.log_debug_http_response(
            200,
            {"Set-Cookie": "session=secret_value; Path=/; HttpOnly"},
            "",
            time.time(),
        )
    finally:
        test_logger.debug = original_debug

    cookie_lines = [l for l in captured if "Set-Cookie" in l]
    assert len(cookie_lines) == 1
    assert "secret_value" not in cookie_lines[0]
    assert "*****" in cookie_lines[0]


def test_log_debug_http_response_masks_continuation_header(monkeypatch):
    """Verify x-ms-continuation headers are masked."""
    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "true")

    captured = []
    test_logger = logger.get_logger()
    original_debug = test_logger.debug
    test_logger.debug = lambda msg: captured.append(msg)

    try:
        logger.log_debug_http_response(
            200,
            {"x-ms-continuation": "secret-pagination-token"},
            "",
            time.time(),
        )
    finally:
        test_logger.debug = original_debug

    cont_lines = [l for l in captured if "x-ms-continuation" in l]
    assert len(cont_lines) == 1
    assert "secret-pagination-token" not in cont_lines[0]
    assert "*****" in cont_lines[0]


def test_log_debug_http_response_preserves_non_sensitive_headers(monkeypatch):
    """Verify non-sensitive headers are logged in plaintext."""
    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "true")

    captured = []
    test_logger = logger.get_logger()
    original_debug = test_logger.debug
    test_logger.debug = lambda msg: captured.append(msg)

    try:
        logger.log_debug_http_response(
            200,
            {"Content-Type": "application/json", "x-ms-request-id": "req-123"},
            "",
            time.time(),
        )
    finally:
        test_logger.debug = original_debug

    ct_lines = [l for l in captured if "Content-Type" in l]
    assert "application/json" in ct_lines[0]

    rid_lines = [l for l in captured if "x-ms-request-id" in l]
    assert "req-123" in rid_lines[0]


# ── Security: response body redaction tests ──────────────────────────────────


def test_redact_sensitive_values_redacts_known_keys():
    """Verify _redact_sensitive_values masks all known sensitive keys."""
    obj = {
        "value": [{"id": "ws-1"}],
        "sasToken": "sv=2021&sig=SECRET",
        "connectionString": "AccountKey=SECRET",
        "continuationToken": "token123",
        "safe_key": "visible",
    }
    redacted = logger._redact_sensitive_values(obj)
    assert redacted["sasToken"] == "*****"
    assert redacted["connectionString"] == "*****"
    assert redacted["continuationToken"] == "*****"
    assert redacted["safe_key"] == "visible"
    assert redacted["value"] == [{"id": "ws-1"}]


def test_redact_sensitive_values_handles_nested_objects():
    """Verify redaction works recursively in nested structures."""
    obj = {
        "outer": {
            "inner": {
                "password": "secret123",
                "name": "visible",
            }
        },
        "items": [
            {"accessToken": "tok1", "id": "1"},
            {"refreshToken": "tok2", "id": "2"},
        ],
    }
    redacted = logger._redact_sensitive_values(obj)
    assert redacted["outer"]["inner"]["password"] == "*****"
    assert redacted["outer"]["inner"]["name"] == "visible"
    assert redacted["items"][0]["accessToken"] == "*****"
    assert redacted["items"][0]["id"] == "1"
    assert redacted["items"][1]["refreshToken"] == "*****"


def test_redact_and_format_json_redacts_sensitive_keys():
    """Verify the full JSON redaction + formatting pipeline."""
    input_json = json.dumps({"sasToken": "sig=SECRET", "name": "test"})
    result = logger._redact_and_format_json(input_json)
    parsed = json.loads(result)
    assert parsed["sasToken"] == "*****"
    assert parsed["name"] == "test"


def test_redact_and_format_json_handles_bad_json():
    """Verify graceful handling of malformed JSON."""
    result = logger._redact_and_format_json("{ bad json")
    assert result == "Failed to parse JSON response"


def test_log_debug_http_response_redacts_body_sensitive_keys(monkeypatch):
    """Verify the full logging path redacts sensitive keys in response bodies."""
    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "true")

    captured = []
    test_logger = logger.get_logger()
    original_debug = test_logger.debug
    test_logger.debug = lambda msg: captured.append(msg)

    response_body = json.dumps({
        "value": [{"id": "ws-1"}],
        "sasToken": "sv=2021-06-08&sig=REAL_SIGNATURE",
        "continuationToken": "eyJwYWdl",
    })

    try:
        logger.log_debug_http_response(
            200,
            {"Content-Type": "application/json"},
            response_body,
            time.time(),
        )
    finally:
        test_logger.debug = original_debug

    body_lines = [l for l in captured if "sasToken" in l or "REAL_SIGNATURE" in l]
    full_log = " ".join(captured)
    assert "REAL_SIGNATURE" not in full_log
    assert "eyJwYWdl" not in full_log


# ── Security: request body redaction tests ───────────────────────────────────


def test_log_debug_http_request_redacts_json_body(monkeypatch):
    """Verify request body JSON payloads have sensitive keys redacted."""
    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "true")

    captured = []
    test_logger = logger.get_logger()
    original_debug = test_logger.debug
    test_logger.debug = lambda msg: captured.append(msg)

    request_body = {
        "name": "my-connection",
        "credentialDetails": {
            "password": "SuperSecret123",
            "clientSecret": "spn-secret-value",
        },
    }

    try:
        logger.log_debug_http_request(
            "POST", "http://example.com/connections", {}, 10, json=request_body
        )
    finally:
        test_logger.debug = original_debug

    full_log = " ".join(captured)
    assert "SuperSecret123" not in full_log
    assert "spn-secret-value" not in full_log
    assert "my-connection" in full_log


def test_log_debug_http_request_redacts_data_body(monkeypatch):
    """Verify request data payloads have sensitive keys redacted."""
    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "true")

    captured = []
    test_logger = logger.get_logger()
    original_debug = test_logger.debug
    test_logger.debug = lambda msg: captured.append(msg)

    request_data = {
        "sasToken": "sv=2021&sig=SECRET_SIG",
        "tableName": "sales",
    }

    try:
        logger.log_debug_http_request(
            "POST", "http://example.com/tables", {}, 10, data=request_data
        )
    finally:
        test_logger.debug = original_debug

    full_log = " ".join(captured)
    assert "SECRET_SIG" not in full_log
    assert "sales" in full_log


def test_log_debug_http_request_redacts_file_content(monkeypatch):
    """Verify file upload values are not logged (only keys)."""
    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "true")

    captured = []
    test_logger = logger.get_logger()
    original_debug = test_logger.debug
    test_logger.debug = lambda msg: captured.append(msg)

    try:
        logger.log_debug_http_request(
            "POST", "http://example.com/upload", {}, 10,
            files={"definition": "binary-content-with-secrets"},
        )
    finally:
        test_logger.debug = original_debug

    full_log = " ".join(captured)
    assert "binary-content-with-secrets" not in full_log
    assert "definition" in full_log


# ── Security: case-insensitive key redaction ─────────────────────────────────


def test_redact_sensitive_values_case_insensitive():
    """Verify redaction is case-insensitive for key matching."""
    obj = {
        "SasToken": "sig=SECRET1",
        "PASSWORD": "secret2",
        "connectionString": "AccountKey=secret3",
        "ClientSecret": "secret4",
        "safeName": "visible",
    }
    redacted = logger._redact_sensitive_values(obj)
    assert redacted["SasToken"] == "*****"
    assert redacted["PASSWORD"] == "*****"
    assert redacted["connectionString"] == "*****"
    assert redacted["ClientSecret"] == "*****"
    assert redacted["safeName"] == "visible"


# ── Security: non-JSON response body scrubbing ──────────────────────────────


def test_scrub_secret_patterns_sas_signature():
    """Verify SAS signatures are scrubbed from plain text."""
    text = "Error accessing https://storage.blob.core.windows.net/container?sv=2021&sig=AbCdEfGh123%2B&se=2024-12-31"
    result = logger._scrub_secret_patterns(text)
    assert "AbCdEfGh123" not in result
    assert "*****" in result
    assert "container" in result


def test_scrub_secret_patterns_bearer_token():
    """Verify Bearer tokens are scrubbed from plain text."""
    text = "Authorization failed: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.payload.sig"
    result = logger._scrub_secret_patterns(text)
    assert "eyJhbGciOiJSUzI1NiI" not in result
    assert "*****" in result


def test_scrub_secret_patterns_account_key():
    """Verify AccountKey values are scrubbed from plain text."""
    text = "Connection string: DefaultEndpointsProtocol=https;AccountKey=abc123+def456/ghi789=;EndpointSuffix=core.windows.net"
    result = logger._scrub_secret_patterns(text)
    assert "abc123+def456" not in result
    assert "*****" in result


def test_scrub_secret_patterns_preserves_safe_text():
    """Verify normal text is not modified by scrubbing."""
    text = "Operation completed successfully for workspace my-workspace"
    result = logger._scrub_secret_patterns(text)
    assert result == text


def test_log_debug_http_response_scrubs_non_json_body(monkeypatch):
    """Verify non-JSON response bodies have secret patterns scrubbed."""
    monkeypatch.setattr(fab_state_config, "get_config", lambda x: "true")

    captured = []
    test_logger = logger.get_logger()
    original_debug = test_logger.debug
    test_logger.debug = lambda msg: captured.append(msg)

    non_json_body = "Error: sig=SuperSecretSignature123 at endpoint /api/v1"

    try:
        logger.log_debug_http_response(
            400,
            {"Content-Type": "text/plain"},
            non_json_body,
            time.time(),
        )
    finally:
        test_logger.debug = original_debug

    full_log = " ".join(captured)
    assert "SuperSecretSignature123" not in full_log
