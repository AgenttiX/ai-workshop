import json
from pathlib import Path
import subprocess
import sys

import pytest

REPO_DIR = Path(__file__).resolve().parents[2]
RUFF_HOOK = REPO_DIR / "exercises" / "06_hook" / "hooks" / "ruff_on_edit.py"
PYTEST_HOOK = Path(__file__).resolve().parent / "hooks" / "pytest_on_stop.py"


def run_hook(hook: Path, hook_input: dict[str, object], *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(hook), *args], input=json.dumps(hook_input), capture_output=True, text=True, check=False
    )


def edit_input(path: Path) -> dict[str, object]:
    return {"hook_event_name": "PostToolUse", "tool_name": "Write", "tool_input": {"file_path": str(path)}}


@pytest.mark.parametrize(
    ("name", "content"),
    [("clean.py", '"""A clean module."""\n\nX = 1\n'), ("notes.txt", "import os\n"), ("missing.py", None)],
)
def test_ruff_hook_lets_clean_and_non_python_files_pass(tmp_path, name, content):
    path = tmp_path / name
    if content is not None:
        path.write_text(content)
    result = run_hook(RUFF_HOOK, edit_input(path))
    assert result.returncode == 0
    assert result.stderr == ""


def test_ruff_hook_reports_an_unused_import(tmp_path):
    path = tmp_path / "sloppy.py"
    path.write_text('"""A sloppy module."""\n\nimport os\n')
    result = run_hook(RUFF_HOOK, edit_input(path))
    assert result.returncode == 2
    assert "F401" in result.stderr


def write_test(directory: Path, passes: bool) -> Path:
    directory.mkdir()
    (directory / "test_example.py").write_text(f"def test_example():\n    assert {passes}\n")
    return directory


def test_stop_hook_lets_claude_stop_when_tests_pass(tmp_path):
    result = run_hook(PYTEST_HOOK, {"stop_hook_active": False}, str(write_test(tmp_path / "ok", passes=True)))
    assert result.returncode == 0


def test_stop_hook_keeps_claude_working_when_tests_fail(tmp_path):
    result = run_hook(PYTEST_HOOK, {"stop_hook_active": False}, str(write_test(tmp_path / "bad", passes=False)))
    assert result.returncode == 2
    assert "1 failed" in result.stderr


def test_stop_hook_allows_stopping_on_the_second_attempt(tmp_path):
    result = run_hook(PYTEST_HOOK, {"stop_hook_active": True}, str(write_test(tmp_path / "bad", passes=False)))
    assert result.returncode == 0
