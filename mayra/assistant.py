import re
import json
from .system_utils import *
from .voice import speak, listen

class Mayra:
    def __init__(self, config):
        self.config = config
        self.intents = {
            r'cpu|memory|system info': lambda q: json.dumps(get_system_info(), indent=2),
            r'list files? (.*)': lambda q: list_dir(q.group(1)) if q.groups()[0] else list_dir(),
            r'run (.*)': lambda q: safe_run_cmd(q.group(1)),
            r'admin (.*)': lambda q: safe_run_cmd(q.group(1), admin=True),
            r'weather (.*)': lambda q: web_query(q),
            r'.*': lambda q: "I can help with system info, files, commands, weather. Try 'cpu usage' or 'list files'."
        }

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
        if self.config['voice_enabled']:
            speak(resp)
        return resp

