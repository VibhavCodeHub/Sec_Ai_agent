import time
import keyboard
import json
from .config import config  # Wait, import from file
from .voice import listen
from .assistant import Mayra

def load_config():
    with open('mayra/config.json') as f:
        return json.load(f)

def daemon_loop():
    config = load_config()
    mayra = Mayra(config)
    print("Mayra daemon running. Wake with 'mayra' or hotkey.")
    
    while True:
        # Hotkey check
        if keyboard.is_pressed(config['hotkey']):
            query = input("Mayra: ") or listen()
            if query.startswith(config['wake_word']):
                query = query[len(config['wake_word'])+1:]
                print(mayra.respond(query))
        
        # Voice listen loop (non-blocking attempt)
        if config['voice_enabled']:
            query = listen()
            if query and config['wake_word'] in query:
                query = query.split(config['wake_word'])[1].strip()
                print(mayra.respond(query))
        
        time.sleep(0.1)

