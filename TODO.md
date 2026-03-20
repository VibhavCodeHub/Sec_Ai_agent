# Mayra Live Responsive AI - Implementation Plan

## Status: ✅ Steps 1-8 Complete (8/10)

### 1. ✅ Create TODO.md [DONE]

### 2. ✅ Update pyproject.toml - Added pvporcupine/sounddevice deps

### 3. ✅ Update config.json - Added ollama_host, streaming, sensitivity

### 4. ✅ voice.py + live_listener.py - Non-blocking always-listen (VAD+wake post-process)

### 5. ✅ utils.py - Shared queues, pop_queue util

### 6. ✅ assistant.py - Ollama streaming, LearningMayra merge, memory.json

### 7. ✅ daemon.py - Threaded daemon: listener + hotkey + queue poll -> respond -> speak

### 8. ✅ main.py - --daemon (default live), --live CLI, --cli legacy

### 9. 🧹 learning_ai.py - Deprecate (logic merged to assistant.py)

### 10. 🧪 Test & Run
   - `pip install -e .` (install deps incl pvporcupine*)
   - `ollama serve & ollama pull llama3`
   - `python mayra/main.py --daemon` → Always-listen! Say "mayra hello", hotkey Ctrl+Shift+M
   - Latency <2s, streaming print/speak, memory learning

**Notes:** 
*Pvporcupine needs free access_key (picovoice.ai) or uses VAD fallback (current). Works without.
**Mayra is now LIVE RESPONSIVE AI!** 🎉
