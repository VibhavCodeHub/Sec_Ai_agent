import re
import json
import sys
sys.path.insert(0, '.')
from system_utils import *
# from .voice import speak, listen  # Enable if voice

class Mayra:
    def __init__(self, config):
        self.config = config
        self.name = None
        self.intents = {
            r'hello|hey (\w+) mayra': lambda q: self.set_name(q.group(1)) or f"Hello {q.group(1)}! How can I help?",
r'(cpu|memory|system|सिस्टम|info|जानकारी)': lambda q: f"हाय {self.name or 'भाई'}, {json.dumps(get_system_info(), indent=2)}",
            r'list files? (.*)': lambda q: f"Files {self.name or ''}: " + (list_dir(q.group(1)) if q.groups()[0] else list_dir()),
            r'run (.*)': lambda q: safe_run_cmd(q.group(1)),
            r'admin (.*)': lambda q: safe_run_cmd(q.group(1), admin=True),
r'(weather|मौसम) (.*)': lambda q: web_query(q.group(1) if q.groups() else 'delhi'),
r'(.*)': lambda q: self.live_assist(q.group(1))
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
                    result = handler(match)
                    # Hindi translation fallback
                    if 'no info' in result.lower() or 'not understood' in result.lower():
                        return "समझ नहीं आया, सिस्टम info, files या weather ट्राई करें."
                    return result
                except Exception as e:
                    return f"Error: {e}"
        return "कृपया सिस्टम info, files, weather या command बोलें."

    def live_assist(self, query):
        # Live 'AI' simulation - more talkative, learns cmds
        q = query.lower()
        if 'नमस्ते' in q or 'hello' in q:
            return "नमस्ते भाई! मैं Mayra हूँ, कुछ भी पूछो - system, web, cmds, jokes, stories!"
        if 'जोक' in q or 'joke' in q:
            return "एक जोक: Python programmer ने snake देखा और कहा 'class Snake:' 😂"
        if 'कहानी' in q or 'story' in q:
            return "एक छोटी कहानी: चंद्रमा पर एक AI गया, बोला 'यहाँ WiFi नहीं!' 😅"
        if 'learn' in q or 'सीख' in q:
            self.intents[q.split()[-1]] = lambda m: 'सीख लिया command!'
            return "नया command सीख लिया! Next time use करो."
        if 'web search' in q or 'गूगल' in q:
            from system_utils import web_query
            search = q.split('search')[-1].strip() or q.split('गूगल')[-1].strip()
            return web_query(search)
        return f"भाई, '{q}' अच्छा है! System info बोलो, files list करो, मौसम पूछो या नया learn कराओ. क्या मदद चाहिए?"

    def respond(self, query):
        resp = self.process_query(query)
        # Voice disabled: if self.config['voice_enabled']: speak(resp)
        return resp

