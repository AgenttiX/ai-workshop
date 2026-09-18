from workshop import check


def test_python_version_is_supported():
    result = check.check_python()
    assert result.ok
    assert "3." in result.detail


def test_python_version_check_can_fail():
    result = check.check_python(min_version=(99, 0))
    assert not result.ok


def test_installed_package():
    result = check.check_package("numpy")
    assert result.ok
    assert result.detail[0].isdigit()


def test_missing_package():
    result = check.check_package("this-package-does-not-exist")
    assert not result.ok
    assert "pip install" in result.detail


def test_missing_command_is_reported():
    result = check.check_command("this-command-does-not-exist", required=False)
    assert not result.ok
    assert not result.required
    assert str(result).startswith("[MISS]")


def test_git_is_available():
    result = check.check_command("git")
    assert result.ok
    assert "git" in result.detail


def test_run_checks_covers_everything():
    names = {result.name for result in check.run_checks()}
    assert "Python" in names
    assert set(check.REQUIRED_PACKAGES) <= names
    assert set(check.REQUIRED_COMMANDS) <= names
    assert set(check.OPTIONAL_COMMANDS) <= names


def test_main_exit_code(capsys):
    code = check.main()
    output = capsys.readouterr().out
    assert code in (0, 1)
    assert "[OK  ] Python" in output
