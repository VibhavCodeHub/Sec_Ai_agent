import re
import json
from .system_utils import *
# from .voice import speak, listen  # Enable if voice

class Mayra:
    def __init__(self, config):
        self.config = config
        self.name = None
        self.intents = {
            r'hello|hey (\w+) mayra': lambda q: self.set_name(q.group(1)) or f"Hello {q.group(1)}! How can I help?",
            r'cpu|memory|system info': lambda q: f"Hi {self.name or 'user'}, " + json.dumps(get_system_info(), indent=2),
            r'list files? (.*)': lambda q: f"Files {self.name or ''}: " + (list_dir(q.group(1)) if q.groups()[0] else list_dir()),
            r'run (.*)': lambda q: safe_run_cmd(q.group(1)),
            r'admin (.*)': lambda q: safe_run_cmd(q.group(1), admin=True),
            r'weather (.*)': lambda q: web_query(q),
            r'.*': lambda q: f"Hello {self.name or 'there'}! I can help with system info, files, commands, weather. Try 'cpu usage'."
        }

    def set_name(self, name):
        self.name = name.capitalize()
        return f"Name set to {self.name}"

    def process_query(self, query):
        query = query.lower()
        for pattern, handler in self.intents.items():
            match = re.match(pattern, query)
            if match:
                try:
                    return handler(match)
                except Exception as e:
                    return f"Error: {e}"
        return "Sorry, not understood."

    def respond(self, query):
        resp = self.process_query(query)
        # Voice disabled: if self.config['voice_enabled']: speak(resp)
        return resp

