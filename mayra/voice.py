import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()
recognizer = sr.Recognizer()

import platform
import winsound  # Windows beep fallback
try:
    import simpleaudio as sa
TONE_ACTIVATE = None  # Skip file
except:
    TONE_ACTIVATE = None

def activate_tone():
    if TONE_ACTIVATE:
        play_obj = TONE_ACTIVATE.play()
        play_obj.wait_done()
    else:
        if platform.system() == 'Windows':
            winsound.Beep(800, 200)  # Activate beep

def response_tone():
    if platform.system() == 'Windows':
        winsound.Beep(600, 100)  # Response ding

def speak(text):
    response_tone()
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=1)
        try:
            return recognizer.recognize_google(audio).lower()
        except:
            return ""

