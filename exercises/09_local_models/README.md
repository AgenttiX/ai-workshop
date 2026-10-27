# Exercise 09: Local models (15 min, optional, advanced)
The harness is separate from the model. Claude Code can talk to any server that speaks the Anthropic Messages API, and two programs that run open-weight models on your own computer do: [LM Studio](https://lmstudio.ai/) (a desktop app) and llama-server of [llama.cpp](https://github.com/ggml-org/llama.cpp) (a command-line server, here run in Docker).

Why: privacy (the data never leaves the machine), no rate limits, offline use, cost. What you give up: capability and speed. A model that fits on a laptop is roughly where the cloud models were 1–2 years ago, and on a laptop without a dedicated GPU it's slow.

## What runs where
```text
You → Claude Code ──request (JSON over HTTP)──→ model server on your computer
          ↑   │                                   (LM Studio or llama-server)
          │   └─ runs the tool calls                chat template → llama.cpp → weights
          └──────────reply: text or a tool call───┘
```

- **Weights:** the model itself, a file of billions of numbers (a `.gguf` file, a few GB).
- **Model server:** loads the weights into memory, computes the replies and answers requests at an address such as `http://localhost:1234`. `localhost` means this computer; the number is the *port*, which tells programs on the same computer apart.
- **Chat template:** a small program stored in the model file that turns the list of messages into the one long string the model reads.
- **Context length:** how many tokens (pieces of words) the server keeps room for. Claude Code's instructions and tool descriptions alone are about 1 300 tokens with `claude --bare` and about 22 000 without it.
- **Claude Code** sends the whole conversation every turn. When the model replies with a tool call (e.g. "run `pytest`"), Claude Code runs it on your computer and sends the result back.

The slides *Under the hood* and *Why local models misbehave, in numbers* explain each part and its problems in more detail.

## Before you start
- **Memory:** a model needs about its file size in RAM (or GPU memory), plus the context. The examples here use **Qwen3.5-4B** (2.7 GB). With 8 GB of RAM, take Qwen3.5-2B (1.3 GB); with a GPU with 12 GB or more, Qwen3.5-9B (5.7 GB).
- **Disk:** the model file, and about 1 GB for LM Studio or 1.2 GB for the llama.cpp Docker image.
- **Speed:** without a dedicated GPU, plain `claude` is too slow for this exercise: on our laptop, the model read its 22 000-token prompt at about 24 tokens per second, which makes about 15 minutes before the first answer. That's why the commands below use `claude --bare`, which leaves out most of the tools, `CLAUDE.md` and the memory, so that the prompt is about 1 300 tokens.

Pick **route A** (LM Studio, easier) or **route B** (llama.cpp in Docker, more control). Both end with the same step 3.

## Route A: LM Studio
### A1. Install LM Studio and get a model
Download LM Studio from <https://lmstudio.ai/download>, install it and start it once.

- **Windows, macOS:** run the installer.
- **Linux:** the download is an `.AppImage`. Make it executable and start it:

  ```bash
  chmod +x ~/Downloads/LM-Studio-*.AppImage
  ~/Downloads/LM-Studio-*.AppImage
  ```

  If nothing happens (e.g. on Ubuntu 24.04 and newer), start it with `--no-sandbox` at the end. This turns off the security sandbox of the app's window for this run.

LM Studio comes with a command-line tool, `lms`. Open a terminal and make `lms` available in it:

| Linux, macOS | Windows (PowerShell) |
|---|---|
| `alias lms=~/.lmstudio/bin/lms` | `Set-Alias lms "$env:USERPROFILE\.lmstudio\bin\lms.exe"` |

Download the model and check its name:

```bash
lms get qwen/qwen3.5-4b
lms ls
```

`lms ls` lists the models on your computer. The name in the first column is the one you use below. (You can also download models in the app: the magnifying glass on the left.)

### A2. Fix the chat template
The chat template of Qwen3.5 stops with the error `System message must be at the beginning`, because Claude Code sends a second system message later in the conversation. Change one line:

1. In LM Studio, click **My Models** (the folder icon on the left) and then the **gear icon** next to the model.
2. Find **Prompt Template**. It shows the template as text (Jinja).
3. Find this line:

   ```jinja
   {{- raise_exception('System message must be at the beginning.') }}
   ```

   and replace it with:

   ```jinja
   {{- '<|im_start|>system\n' + content + '<|im_end|>\n' }}
   ```

   The model now reads the second system message as one, instead of stopping.

The fixed template is also in this folder: [`qwen35-claude-code.jinja`](qwen35-claude-code.jinja).

### A3. Load the model and start the server
LM Studio's default context length (8 192 tokens) is too small for Claude Code. Load the model with 32 768 tokens and start the server (replace `qwen3.5-4b` with the name from `lms ls`):

```bash
lms load qwen3.5-4b -c 32768
lms server start
```

Check that it answers: open <http://localhost:1234/v1/models> in a browser. You can also chat with the model in the app first, to see how fast it is. Continue with [step 3](#3-point-claude-code-at-the-server), with port **1234**.

## Route B: llama.cpp in Docker
[Docker](https://docs.docker.com/get-started/get-docker/) runs a program together with everything it needs as a sealed box, a *container*. [`docker-compose.yml`](docker-compose.yml) is the recipe for this one: which program to run (the llama-server image), which folder of your computer to show inside it (`models/`), and which port to open (8080). It also sets the context length, the fixed chat template ([`qwen35-claude-code.jinja`](qwen35-claude-code.jinja)) and turns off Qwen's thinking, which would otherwise be written at the same slow speed as the answer.

### B1. Install Docker and get a model
Install Docker: Docker Engine on Linux, Docker Desktop on Windows and macOS. Then go to this folder and download the model as `models/model.gguf`:

| Linux, macOS | Windows (PowerShell) |
|---|---|
| `cd exercises/09_local_models` | `cd exercises\09_local_models` |
| `mkdir models` | `mkdir models` |
| `curl -L -o models/model.gguf https://huggingface.co/unsloth/Qwen3.5-4B-GGUF/resolve/main/Qwen3.5-4B-Q4_K_M.gguf` | `curl.exe -L -o models\model.gguf https://huggingface.co/unsloth/Qwen3.5-4B-GGUF/resolve/main/Qwen3.5-4B-Q4_K_M.gguf` |

For the 2B or 9B model, change both `4B`s in the address to `2B` or `9B`.

### B2. Start the server
In the same folder:

```bash
docker compose up -d
docker logs -f llama-cpp
```

`up -d` starts the container in the background. `docker logs -f` shows what the server does; wait for `listening on http://0.0.0.0:8080`. Keep this terminal open: for each request, the log shows how fast the model reads the prompt (`prompt eval time`) and writes the answer (`eval time`). Ctrl+C stops showing the log, not the server.

Open <http://localhost:8080> in a browser: llama-server has its own chat page. Continue with step 3, with port **8080**.

## 3. Point Claude Code at the server
Open **a new terminal** and go to the workshop folder. The settings apply only in this terminal, so start `claude` in the same one. Use port 1234 for LM Studio and 8080 for llama-server, and for LM Studio the model name from `lms ls` (llama-server serves one model and ignores the name).

**Linux and macOS:**

```bash
export ANTHROPIC_BASE_URL=http://localhost:1234
export ANTHROPIC_API_KEY=local
export ANTHROPIC_MODEL=qwen3.5-4b
export CLAUDE_CODE_MAX_CONTEXT_TOKENS=32768
export CLAUDE_CODE_ATTRIBUTION_HEADER=0
claude --bare
```

**Windows (PowerShell):**

```powershell
$env:ANTHROPIC_BASE_URL = "http://localhost:1234"
$env:ANTHROPIC_API_KEY = "local"
$env:ANTHROPIC_MODEL = "qwen3.5-4b"
$env:CLAUDE_CODE_MAX_CONTEXT_TOKENS = "32768"
$env:CLAUDE_CODE_ATTRIBUTION_HEADER = "0"
claude --bare
```

What they do:

- `ANTHROPIC_BASE_URL`: where to send the requests, instead of Anthropic's servers.
- `ANTHROPIC_API_KEY`: a key sent with each request. The local servers don't check it, but `claude --bare` needs one.
- `ANTHROPIC_MODEL`: which model to ask for.
- `CLAUDE_CODE_MAX_CONTEXT_TOKENS`: the context length of the server, so that Claude Code summarizes the conversation before it overflows.
- `CLAUDE_CODE_ATTRIBUTION_HEADER=0`: Claude Code otherwise adds a line that changes with every request. The server can reuse the work it did for an unchanged beginning of the conversation, and that line would make it read everything again.

## 4. Compare
Do exercise 01 again with the local model, e.g. *"Fix the bug in exercises/01_fix_the_bug. Check with `pytest exercises/01_fix_the_bug`."* Compare with the cloud model: time, quality, how many tries it needs. Watch the server (LM Studio's developer logs or `docker logs -f llama-cpp`) while it works.

## Switching back
The variables live only in that terminal: close it, or remove them:

| Linux, macOS | Windows (PowerShell) |
|---|---|
| `unset ANTHROPIC_BASE_URL ANTHROPIC_API_KEY ANTHROPIC_MODEL CLAUDE_CODE_MAX_CONTEXT_TOKENS CLAUDE_CODE_ATTRIBUTION_HEADER` | `Remove-Item Env:ANTHROPIC_BASE_URL, Env:ANTHROPIC_API_KEY, Env:ANTHROPIC_MODEL, Env:CLAUDE_CODE_MAX_CONTEXT_TOKENS, Env:CLAUDE_CODE_ATTRIBUTION_HEADER` |

Stop the server, which keeps the model in memory:

- **LM Studio:** `lms server stop` and `lms unload --all`, or quit the app.
- **llama-server:** `docker compose down` in this folder.

## If something goes wrong
| Symptom | Likely cause | What to do |
|---|---|---|
| `Unable to connect to API` | The server isn't running, or the port is wrong | Check <http://localhost:1234/v1/models> or <http://localhost:8080/v1/models> |
| `Prompt is too long` | The context length is too small | A3: load with `-c 32768`; set `CLAUDE_CODE_MAX_CONTEXT_TOKENS` to the same number |
| `System message must be at the beginning` | The model's original chat template | A2, or the template in `docker-compose.yml` |
| No answer for minutes | The model is reading the prompt (see the server's log) | Use `claude --bare`, a smaller model or a GPU |
| The computer runs out of memory | The model or the context is too big for your RAM | A smaller model, or a smaller context length |

## Notes
- **With a GPU**, plain `claude` (without `--bare`) gives the model all of Claude Code's tools. Raise the context to 65 536 tokens (`-c 65536`, `--ctx-size` in `docker-compose.yml` and `CLAUDE_CODE_MAX_CONTEXT_TOKENS`), because the first request alone is about 22 000 tokens. Plain `claude` may ask once whether to use the API key: answer yes.
- **LiteLLM** ([`litellm/config.yaml`](litellm/config.yaml)) is a translator between Anthropic's API format and OpenAI's. Neither route needs it, but a server that speaks only OpenAI's format does: Claude Code → LiteLLM → server.
- **Other models** have other chat templates. We tested the Qwen3.5 models; with another model, the template may not need the fix, or may need a different one.
- **Memory rule of thumb:** a 4-bit model file is about 0.6 GB per billion parameters. A mixture-of-experts model such as Gemma 4 26B-A4B needs memory for all its 26B parameters but computes with about 4B per token, so it runs faster than its size suggests.
- Mika's full stack (llama.cpp on a Radeon VII, LiteLLM, Open WebUI, OpenCode) is in [agx-ai](https://github.com/AgenttiX/agx-ai). The biggest open models (Kimi, DeepSeek, Qwen-Max class) need a server; for those, a hosted API is the realistic option.
