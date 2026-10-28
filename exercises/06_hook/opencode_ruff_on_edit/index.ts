/* The OpenCode counterpart of ``hooks/ruff_on_edit.py``.

OpenCode does not read ``settings.local.json`` and has no stdin-JSON hook protocol:
hooks are registered by a TypeScript *plugin* that lives under ``.opencode/plugins/``.
Copy this directory there (see the exercise README) and OpenCode loads it — it watches
the plugins and reloads them after a save, so no restart is needed.

What the plugin does is the same as the Python hook in the Claude Code version of this
exercise: after the edit, write or patch tool has touched a Python file, it runs
``ruff check`` on the file (with the Python of the repository's ``.venv``, found by
walking up from this folder; otherwise ``python3``), and appends ruff's findings to the
tool result so that the agent reads them and fixes the file by itself.

The difference to Claude Code: an OpenCode hook cannot veto an edit that has already
happened, so there is no exit-code-2 blocking. The report rides along with the result
instead. The plugin is written as a plain object without the ``@opencode/plugin``
import, which a bare local folder cannot resolve; the loader reads ``id`` and
``setup()`` from it all the same. The hook event types are read defensively, so that
small API changes only make the hook no-op instead of failing.

See https://opencode.ai/v2/docs/build/plugins/server/ for the plugin and hook API.
"""

import { execFileSync } from "node:child_process"
import fs from "node:fs"
import path from "node:path"

/** The tools that can change a file. */
const EDIT_TOOLS = new Set(["edit", "write", "patch"])

/** Return the path from a tool call input, whichever of the field names the tool uses. */
function editedPath(input: unknown): string | null {
  if (typeof input !== "object" || input === null) {
    return null
  }
  const fields = input as Record<string, unknown>
  const filePath = fields.filePath ?? fields.file_path ?? fields.path
  return typeof filePath === "string" ? filePath : null
}

/** Find the Python of the repository's virtual environment, walking up from ``startDir``. */
function pythonInterpreter(startDir: string): string {
  const folder = process.platform === "win32" ? "Scripts" : "bin"
  const names = process.platform === "win32" ? ["python.exe"] : ["python", "python3"]
  let dir = path.resolve(startDir)
  for (;;) {
    for (const name of names) {
      const candidate = path.join(dir, ".venv", folder, name)
      if (fs.existsSync(candidate)) {
        return candidate
      }
    }
    const parent = path.dirname(dir)
    if (parent === dir) {
      return process.platform === "win32" ? "python" : "python3"
    }
    dir = parent
  }
}

export default {
  id: "ruff-on-edit",
  /* ctx is the plugin context of the OpenCode plugin API. */
  async setup(ctx: Record<string, any>) {
    const interpreter = pythonInterpreter(ctx.location.directory)
    ctx.tool.hook("execute.after", (event: Record<string, any>) => {
      if (event.status !== "completed" || !EDIT_TOOLS.has(event.tool ?? "")) {
        return
      }
      const filePath = editedPath(event.input)
      if (filePath === null || !filePath.endsWith(".py") || !fs.existsSync(filePath)) {
        return
      }

      let findings: string | null = null
      try {
        execFileSync(interpreter, ["-m", "ruff", "check", filePath], {
          encoding: "utf8",
          cwd: path.dirname(filePath), // so that ruff prints short, relative file names
        })
      } catch (error) {
        const exit = error as { code?: string; status?: number; stdout?: string; stderr?: string }
        if (exit.code !== undefined) {
          return // Python could not be run; nothing the agent could fix by editing the file.
        }
        if (exit.status === 1) {
          findings = exit.stdout?.trim() || exit.stderr?.trim() || null
        }
      }
      if (findings === null) {
        return
      }

      const report = [
        `Plugin ruff-on-edit: ruff found problems in the Python file that was just edited (${filePath}):`,
        "",
        findings,
        "",
        "Fix the file (with `ruff check --fix` on it or by hand) before moving on.",
      ].join("\n")
      event.result = {
        ...event.result,
        content: [...(event.result?.content ?? []), { type: "text", text: report }],
      }
    })
  },
}
