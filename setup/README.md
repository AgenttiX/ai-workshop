# Setup scripts

The commands of the quick setup in the [README](../README.md#set-up-your-laptop-before-the-workshop),
one file per operating system:

- `ubuntu.sh`: Ubuntu 24.04 and newer
- `macos.sh`: macOS with [Homebrew](https://brew.sh/)
- `windows.ps1`: Windows 11 with PowerShell

The README tells participants to run them one line at a time, but the files can also be run as a whole.
The workflow `.github/workflows/setup.yml` runs each of them on a fresh GitHub Actions runner.

These files are the source of truth. After editing them, copy them to `README.md` with
```bash
./setup/sync_readme.py
```
The script fills the code blocks that follow a `<!-- source: setup/... -->` comment.
CI checks with `./setup/sync_readme.py --check` that the README is up to date.
