import json
import re
from collections import defaultdict
import random
from system_utils import *
from voice import speak, listen

class LearningMayra:
    def __init__(self):
        self.memory_file = 'mayra_memory.json'
        self.memory = self.load_memory()
        self.learned_cmds = {}
        self.chat_history = []
        self.name = "Mayra"

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
        print("Learned!")

def process(self, query):
        print("Thinking...")
        q_lower = query.lower()
        self.chat_history.append(q_lower)
        # Intelligent API - Grok/OpenAI fallback
        resp = self.grok_api(query)
        if resp:
            self.learn(q_lower, resp)
            return resp
        # System/ML intents
        if re.match(r'(cpu|memory|system|सिस्टम)', q_lower):
            resp = json.dumps(get_system_info())
        elif re.match(r'(weather|मौसम)', q_lower):
            city = q_lower.split()[-1] if len(q_lower.split()) >1 else 'delhi'
            resp = web_query(city)
        elif re.match(r'learn |सीख', q_lower):
            cmd = ' '.join(q_lower.split()[1:])
            self.learned_cmds[cmd.split()[-1]] = cmd
            resp = "सीख लिया भाई! अब बोलो."
        elif re.match(r'run |चला', q_lower):
            cmd = ' '.join(q_lower.split()[1:])
            resp = safe_run_cmd(cmd)
        else:
            # Learned memory
            if q_lower in self.memory:
                resp = random.choice(self.memory[q_lower])
            else:
                resp = web_query(query) or f"Web se info मिला: {query}"
                self.learn(q_lower, resp)
                print(f"Web learned: {resp}")
        self.learn(q_lower, resp)
        return resp

    def grok_api(self, query):
        try:
            # Use Grok API or Ollama local (install ollama, model: llama3)
            import requests
            # Replace with your API key or local Ollama
            url = 'http://localhost:11434/api/generate'  # Ollama local
            payload = {
                'model': 'llama3',  # Download via ollama pull llama3
                'prompt': f"Answer in Hindi/English: {query}",
                'stream': False
            }
            resp = requests.post(url, json=payload, timeout=30).json()
            return resp['response']
        except:
            return None

    def run_loop(self):
        print("Mayra learning AI live! Speak anything.")
        while True:
            query = listen()
            if not query or 'exit' in query.lower():
                self.save_memory()
                break
            resp = self.process(query)
            speak(resp)

if __name__ == '__main__':
    ai = LearningMayra()
    ai.run_loop()

