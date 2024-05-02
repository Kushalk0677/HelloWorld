import os
import webbrowser
import requests
import datetime
import smtplib
import pyttsx3
import speech_recognition as sr

# Initialize speech recognition
recognizer = sr.Recognizer()

# Initialize text-to-speech engine
engine = pyttsx3.init()


def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            query = recognizer.recognize_google(audio)
            return query.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Can you please repeat?")
            return listen()
        except sr.RequestError:
            speak("Sorry, I'm unable to access the speech recognition service at the moment.")
            return None


def open_application(application_name):
    try:
        os.startfile(application_name)
        speak(f"Opening {application_name}")
    except Exception as e:
        speak("Sorry, I couldn't open the application.")


def search_google(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speak("Here are the search results for your query on Google.")


def search_youtube(query):
    url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(url)
    speak("Here are the search results for your query on YouTube.")


def search_wikipedia(query):
    url = f"https://en.wikipedia.org/wiki/{query}"
    webbrowser.open(url)
    speak("Here are the search results for your query on Wikipedia.")


def get_weather(location):
    api_key = "YOUR_WEATHER_API_KEY"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    if data["cod"] == 200:
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        speak(
            f"The weather in {location} is {weather_description} with a temperature of {temperature} degrees Celsius.")
    else:
        speak("Sorry, I couldn't fetch the weather information for that location.")


def get_current_time_and_date():
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")
    current_date = now.strftime("%A, %B %d, %Y")
    speak(f"The current time is {current_time} and the current date is {current_date}.")


def send_email(subject, body, recipient_email):
    # Configure SMTP server settings
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "YOUR_EMAIL_ADDRESS"
    sender_password = "YOUR_EMAIL_PASSWORD"

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(sender_email, recipient_email, message)
        server.quit()
        speak("Email sent successfully.")
    except Exception as e:
        speak("Sorry, I couldn't send the email.")


def play_music(song_path):
    try:
        os.startfile(song_path)
        speak("Playing music.")
    except Exception as e:
        speak("Sorry, I couldn't play the music.")


def solve_math_problem(problem):
    try:
        solution = eval(problem)
        speak(f"The solution to the problem is {solution}.")
    except Exception as e:
        speak("Sorry, I couldn't solve the problem.")


def system_command(command):
    try:
        os.system(command)
        speak(f"Executing {command}.")
    except Exception as e:
        speak("Sorry, I couldn't execute the command.")


def assistant():
    speak("Hello! How can I assist you today?")

    while True:
        query = listen()

        if query:
            if "open" in query:
                application_name = query.replace("open ", "")
                open_application(application_name)
            elif "search on google" in query:
                query = query.replace("search on google ", "")
                search_google(query)
            elif "search on youtube" in query:
                query = query.replace("search on youtube ", "")
                search_youtube(query)
            elif "search on wikipedia" in query:
                query = query.replace("search on wikipedia ", "")
                search_wikipedia(query)
            elif "weather update" in query:
                location = query.replace("weather update for ", "")
                get_weather(location)
            elif "current time and date" in query:
                get_current_time_and_date()
            elif "send email" in query:
                speak("What is the subject of the email?")
                subject = listen()
                speak("What is the body of the email?")
                body = listen()
                speak("What is the recipient's email address?")
                recipient_email = listen()
                send_email(subject, body, recipient_email)
            elif "play music" in query:
                speak("Please provide the path to the music file.")
                song_path = listen()
                play_music(song_path)
            elif "solve" in query:
                speak("What is the math problem you would like me to solve?")
                problem = listen()
                solve_math_problem(problem)
            elif "restart" in query:
                system_command("shutdown /r /t 1")
            elif "sleep" in query:
                system_command("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            elif "shut down" in query:
                system_command("shutdown /s /t 1")
            elif "exit" in query or "bye" in query:
                speak("Goodbye!")
                break
            else:
                speak("I'm sorry, I didn't understand that.")


if __name__ == "__main__":
    assistant()
