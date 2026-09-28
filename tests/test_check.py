import io
from pathlib import Path
import sys

from workshop import check


def test_python_version_is_supported():
    result = check.check_python()
    assert result.ok
    assert "3." in result.detail


def test_python_version_check_can_fail():
    result = check.check_python(min_version=(99, 0))
    assert not result.ok
    assert "99.0 or newer is needed" in result.detail


def test_installed_package():
    result = check.check_package("numpy")
    assert result.ok
    assert result.detail[0].isdigit()


def test_missing_package():
    result = check.check_package("this-package-does-not-exist")
    assert not result.ok
    assert "--setup" in result.detail


def test_missing_command_is_reported():
    result = check.check_command("this-command-does-not-exist", required=False)
    assert not result.ok
    assert not result.required
    assert str(result).startswith("[WARN]")


def test_git_is_available():
    result = check.check_command("git")
    assert result.ok
    assert "git" in result.detail


def test_vscode_extensions_are_skipped_without_the_editor():
    assert check.check_vscode_extensions("this-editor-does-not-exist") == []


def test_virtual_environment_is_detected(monkeypatch, tmp_path):
    monkeypatch.setattr(sys, "prefix", str(tmp_path / "venv"))
    monkeypatch.setattr(sys, "base_prefix", str(tmp_path / "python"))
    assert check.in_virtual_environment()


def test_missing_virtual_environment_is_detected(monkeypatch, tmp_path):
    monkeypatch.setattr(sys, "prefix", str(tmp_path))
    monkeypatch.setattr(sys, "base_prefix", str(tmp_path))
    assert not check.in_virtual_environment()
    assert not check.check_environment().ok


def test_conda_environment_counts_as_an_environment(monkeypatch, tmp_path):
    (tmp_path / "conda-meta").mkdir()
    monkeypatch.setattr(sys, "prefix", str(tmp_path))
    monkeypatch.setattr(sys, "base_prefix", str(tmp_path))
    assert check.in_virtual_environment()


def test_venv_python_paths():
    venv = Path("venv")
    assert check.venv_python(venv, windows=False) == venv / "bin" / "python"
    assert check.venv_python(venv, windows=True) == venv / "Scripts" / "python.exe"


def test_activation_instructions():
    assert "source venv/bin/activate" in check.activation_instructions(windows=False)
    windows = check.activation_instructions(windows=True)
    assert "venv\\Scripts\\Activate.ps1" in windows
    assert "Set-ExecutionPolicy" in windows


def test_ask_without_a_terminal_answers_no(monkeypatch):
    monkeypatch.setattr(sys, "stdin", io.StringIO("y\n"))
    assert not check.ask("Proceed?")


def test_run_checks_covers_everything():
    names = {result.name for result in check.run_checks()}
    assert {"Python", "Virtual environment"} <= names
    assert set(check.REQUIRED_PACKAGES) <= names
    assert set(check.REQUIRED_COMMANDS) <= names
    assert set(check.OPTIONAL_COMMANDS) <= names


def test_main_exit_code(capsys):
    code = check.main(["--no-setup"])
    output = capsys.readouterr().out
    assert code in (0, 1)
    assert "[OK  ] Python" in output
