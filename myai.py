import pyttsx3
import speech_recognition as sr
import openai
from googletrans import Translator
import webbrowser
import os
import datetime
import smtplib
from email.mime.text import MIMEText
import pyautogui
import time
import random
# from distutils.version import LooseVersion
from email.mime.multipart import MIMEMultipart

# Initialize the speech engine and translator
engine = pyttsx3.init()
translator = Translator()
openai.api_key = "Your api key"
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 50)  # Adjust this value as needed
voices = engine.getProperty('voices')
# Choose a different voice by index, e.g., 0 for male, 1 for female
engine.setProperty('voice', voices[0].id)  # Changing to female voice


# Function to speak
def speak(text):
    engine.say(text)
    engine.runAndWait()


# Function to listen to user's command
def listen(lang='en'):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language="en-in")
        print(f"User said: {query}")
        return query.lower()
    except Exception as e:
        print(f"Say that again please... Error: {e}")
        return "None"


# Function to get a response from OpenAI
def get_response(query):
    try:
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=query,
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I couldn't process your request."


# Function to send email
def send_email(to, subject, body):
    try:
        from_email = "your_email@example.com"
        from_password = "your_email_password"
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to, text)
        server.quit()
        speak("Email has been sent successfully.")
    except Exception as e:
        speak(f"Sorry, I was unable to send the email. {e}")


# Function to store learning data
def store_learning(data):
    with open('jarvis_learning.txt', 'a') as f:
        f.write(data + '\n')
    speak("I've learned that!")

def click_youtube_video(video_name):
    webbrowser.open(f"https://www.youtube.com/results?search_query={video_name}")
    time.sleep(3)  # Wait for the page to load
    pyautogui.click(600, 350)  # Adjust coordinates based on your screen resolution

#C:\Users\anshu\OneDrive\Desktop\vs code\.vs\school
# Function to retrieve learning data
def retrieve_learning(query):
    try:
        with open('jarvis_learning.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if query in line:
                    return line.strip()
        return "I don't remember learning that."
    except FileNotFoundError:
        return "I don't have any learning data yet."

# MY mood music 
def music_mood(query):
        speak("sir aaap konsa gana sunna chaahte ho...")
        query = listen()
        if "as your wish" in query:
            music_dir = "path_to_music_directory"
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, random.songs[0,-1]))
        else:
            speak("music is not Available in music folder   can i play song on web")
            if "yes" in query:
                speak("Tell me siddhu which song you want to play")
                song = listen()
                click_youtube_video(song)
                # click_youtube_video(song)
            else:
                return
def res():
    speak("what you wnat to search")
    query = listen
    if "what is " or "who is" in query:
        webbrowser.open("https://www.google.com/search?q={query}")




if __name__ == "__main__":
    speak("Hello sir, I am Jarvis AI assistant, How can i help you")
    while True:
        query = listen('en')

        if query == "None":
            continue

        if "search" in query:
            search_term = query.replace("search", "").strip()
            webbrowser.open(f"https://www.google.com/search?q={search_term}")
            speak(f"Searching for {search_term}")

        # elif "play music" in query:
        #     music_dir = "path_to_music_directory"
        #     songs = os.listdir(music_dir)
        #     os.startfile(os.path.join(music_dir, songs[0]))

        elif "r u" in query:
            speak("I am Jarvis, the most advanced AI system, created by Siddharth.")

        elif "learn" in query:
            speak("What should I learn?")
            learning_data = listen('en')
            store_learning(learning_data)
        
        elif "play music" in query:
            music_mood(query)
 
        elif "what time " and "whats time"  in query:
            time_str = datetime.datetime.now().strftime("%H:%M:%S")
            print(time_str)
            speak(f"The current time is {time_str}")

        elif "send email" in query:
            try:
                speak("What should be the subject?")
                subject = listen()
                speak("What should I write in the email?")
                body = listen()
                speak("Whom should I send it to?")
                to = "recipient_email@example.com"  # Replace with actual recipient
                send_email(to, subject, body)
            except Exception as e:
                speak("Sorry, I was unable to send the email.")
        elif 'play song' in query:
            speak("Tell me siddhu which song you want to play")
            song = listen()
            click_youtube_video(song)
            click_youtube_video(song)
    
        elif "what is" or "who is " in query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
        elif "what is " in query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            speak

        elif "open" in query:
            if "youtube" in query:
                webbrowser.open("https://www.youtube.com")
            elif "google" in query:
                webbrowser.open("https://www.google.com")
            elif "instagram" in query:
                webbrowser.open("https://www.instagram.com/")

        elif "quit" in query:
            speak("Goodbye!")
            break

        else:
            learned_response = retrieve_learning(query)
            if "I don't remember learning that." in learned_response:
                response = get_response(query)
                speak(response)
            else:
                speak(learned_response)
