import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLib
import requests

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
NEWS_API_KEY = "f7830caf186b4d67961c4db313278e50"
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def open_website(url):
    """Open a website using the default web browser."""
    webbrowser.open(url)

def play_music(song):
    """Play a song from the music library."""
    link = musicLib.music.get(song)
    if link:
        open_website(link)
    else:
        speak("Song not found in the library.")

def fetch_news():
    """Fetch and speak the latest news headlines."""
    try:
        response = requests.get(NEWS_API_URL, params={'country': 'in', 'apiKey': NEWS_API_KEY})
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        articles = response.json().get('articles', [])
        for article in articles:
            speak(article['title'])
    except requests.RequestException as e:
        speak(f"An error occurred while fetching news: {e}")
        print(f"News fetch error: {e}")

def process_command(command):
    """Process the voice command."""
    command = command.lower()
    if "open google" in command:
        open_website("https://google.com")
    elif "open facebook" in command:
        open_website("https://facebook.com")
    elif "open youtube" in command:
        open_website("https://youtube.com")
    elif "open linkedin" in command:
        open_website("https://linkedin.com")
    elif command.startswith("play "):
        song = command.split(" ", 1)[1]  # Get the song name after 'play'
        play_music(song)
    elif "news" in command:
        fetch_news()
    else:
        speak("Command not recognized.")

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                print("Listening for wake word 'Jarvis'...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                word = recognizer.recognize_google(audio)
                
                if word.lower() == "jarvis":
                    speak("Yes?")
                    print("Jarvis Active... Listening for command...")
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
                    command = recognizer.recognize_google(audio)
                    process_command(command)
        
        except sr.WaitTimeoutError:
            print("Timeout; no speech detected.")
        except sr.UnknownValueError:
            speak("Sorry, I did not understand the audio. Please try again.")
            print("Sorry, I did not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
