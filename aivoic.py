import pyttsx3
import speech_recognition as sr
import nltk
from nltk.tokenize import word_tokenize
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio)
            print(f"You said: {query}")
            return query
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return ""

nltk.download('punkt')

def process_text(text):
    tokens = word_tokenize(text)
    return tokens
def ai_assistant():
    while True:
        query = listen()
        if 'exit' in query:
            speak("Goodbye!")
            break
        else:
            response = "You said: " + query  # Add logic for more complex responses
            speak(response)

if __name__ == "__main__":
    ai_assistant()
