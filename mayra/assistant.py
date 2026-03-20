import re
import json
import sys
import requests
import random
from collections import defaultdict
sys.path.insert(0, '.')
from system_utils import *
from utils import load_config, query_queue, response_queue, pop_queue
from voice import speak
import threading
import time

class LearningMayra:
    def __init__(self, config):
        self.config = config
        self.memory_file = 'mayra_memory.json'
        self.memory = self.load_memory()
        self.name = "Mayra"
        self.chat_history = []

    def load_memory(self):
        try:
            with open(self.memory_file, 'r') as f:
                return defaultdict(list, json.load(f))
        except:
            return defaultdict(list)

    def save_memory(self):
        with open(self.memory_file, 'w') as f:
            json.dump(dict(self.memory), f)

    def learn(self, query, response):
        self.memory[query.lower()].append(response)
        print("✅ Learned!")

    def ollama_stream(self, query):
        try:
            url = f"{self.config['ollama_host']}/api/generate"
            payload = {
                'model': 'llama3',
                'prompt': f"You are Mayra, friendly Hindi/English AI assistant. Answer concisely: {query}",
                'stream': self.config.get('streaming_enabled', True)
            }
            response = ''
            print("🤖 Ollama streaming...")
            for line in requests.post(url, json=payload, stream=True, timeout=60).iter_lines():
                if line:
                    data = json.loads(line)
                    if 'response' in data:
                        chunk = data['response']
                        print(chunk, end='', flush=True)
                        response += chunk
                        yield chunk  # For live speak
                    if data.get('done'):
                        break
            print()
            return response
        except Exception as e:
            print(f"Ollama error: {e}")
            return None

    def process_query(self, query):
        q_lower = query.lower()
        self.chat_history.append(q_lower)

        # Streaming Ollama first
        stream_resp = self.ollama_stream(query)
        if stream_resp:
            self.learn(q_lower, stream_resp)
            return stream_resp

        # Fallback intents/learning
        if re.match(r'(cpu|memory|system|सिस्टम)', q_lower):
            return json.dumps(get_system_info(), indent=2)
        elif re.match(r'(weather|मौसम)', q_lower):
            city = q_lower.split()[-1] or 'delhi'
            return web_query(city)
        elif re.match(r'run (.*)', q_lower):
            cmd = q_lower.split('run ', 1)[1]
            return safe_run_cmd(cmd)
        elif q_lower in self.memory:
            resp = random.choice(self.memory[q_lower])
            self.learn(q_lower, resp)
            return resp
        else:
            resp = web_query(query) or "Try system info, weather, or speak naturally!"
            self.learn(q_lower, resp)
            return resp

    def respond_stream(self, query):
        resp_gen = self.process_query(query)  # For now sync; enhance later
        full_resp = ''
        if hasattr(resp_gen, '__iter__'):
            for chunk in resp_gen:
                full_resp += chunk
                # Live speak chunks
                threading.Thread(target=speak, args=(chunk,), daemon=True).start()
                time.sleep(0.1)
        else:
            full_resp = resp_gen
        response_queue.put(full_resp)
        return full_resp

# Global instance
config = load_config()
mayra = LearningMayra(config)

def respond(query):
    return mayra.respond_stream(query)
