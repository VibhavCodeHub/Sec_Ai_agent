import speech_recognition as sr
import pyttsx3
import platform
import winsound  # Windows tone fallback

r = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    print("Mayra:", text)
    engine.say(text)
    engine.runAndWait()
    response_tone()

def response_tone():
    if platform.system() == 'Windows':
        winsound.Beep(1000, 200)  # Activate beep

def activate_tone():
    response_tone()

def listen():
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            print("Listening...")
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            text = r.recognize_google(audio, language='hi-IN').lower()
            print("Heard:", text)
            return text
    except:
        return ""

# Default name "Mayra"

