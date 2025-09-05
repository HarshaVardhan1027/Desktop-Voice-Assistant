import speech_recognition as sr
import pyttsx3
import wikipedia
import webbrowser
import os
import pyjokes
import time
import pyautogui
import keyboard
import threading
import re
import subprocess
from urllib.parse import quote_plus
from playsound import playsound

# Initialize TTS engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 180)

exit_flag = False

def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def wish_me():
    playsound("C:\\Users\\Harsha\\voice-desktop-assistant\\JARVIS - Marvel's Iron Man 3 Second Screen Experience - Trailer.mp3")
    time.sleep(0.2)  # very small wait
    speak("Hi, I am Jarvis. How can I help you?")

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=6)
        except sr.WaitTimeoutError:
            return "none"
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
    except sr.UnknownValueError:
        speak("Sorry, I didn’t catch that.")
        return "none"
    except sr.RequestError:
        speak("Speech service is unavailable.")
        return "none"
    return query.lower()

def write_to_notepad(text):
    subprocess.Popen("notepad.exe")
    time.sleep(0.5)  # wait for notepad to open
    pyautogui.click(x=700, y=400)  # ensures notepad is in focus (adjust x/y if needed)
    keyboard.write(text, delay=0)  # fastest typing method

def handle_command(command):
    if "wikipedia" in command and "open" not in command:
        speak("Searching Wikipedia...")
        topic = command.replace("wikipedia", "").strip()
        try:
            summary = wikipedia.summary(topic, sentences=2)
            speak("According to Wikipedia:")
            speak(summary)
        except:
            speak("Sorry, I couldn't find a summary.")

    elif "open wikipedia page" in command:
        speak("What topic should I open on Wikipedia?")
        topic = take_command()
        if topic != "none":
            try:
                page = wikipedia.page(topic)
                summary = wikipedia.summary(topic, sentences=2)
                sections = page.sections
                speak("Here's the summary:")
                speak(summary)
                top_points = ", ".join(sections[:5])
                speak("Main topics are: " + top_points)
            except:
                speak("Could not fetch full Wikipedia data.")

    elif "write this to notepad" in command or "note this down" in command:
        speak("What should I write in Notepad?")
        content = take_command()
        if content != "none":
            write_to_notepad(content)
            speak("Done writing to Notepad.")

    elif "calculate" in command:
        speak("What calculation should I perform?")
        expression = take_command()
        if expression != "none":
            try:
                result = eval(expression)
                speak(f"The result is {result}")
            except:
                speak("Sorry, I couldn't compute that.")

    elif "play" in command and "video" in command:
        match = re.search(r"play (.+?) video.*?(\d+)\s*(seconds|minutes)?", command)
        if match:
            search = match.group(1)
            time_val = int(match.group(2))
            unit = match.group(3)
            seconds = time_val * 60 if unit and "minute" in unit else time_val
            speak(f"Opening {search} video at {seconds} seconds")
            webbrowser.open(f"https://www.youtube.com/results?search_query={quote_plus(search)}")
        else:
            speak("What video should I search?")
            video = take_command()
            if video != "none":
                webbrowser.open(f"https://www.youtube.com/results?search_query={quote_plus(video)}")

    elif "joke" in command:
        speak(pyjokes.get_joke())

    elif "open notepad" in command:
        os.system("notepad")

    elif "open calculator" in command:
        os.system("calc")

    elif "open chrome" in command:
        chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        if os.path.exists(chrome_path):
            speak("Opening Chrome")
            os.startfile(chrome_path)
        else:
            speak("Chrome not found.")

    elif "google search" in command or "search google for" in command:
        speak("What should I search for on Google?")
        term = take_command()
        if term != "none":
            webbrowser.open(f"https://www.google.com/search?q={quote_plus(term)}")

    elif "exit" in command or "quit" in command or "stop" in command:
        speak("Goodbye! Have a nice day.")
        exit()

    else:
        speak("Sorry, I didn’t understand that command.")

def listen_for_exit():
    global exit_flag
    keyboard.wait("ctrl+q")
    exit_flag = True

# Main
if __name__ == "__main__":
    wish_me()
    speak("Press Control + Q anytime to exit.")
    threading.Thread(target=listen_for_exit, daemon=True).start()

    while True:
        if exit_flag:
            speak("Exiting on keyboard command. Goodbye!")
            break
        query = take_command()
        if query != "none":
            handle_command(query)
