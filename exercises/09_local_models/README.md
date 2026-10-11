# Exercise 09: Local models (15 min, optional, advanced)
The harness is separate from the model. Claude Code can talk to any server that speaks the Anthropic Messages API,
and [LiteLLM](https://www.litellm.ai/) can translate that to an OpenAI-compatible local server such as
[llama.cpp](https://github.com/ggml-org/llama.cpp), [LM Studio](https://lmstudio.ai/) or Ollama.

Why: privacy (the data never leaves the machine), no rate limits, offline use, cost.
What you give up: capability and speed. An open-weight model that fits on a laptop is roughly where the cloud
models were 1–2 years ago, which is still remarkably useful for many tasks.

## Task
1. Run a local model server. Options, from easiest to most flexible:
   - LM Studio: download a model (e.g. a Gemma 4 or Qwen 3.8 variant that fits your RAM/VRAM), start the server.
   - llama.cpp: `docker compose up` with the example `docker-compose.yml` here (edit the model path).
   Check it works: `curl http://localhost:8080/v1/models`.
2. Run LiteLLM as the translating proxy with the example `litellm/config.yaml`:
   ```bash
   pip install 'litellm[proxy]'
   litellm --config exercises/09_local_models/litellm/config.yaml --port 4000
   ```
3. Point Claude Code at the proxy:
   ```bash
   # Linux, macOS
   export ANTHROPIC_BASE_URL=http://localhost:4000
   export ANTHROPIC_AUTH_TOKEN=local
   export ANTHROPIC_MODEL=local-model
   claude
   ```
   ```powershell
   # Windows (PowerShell)
   $env:ANTHROPIC_BASE_URL = "http://localhost:4000"
   $env:ANTHROPIC_AUTH_TOKEN = "local"
   $env:ANTHROPIC_MODEL = "local-model"
   claude
   ```
4. Do exercise 01 again with the local model and compare: time, quality, how many tries it needs.

## Notes
- Mika's full stack (llama.cpp on a Radeon VII, LiteLLM, Open WebUI, Claude Code through the proxy) is in
  [agx-ai](https://github.com/AgenttiX/agx-ai).
- Hardware rules of thumb: a 4-bit quantized model needs roughly 0.6 GB of memory per billion parameters plus
  the context. 8 GB VRAM → ~10B parameters; a 24–32 GB GPU → ~30B or a mixture-of-experts model like Gemma 4 26B-A4B.
- The biggest open models (Kimi, DeepSeek, Qwen-Max class) need a server; for those, a hosted API is the realistic option.
