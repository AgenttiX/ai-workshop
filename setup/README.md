# Setup scripts

The setup commands shown on the slides, one file per operating system:

- `ubuntu.sh`: Ubuntu 24.04 and newer
- `macos.sh`: macOS with [Homebrew](https://brew.sh/)
- `windows.ps1`: Windows 11 with PowerShell

The slides are meant to be followed one line at a time, but the files can also be run as a whole.
The workflow `.github/workflows/setup.yml` runs each of them on a fresh GitHub Actions runner.

These files are the source of truth. After editing them, copy them to `slides.html` with
```bash
./setup/sync_slides.py
```
The script fills the `<code>` elements that have a `data-source-file` attribute.
CI checks with `./setup/sync_slides.py --check` that the slides are up to date.
