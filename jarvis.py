import speech_recognition as sr
import edge_tts
import asyncio
import pygame
import tempfile
import os
import datetime
import webbrowser

pygame.mixer.init()

# ---------- SPEAK FUNCTION ----------
async def async_speak(text):
    print("Jarvis:", text)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        filename = fp.name

    # Indian Male Voice
    communicate = edge_tts.Communicate(
        text=text,
        voice="en-IN-PrabhatNeural"
    )

    await communicate.save(filename)

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        await asyncio.sleep(0.1)

    pygame.mixer.music.unload()
    os.remove(filename)


def speak(text):
    asyncio.run(async_speak(text))


# ---------- LISTEN FUNCTION ----------
def take_command():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-IN")
        print("You:", query)
        return query.lower()

    except Exception:
        speak("Sorry, please say that again.")
        return ""


# ---------- GREETING ----------
hour = datetime.datetime.now().hour

if hour < 12:
    speak("Good Morning Rohan")
elif hour < 18:
    speak("Good Afternoon Rohan")
else:
    speak("Good Evening Rohan")

speak("I am Jarvis. How can I help you?")


# ---------- MAIN LOOP ----------
while True:

    query = take_command()

    if query == "":
        continue

    # Greetings
    if "hello" in query or "hi" in query:
        speak("Hello Rohan. How are you?")

    elif "how are you" in query:
        speak("I am fine. Thank you for asking.")

    elif "who are you" in query:
        speak("I am Jarvis, your personal assistant.")

    elif "your name" in query:
        speak("My name is Jarvis.")

    # Your details
    elif "my details" in query or "tell my details" in query:
        speak(
            "Your name is Rohan Mondal. "
            "You are a B Tech student and an aspiring Full Stack Developer."
        )

    # Time
    elif "time" in query:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak("The time is " + current_time)

    # Date
    elif "date" in query:
        today = datetime.datetime.now().strftime("%d %B %Y")
        speak("Today is " + today)

    # Open Chrome
    elif "open chrome" in query:
        speak("Opening Chrome")
        webbrowser.open("https://www.google.com")

    # Open YouTube
    elif "open youtube" in query:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    # Open Google
    elif "open google" in query:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    # Open GitHub
    elif "open github" in query:
        speak("Opening GitHub")
        webbrowser.open("https://github.com")

    # Search
    elif "search" in query:
        search_term = query.replace("search", "")
        speak("Searching " + search_term)
        webbrowser.open(
            f"https://www.google.com/search?q={search_term}"
        )

    # Joke
    elif "tell me a joke" in query:
        speak(
            "Why do programmers prefer dark mode? "
            "Because light attracts bugs."
        )

    # Exit
    elif "exit" in query or "stop" in query:
        speak("Goodbye Rohan. Have a nice day.")
        break

    else:
        speak("Sorry, I don't know that command yet.")

        