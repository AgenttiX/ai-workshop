# Solution of exercise 09: Local models

## The result
Claude Code runs as usual, but the answers come from a model on your own computer. `/status` in the session shows the local address (`http://localhost:1234` or `http://localhost:8080`) as the base URL, and the model server's log shows each request arriving. Exercise 01 can still get solved, more slowly and possibly after more attempts.

## What was going on
Claude Code is a *harness*: the program that reads files, runs commands and talks to a model. The model is a separate service reached over HTTP. With a local model, the chain is:

```text
Claude Code  --Anthropic Messages API-->  LM Studio or llama-server  -->  chat template  -->  llama.cpp  -->  the weights
```

- **LM Studio / llama-server** load an open-weight model (a model whose parameters you can download, usually as a `.gguf` file) and answer requests in Anthropic's format at `/v1/messages`. Both have llama.cpp inside, the program that does the actual computation.
- **The chat template** turns the list of messages into the one string the model reads, with markers such as `<|im_start|>user`.
- **Environment variables** point Claude Code at the server. An environment variable is a setting that a program reads from the terminal it was started in:
    - `ANTHROPIC_BASE_URL`: where to send requests instead of Anthropic's servers.
    - `ANTHROPIC_API_KEY`: the key sent with each request. The local servers don't check it, but `claude --bare` refuses to start without one.
    - `ANTHROPIC_MODEL`: the model name to ask for. LM Studio uses it to pick the model; llama-server serves one model and ignores it.

Anthropic's documentation says it [doesn't support](https://code.claude.com/docs/en/llm-gateway) routing Claude Code to non-Claude models. It worked in our tests, but nobody guarantees that every Claude Code feature works, and an update can break it.

## Why the exercise needed three fixes
We measured these on 27 October 2026 with Claude Code 2.1.285 and Qwen3.5 models on a laptop without a dedicated GPU (Intel i5-1145G7, 16 GB of RAM). The slide *Why local models misbehave, in numbers* has the math.

1. **The context length.** llama-server reserves memory for the model's maximum context unless told otherwise: 262 144 tokens for Qwen3.5, which took 11 GiB for the 9B model and left 0.8 GiB of the 16 GB free. With `--ctx-size 32768` it was about 4 GiB. LM Studio has the opposite default, 8 192 tokens, and Claude Code refuses to start with `Prompt is too long`.
2. **The chat template.** Claude Code sends a second system message later in the conversation (with today's date), and the Qwen3.5 template stops with `System message must be at the beginning`. This happened with both servers, and it's a known open issue ([llama.cpp #27367](https://github.com/ggml-org/llama.cpp/issues/27367)). The fix in [`qwen35-claude-code.jinja`](../../exercises/09_local_models/qwen35-claude-code.jinja) changes one line, so that the template renders the message instead of stopping. Other models have other templates: the one of Gemma 4 E4B, for example, doesn't contain this check.
3. **Thinking.** Qwen3.5 writes its reasoning before the answer, at the same few tokens per second. In our test, a 300-token limit ran out during the thinking, and the answer was empty. `docker-compose.yml` turns thinking off. In LM Studio it stays on unless you turn it off, which makes every answer slower.

`CLAUDE_CODE_ATTRIBUTION_HEADER=0` is a speed setting. The server reuses its work for an unchanged beginning of the conversation (the *prefix cache*), and Claude Code otherwise adds a line that changes with every request near the beginning. Unsloth's guide reports that it makes local models much slower ([Unsloth](https://unsloth.ai/docs/basics/api/claude-code.md)); we checked that the line is gone with the setting, not how much time it saves.

## Checking each link
Check from the model end, so that a failure points at one link. Use port 1234 for LM Studio and 8080 for llama-server.

| Link | Linux, macOS | Windows (PowerShell) |
|---|---|---|
| 1. Model server | `curl http://localhost:1234/v1/models` | `Invoke-RestMethod http://localhost:1234/v1/models` |
| 2. Claude Code's format | see below | see below |
| 3. Claude Code | `/status` in the session | the same |

A one-sentence request in Anthropic's format, as Claude Code sends it:

```bash
curl -X POST http://localhost:1234/v1/messages -H "anthropic-version: 2023-06-01" -H "content-type: application/json" \
  -d '{"model": "qwen3.5-4b", "max_tokens": 1000, "messages": [{"role": "user", "content": "Say hello."}]}'
```

```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:1234/v1/messages `
  -Headers @{ "anthropic-version" = "2023-06-01" } -ContentType "application/json" `
  -Body '{"model": "qwen3.5-4b", "max_tokens": 1000, "messages": [{"role": "user", "content": "Say hello."}]}'
```

The answer should contain the model's reply. With thinking on, the model first writes its reasoning; if `max_tokens` is too small, only that fits and the text is missing. (In Windows PowerShell, `curl` is a different command; use `curl.exe` or the lines above.)

## Letting the cloud model fix the rest
A local setup has many small parts, and the error messages are often cryptic. That's a good task for the cloud model: open another terminal *without* the variables, start `claude` in the workshop folder, and give it the problem, e.g.

- *"I'm doing exercise 09 with LM Studio. Claude Code says `API Error: 500 … System message must be at the beginning`. What does it mean and how do I fix it?"*
- *"Check whether my llama-server in Docker works: run the checks of solutions/09_local_models/README.md and read `docker logs llama-cpp`."*
- *"The model takes minutes to answer. Read the server log and tell me where the time goes."*

It can run the checks itself, read the logs and the exercise files, and look up the documentation. As always, check what it changes, and give it the exact symptom, not your guess about the cause.

## What to expect
- **Speed:** on our laptop, the 9B model read the prompt at 24–80 tokens per second, and the models wrote 25 (2B), 9 (4B) or 5 (9B) tokens per second. Claude Code sends its instructions and tool descriptions with every request: about 22 000 tokens in plain `claude`, about 1 300 in `claude --bare`. Reading 22 000 tokens at 24 per second takes about 15 minutes; `claude --bare` answered a short question after 29 s. A GPU is much faster at both.
- **Quality:** Claude Code relies on many correct tool calls in a row. Smaller models more often call tools with wrong arguments, lose track of the task, or claim success without running the test. Watch for that in exercise 01.
- **Context:** `CLAUDE_CODE_MAX_CONTEXT_TOKENS` tells Claude Code the context length of the server, so that it compacts the conversation in time ([documentation](https://code.claude.com/docs/en/env-vars)).
- **Other names:** Anything in Claude Code that asks for a model *alias* uses that alias, not `ANTHROPIC_MODEL`: the reviewer of exercise 07 asks for `sonnet`. Set `ANTHROPIC_DEFAULT_SONNET_MODEL` (and likewise `..._HAIKU_MODEL`, `..._OPUS_MODEL`) to the local model's name to send those to it too ([gateway documentation](https://code.claude.com/docs/en/llm-gateway-protocol#requests-and-defaults-by-connection-method)).

**The memory rule of thumb** (0.6 GB per billion parameters at 4 bits) holds for the model files: Qwen3.5-9B at Q4_K_M is 5.68 GB, Qwen3.5-4B 2.74 GB, Qwen3.5-2B 1.28 GB. The context comes on top: for Qwen3.5-9B, 32 KiB per token (only 8 of its 32 layers keep keys and values for every token), i.e. 1 GiB for 32 768 tokens.

## LiteLLM
[LiteLLM](https://www.litellm.ai/) translates Anthropic's format to OpenAI's, which most model servers speak. LM Studio (0.4.1 and later) and llama-server speak Anthropic's format themselves, so the exercise doesn't need it. For a server that speaks only OpenAI's format, [`litellm/config.yaml`](../../exercises/09_local_models/litellm/config.yaml) maps the model name `local-model` to a server at `localhost:8080`. Install LiteLLM in its own environment, not in the workshop's `venv/`, whose package versions the exercises rely on:

```bash
uv tool install 'litellm[proxy]'
litellm --config exercises/09_local_models/litellm/config.yaml --port 4000
```

Then point Claude Code at `http://localhost:4000` with `ANTHROPIC_API_KEY=local` (LiteLLM's `master_key`).

## VS Code extension
The extension doesn't read the variables of your terminal. Put them in VS Code's user settings (Ctrl+Shift+P → **Preferences: Open User Settings (JSON)**), as described in the [gateway documentation](https://code.claude.com/docs/en/llm-gateway-connect#vs-code-extension), and remove them afterwards:

```json
"claudeCode.environmentVariables": [
  { "name": "ANTHROPIC_BASE_URL", "value": "http://localhost:1234" },
  { "name": "ANTHROPIC_API_KEY", "value": "local" },
  { "name": "ANTHROPIC_MODEL", "value": "qwen3.5-4b" },
  { "name": "CLAUDE_CODE_MAX_CONTEXT_TOKENS", "value": "32768" },
  { "name": "CLAUDE_CODE_ATTRIBUTION_HEADER", "value": "0" }
]
```

## What to take away about prompting
1. With a weaker model, prompts matter more: give the exact file, the exact command to check the result, and one task at a time.
2. Check every claim of success yourself. A local model is more likely to stop early or report a test it didn't run.
3. Decide per task: private data or offline work may justify a local model; hard reasoning usually doesn't.
4. When the setup itself breaks, ask the cloud model: it's good at reading logs and error messages.
