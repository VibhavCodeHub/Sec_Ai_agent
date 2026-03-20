import threading
import time
from queue import Queue
import speech_recognition as sr
from utils import load_config, query_queue

r = sr.Recognizer()
config = load_config()
WAKE_WORD = config['wake_word']

class ListenerThread(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.running = True
        self.mic = sr.Microphone()

    def run(self):
        with self.mic as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
        print(f"🔊 Always-listening for '{WAKE_WORD}'...")
        while self.running:
            try:
                audio = r.listen(self.mic, timeout=1, phrase_time_limit=3)
                text = r.recognize_google(audio, language='hi-IN').lower()
                print("👂", text)
                if WAKE_WORD in text:
                    query = text.replace(WAKE_WORD, '').strip()
                    if query:
                        query_queue.put(query)
                        print(f"✅ Processing: {query}")
            except sr.WaitTimeoutError:
                pass
            except:
                pass
            time.sleep(0.05)

    def stop(self):
        self.running = False

def start_listener():
    listener = ListenerThread()
    listener.start()
    return listener
