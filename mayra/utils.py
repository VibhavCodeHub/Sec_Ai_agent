import json
import os
import threading
from queue import Queue, Empty

# Shared queues for live comms
query_queue = Queue()
response_queue = Queue()

class TimeoutError(Exception):
    pass

def pop_queue(q, timeout=1.0):
    try:
        return q.get(timeout=timeout)
    except Empty:
        raise TimeoutError("Queue timeout")

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    return {
        "voice_enabled": False, 
        "admin_mode": True, 
        "wake_word": "mayra", 
        "hotkey": "ctrl+shift+m", 
        "ollama_host": "http://localhost:11434", 
        "streaming_enabled": True, 
        "hotword_sensitivity": 0.5
    }
