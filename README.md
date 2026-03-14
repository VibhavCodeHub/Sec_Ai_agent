# Mayra AI Assistant - Like Jarvis

Platform-independent Python AI for system assistance. Voice/text, admin cmds, auto-start.

## Quick Start (Windows/Linux/Mac)

1. **Setup venv:**
   ```
   cd c:/Users/vibha/OneDrive/Documents/Desktop/Ai_agents/Sec_Ai_agent
   python -m venv mayra/venv
   # Windows:
   mayra\\venv\\Scripts\\activate
   # Linux/Mac:
   source mayra/venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Test CLI:**
   ```
   python -m mayra --cli
   ```
   Queries: "cpu usage", "list files", "weather delhi", "run ls".

3. **Install Daemon/Auto-start:**
   ```
   python -m mayra installer --install
   ```
   Restarts on boot. Wake with "mayra".

4. **Run Daemon:**
   ```
   python -m mayra daemon
   ```
   Listens for "mayra [query]".

## Features
- System info, file ops, web queries.
- Voice I/O (pyaudio mic).
- Admin elevation (prompts UAC/sudo).
- Hotkey wake.

## Config
Edit `mayra/config.json`: voice_enabled, wake_word.

**Note:** Mic access required for voice. Admin for privileged cmds.

