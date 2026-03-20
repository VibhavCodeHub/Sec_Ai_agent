# Mayra Live Responsive AI - Implementation Plan

## Status: 📋 Planned (0/9 complete)

### 1. ✅ Create TODO.md [DONE]

### 2. 📝 Update pyproject.toml - Add pvporcupine, sounddevice (for better audio), queue backport if needed
### 3. 💾 Update config.json - Add ollama_host, hotword_sensitivity, enable_streaming
### 4. 🔊 voice.py - Implement non-blocking hotword listener with pvporcupine threading, VAD fallback, response queue
### 5. 🧠 utils.py - Add shared Threading.Queue for inter-module comms
### 6. 🤖 assistant.py - Integrate Ollama streaming API, merge LearningMayra (memory, process), live_assist streaming
### 7. 🔄 daemon.py - Threaded always-on: hotword listener + keyboard hotkey -> queue query -> assistant -> speak/print
### 8. 🚀 main.py - --daemon uses new daemon_loop, --live for continuous CLI with listener
### 9. 🧹 Refactor learning_ai.py - Deprecate standalone, import to assistant
### 10. 🧪 Test & Install
   - pip install -e .
   - ollama pull llama3 (if not)
   - python mayra/main.py --daemon
   - Verify: always-listen (say "mayra what time"), hotkey, streaming resp, low latency

**Next: Approve deps update? Run pip sync? Note: Skip porcupine if no key (VAD-only).**
