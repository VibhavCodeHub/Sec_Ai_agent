import speech_recognition as sr
import pyttsx3
import platform
import winsound
import threading
from utils import response_queue, load_config, pop_queue

r = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 180)  # Faster for responsive

config = load_config()

def speak(text):
    print("🎤 Mayra:", text)
    engine.say(text)
    engine.runAndWait()
    response_tone()

def response_tone():
    if platform.system() == 'Windows':
        winsound.Beep(1200, 150)
        winsound.Beep(1000, 150)

def activate_tone():
    threading.Thread(target=response_tone, daemon=True).start()

def listen_blocking():
    """Legacy blocking listen"""
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            text = r.recognize_google(audio, language='hi-IN').lower()
            print("Heard:", text)
            return text
    except:
        return ""

# Always-on listener - use live_listener.py for daemon
