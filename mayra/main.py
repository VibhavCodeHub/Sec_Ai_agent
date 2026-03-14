import click
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from assistant import Mayra
from daemon import daemon_loop
from installer import install_auto_start

def load_config():
    import json
    import os
    config_path = 'config.json'
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    return {"voice_enabled": True, "admin_mode": True, "wake_word": "mayra", "hotkey": "ctrl+shift+m"}

@click.command()
@click.option('--cli', is_flag=True, help='CLI mode')
@click.option('--daemon', is_flag=True, help='Daemon mode')
@click.option('--install', is_flag=True, help='Install auto-start')
def main(cli, daemon, install):
    config = load_config()
    mayra = Mayra(config)
    
    if install:
        install_auto_start()
        return
    
    if daemon:
        daemon_loop()
        return
    
    if cli:
        print("Mayra voice CLI ready. Speak or type 'exit'.")
        while True:
            try:
                from voice import listen
            query_voice = listen()
            if not query_voice:
                print("Voice only now. Speak!")
                continue
            query = query_voice
            except:
                query = input("You: ")
            if query.lower() == 'exit':
                break
            try:
                from voice import response_tone
                response_tone()
            except:
                pass
            resp = mayra.respond(query)
            try:
                from voice import speak
                speak(resp)
            except:
                print("Mayra:", resp)
    else:
        print("Use --cli, --daemon, or --install. Voice default on.")

if __name__ == "__main__":
    main()

