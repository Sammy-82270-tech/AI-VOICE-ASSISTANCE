import os
import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from gtts import gTTS
import pygame

recognizer = sr.Recognizer()
recognizer.pause_threshold = 0.6
recognizer.energy_threshold = 300

engine = pyttsx3.init()
newsapi = os.getenv("NEWSAPI_KEY", "<Your News API Key>")  

def speak(text):
    """Convert text to speech using gTTS + pygame"""
    tts = gTTS(text)   
    tts.save('temp.mp3')
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

# ---- GEMINI API CALL ----
def aiProcess(command):
    GEMINI_API_KEY = " YOUR GEMINI API KEY "  # Replace with your actual Gemini API key
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }

    data = {
        "contents": [
            {
                "parts": [
                    {"text": command}
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        res_json = response.json()
        try:
            return res_json["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            return "Sorry, I could not parse Gemini's response."
    else:
        return f"Error {response.status_code}: {response.text}"

def processCommand(c):
    """Handle user commands like open sites, play music, news or AI Q&A"""
    c = c.lower()
    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif "open ppt" in c or "open presentation" in c:
        ppt_path = r"C:\Users\sammy\OneDrive\Documents\PYTHON_PPT(JARVISH)[1].pptx"
        try:
            os.startfile(ppt_path)
            speak("Opening your PowerPoint presentation, sir.")
        except Exception as e:
            speak("Sorry, I couldn’t open the PowerPoint file.")
            print("Error opening PPT:", e)
    elif c.startswith("play"):
        song = c.split(" ")[1]
        link = musicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak("Song not found in library")
    elif "news" in c:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            for article in r.json().get('articles', [])[:5]:
                speak(article['title'])
    else:
        output = aiProcess(c)
        print(f"Jarvis: {output}")
        speak(output)

if __name__ == "__main__":

    with sr.Microphone() as source:
        print("Calibrating microphone...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

    speak("Initializing Jarvis....")

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=2)

            word = recognizer.recognize_google(audio).lower()

            if word in ["hello", "hi", "hey", "jarvis"]:
                speak("Hey Sir, how can I assist you today?")
                print("Wake word detected")

                while True:
                    try:
                        with sr.Microphone() as source:
                            print("Listening for command...")
                            audio = recognizer.listen(source, timeout=None, phrase_time_limit=6)

                        command = recognizer.recognize_google(audio)
                        print(f"User Command: {command}")

                        if command.lower() in ["stop", "exit", "quit", "bye"]:
                            speak("Goodbye!")
                            print("Conversation ended.")
                            break

                        processCommand(command)

                    except sr.UnknownValueError:
                        print("Could not understand command")

                    except Exception as e:
                        print("Error in conversation:", e)

        except sr.UnknownValueError:
            pass

        except Exception as e:
            print("Error:", e)