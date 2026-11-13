"""Basic tests for the tecli package."""

import json
import logging
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest
import requests

import tecli
from tecli import commands


def test_commands_class_exists():
    """Test that the Commands class is importable."""
    assert hasattr(commands, "Commands")


def test_commands_has_required_methods():
    """Test that Commands class has all required methods."""
    required_methods = [
        "create",
        "start",
        "config",
        "login",
        "publish",
        "download",
        "clear",
        "info",
        "logs",
    ]

    for method in required_methods:
        assert hasattr(commands.Commands, method)
        assert callable(getattr(commands.Commands, method))


class TestCommandsClass:
    """Test the Commands class functionality."""

    def test_commands_are_static_methods(self):
        """Test that command methods are static methods."""
        # These should be callable without instantiation
        assert callable(commands.Commands.create)
        assert callable(commands.Commands.start)
        assert callable(commands.Commands.config)


@pytest.fixture
def publish_project(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Create a project and invoke publish through the real CLI entry point."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["trends", "publish", "--overwrite"])
    monkeypatch.setattr(commands.publish.config, "get", lambda key: "https://api.example.test")
    (tmp_path / "configuration.json").write_text(json.dumps({"name": "test-script"}))
    (tmp_path / "requirements.txt").write_text("")
    (tmp_path / "src").mkdir()
    return tmp_path


@pytest.mark.parametrize("existing", [False, True])
@pytest.mark.parametrize("authenticated", [False, True])
def test_publish_failure_exits_nonzero(
    publish_project: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    caplog: pytest.LogCaptureFixture,
    existing: bool,
    authenticated: bool,
) -> None:
    """Rejected uploads and authentication failures must fail the CLI process."""
    configuration = {"name": "test-script"}
    if existing:
        configuration["id"] = "existing-script"
    config_path = publish_project / "configuration.json"
    config_path.write_text(json.dumps(configuration))
    response = Mock(status_code=400)
    response.json.return_value = {"detail": "Unknown batch_execution_config fields", "status": 400}
    request = Mock(return_value=response if authenticated else None)
    monkeypatch.setattr(commands.publish.auth, "make_authenticated_request", request)

    with pytest.raises(SystemExit) as exc:
        tecli.main()

    assert exc.value.code == 1
    assert request.call_args.args[0] == ("PATCH" if existing else "POST")
    assert "Script published successfully" not in capsys.readouterr().out
    if authenticated:
        assert "Unknown batch_execution_config fields" in caplog.text
    assert json.loads(config_path.read_text()) == configuration
    assert not (publish_project / "test-script.tar.gz").exists()


def test_publish_exception_exits_nonzero(
    publish_project: Path,
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Network exceptions must not be logged and converted into a successful exit."""
    monkeypatch.setattr(
        commands.publish.auth,
        "make_authenticated_request",
        Mock(side_effect=requests.ConnectionError("API unavailable")),
    )

    with caplog.at_level(logging.ERROR), pytest.raises(SystemExit) as exc:
        tecli.main()

    assert exc.value.code == 1
    assert "API unavailable" in caplog.text


def test_publish_public_failure_exits_nonzero(
    publish_project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """An uploaded script is not a successful public publication if approval fails."""
    monkeypatch.setattr(sys, "argv", ["trends", "publish", "--overwrite", "--public"])
    uploaded = Mock(status_code=200)
    uploaded.json.return_value = {"data": {"id": "published-script"}}
    rejected = Mock(status_code=403)
    rejected.json.return_value = {"detail": "Not allowed"}
    monkeypatch.setattr(
        commands.publish.auth,
        "make_authenticated_request",
        Mock(side_effect=[uploaded, rejected]),
    )

    with pytest.raises(SystemExit) as exc:
        tecli.main()

    assert exc.value.code == 1


@pytest.mark.parametrize("existing", [False, True])
def test_publish_success_preserves_successful_exit(
    publish_project: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    existing: bool,
) -> None:
    """Successful creates and updates still finish normally and persist the ID."""
    config_path = publish_project / "configuration.json"
    if existing:
        config_path.write_text(json.dumps({"name": "test-script", "id": "published-script"}))
    response = Mock(status_code=200)
    response.json.return_value = {"data": {"id": "published-script"}}
    monkeypatch.setattr(
        commands.publish.auth, "make_authenticated_request", Mock(return_value=response)
    )

    tecli.main()

    assert "Script published successfully" in capsys.readouterr().out
    assert json.loads(config_path.read_text())["id"] == "published-script"
    assert not (publish_project / "test-script.tar.gz").exists()
