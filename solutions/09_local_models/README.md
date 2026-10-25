# Solution of exercise 09: Local models

## The result
Claude Code runs as usual, but the answers come from a model on your own computer.
`/status` in the session shows `http://localhost:4000` as the base URL, and the model server's log shows the requests.
Exercise 01 still gets solved, more slowly and possibly after more attempts.

## What was going on
Claude Code is a *harness*: the program that reads files, runs commands and talks to a model.
The model is a separate service reached over HTTP. Three programs form a chain:

```text
Claude Code  --Anthropic Messages API-->  LiteLLM (port 4000)  --OpenAI-style API-->  llama.cpp or LM Studio  -->  the model
```

- **llama.cpp / LM Studio** load an open-weight model (a model whose parameters you can download, usually as a
  `.gguf` file) and serve it with an OpenAI-compatible API.
- **LiteLLM** translates. Claude Code speaks Anthropic's format; LiteLLM serves that format at `/v1/messages` and
  forwards each request in OpenAI's format. [`litellm/config.yaml`](../../exercises/09_local_models/litellm/config.yaml)
  maps the model name `local-model` to the server at `localhost:8080`.
- **Environment variables** point Claude Code at LiteLLM. An environment variable is a setting that a program
  reads from the terminal it was started in:
  - `ANTHROPIC_BASE_URL`: where to send requests instead of Anthropic's servers.
  - `ANTHROPIC_AUTH_TOKEN`: the key sent as `Authorization: Bearer ...`; here LiteLLM's `master_key`, `local`.
  - `ANTHROPIC_MODEL`: the model name to ask for.

Anthropic's documentation says it [doesn't support](https://code.claude.com/docs/en/llm-gateway) routing
Claude Code to non-Claude models. LiteLLM [documents](https://docs.litellm.ai/docs/tutorials/claude_non_anthropic_models)
the setup, but nobody guarantees that every Claude Code feature works with it, and an update can break it.

## The commands
Start the model server (LM Studio's server tab, or `docker compose -f exercises/09_local_models/docker-compose.yml up`
after editing the model path). LM Studio listens on port **1234** by default, not 8080:
then change `api_base` in `config.yaml` to `http://localhost:1234/v1`.

Install and start LiteLLM in its own environment. Installing it into the workshop's `.venv/` may change the versions
of packages the exercises rely on. LiteLLM's [documentation](https://docs.litellm.ai/docs/tutorials/claude_non_anthropic_models)
suggests `uv tool install 'litellm[proxy]'`. Then, from the workshop folder:
`litellm --config exercises/09_local_models/litellm/config.yaml --port 4000`

Point Claude Code at it, in the terminal where you start `claude`:

| Linux, macOS | Windows (PowerShell) |
|---|---|
| `export ANTHROPIC_BASE_URL=http://localhost:4000` | `$env:ANTHROPIC_BASE_URL = "http://localhost:4000"` |
| `export ANTHROPIC_AUTH_TOKEN=local` | `$env:ANTHROPIC_AUTH_TOKEN = "local"` |
| `export ANTHROPIC_MODEL=local-model` | `$env:ANTHROPIC_MODEL = "local-model"` |
| `claude` | `claude` |

According to the [gateway documentation](https://code.claude.com/docs/en/llm-gateway-protocol#requests-and-defaults-by-connection-method),
Claude Code's background tasks then also use the main model. Anything that asks for a model *alias* doesn't:
the reviewer of exercise 07 asks for `sonnet`. Set `ANTHROPIC_DEFAULT_SONNET_MODEL=local-model` (and likewise
`..._HAIKU_MODEL`, `..._OPUS_MODEL`) to send those to the local model too.

**VS Code extension:** it doesn't read the variables of your terminal. Put them in VS Code's user settings
(Ctrl+Shift+P → **Preferences: Open User Settings (JSON)**), as described in the
[gateway documentation](https://code.claude.com/docs/en/llm-gateway-connect#vs-code-extension):
```json
"claudeCode.environmentVariables": [
  { "name": "ANTHROPIC_BASE_URL", "value": "http://localhost:4000" },
  { "name": "ANTHROPIC_AUTH_TOKEN", "value": "local" },
  { "name": "ANTHROPIC_MODEL", "value": "local-model" }
]
```

## Checking each link
Check from the model end, so that a failure points at one link:

| Link | Linux, macOS | Windows (PowerShell) |
|---|---|---|
| 1. Model server | `curl http://localhost:8080/v1/models` | `Invoke-RestMethod http://localhost:8080/v1/models` |
| 2. LiteLLM | see below | see below |
| 3. Claude Code | `/status` in the session | the same |

LiteLLM, with a one-sentence request in Anthropic's format:
```bash
curl -X POST http://localhost:4000/v1/messages -H "Authorization: Bearer local" -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model": "local-model", "max_tokens": 50, "messages": [{"role": "user", "content": "Say hello."}]}'
```
```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:4000/v1/messages `
  -Headers @{ "Authorization" = "Bearer local"; "anthropic-version" = "2023-06-01" } -ContentType "application/json" `
  -Body '{"model": "local-model", "max_tokens": 50, "messages": [{"role": "user", "content": "Say hello."}]}'
```
The answer should contain the model's reply. (In Windows PowerShell, `curl` is a different command; use `curl.exe` or the lines above.)

## Switching back
The variables live only in that terminal. Close it, or remove them:

| Linux, macOS | Windows (PowerShell) |
|---|---|
| `unset ANTHROPIC_BASE_URL ANTHROPIC_AUTH_TOKEN ANTHROPIC_MODEL` | `Remove-Item Env:ANTHROPIC_BASE_URL, Env:ANTHROPIC_AUTH_TOKEN, Env:ANTHROPIC_MODEL` |

Remove any `ANTHROPIC_DEFAULT_..._MODEL` variables you set the same way. In VS Code, delete the `claudeCode.environmentVariables` entries. Your claude.ai login stays saved while the
variables are set, and Claude Code uses it again once they are gone.

## What to expect
These are expectations, not measurements from this workshop; your hardware and model decide.
- **Speed:** Claude Code sends a long system prompt and tool list with every request. A local model has to process
  it before answering, so each turn can take much longer than with the cloud model.
- **Quality:** Claude Code relies on many correct tool calls in a row. Smaller models more often call tools with wrong
  arguments, lose track of the task, or claim success without running the test. Watch for that in exercise 01.
- **Context:** set `CLAUDE_CODE_MAX_CONTEXT_TOKENS` to the context size your server actually uses, so that Claude Code
  compacts the conversation in time ([documentation](https://code.claude.com/docs/en/env-vars)).

**The memory rule of thumb** (0.6 GB per billion parameters at 4 bits) is reasonable for the model weights.
4 bits alone would be 0.5 GB, and common 4-bit files keep some tensors at higher precision. We checked file sizes
on Hugging Face: Llama 3.1 8B at Q4_K_M is 4.92 GB (0.61 GB per billion), Qwen2.5 32B at Q4_K_M is 19.9 GB (0.61),
Gemma 4 26B-A4B at Unsloth's Q4_K_M is 17.0 GB (0.65, counting 26B parameters). The context comes on top and is
not small for Claude Code: for Llama 3.1 8B, a 32k-token context needs about 4 GiB more at 16-bit precision
(keys and values: 2 × 32 layers × 8 heads × 128 numbers × 2 bytes = 128 KiB per token). So the exercise's
"8 GB VRAM → ~10B parameters" leaves little room for the long contexts Claude Code uses. A mixture-of-experts model such as Gemma 4 26B-A4B
needs memory for all 26B parameters but computes with only about 4B per token, so it runs faster than its size suggests.

## What to take away about prompting
1. With a weaker model, prompts matter more: give the exact file, the exact command to check the result, and one task at a time.
2. Check every claim of success yourself. A local model is more likely to stop early or report a test it didn't run.
3. Decide per task: private data or offline work may justify a local model; hard reasoning usually doesn't.
