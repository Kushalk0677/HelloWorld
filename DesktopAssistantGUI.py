import os
import webbrowser
import requests
import datetime
import smtplib
import pyttsx3
import speech_recognition as sr
import tkinter as tk

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


def open_application():
    application_name = app_entry.get().lower()
    try:
        os.startfile(application_name)
        speak(f"Opening {application_name}")
    except Exception as e:
        speak("Sorry, I couldn't open the application.")


def search_google():
    query = app_entry.get().lower()
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speak("Here are the search results for your query on Google.")


def search_youtube():
    query = app_entry.get().lower()
    url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(url)
    speak("Here are the search results for your query on YouTube.")


def search_wikipedia():
    query = app_entry.get().lower()
    url = f"https://en.wikipedia.org/wiki/{query}"
    webbrowser.open(url)
    speak("Here are the search results for your query on Wikipedia.")


def get_weather():
    location = app_entry.get().lower()
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


def send_email():
    # Configure SMTP server settings
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "YOUR_EMAIL_ADDRESS"
    sender_password = "YOUR_EMAIL_PASSWORD"

    subject = email_subject_entry.get()
    body = email_body_entry.get()
    recipient_email = email_recipient_entry.get()

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


def play_music():
    song_path = app_entry.get()
    try:
        os.startfile(song_path)
        speak("Playing music.")
    except Exception as e:
        speak("Sorry, I couldn't play the music.")


def solve_math_problem():
    problem = app_entry.get()
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
                open_application()
            elif "search on google" in query:
                search_google()
            elif "search on youtube" in query:
                search_youtube()
            elif "search on wikipedia" in query:
                search_wikipedia()
            elif "weather update" in query:
                get_weather()
            elif "current time and date" in query:
                get_current_time_and_date()
            elif "send email" in query:
                send_email()
            elif "play music" in query:
                play_music()
            elif "solve" in query:
                solve_math_problem()
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


# GUI setup
root = tk.Tk()
root.title("Desktop Assistant")

app_label = tk.Label(root, text="Enter your command:")
app_label.pack()

app_entry = tk.Entry(root, width=50)
app_entry.pack()

search_button = tk.Button(root, text="Search on Google", command=search_google)
search_button.pack()

youtube_button = tk.Button(root, text="Search on YouTube", command=search_youtube)
youtube_button.pack()

wikipedia_button = tk.Button(root, text="Search on Wikipedia", command=search_wikipedia)
wikipedia_button.pack()

weather_button = tk.Button(root, text="Get Weather Update", command=get_weather)
weather_button.pack()

time_button = tk.Button(root, text="Get Current Time & Date", command=get_current_time_and_date)
time_button.pack()

email_subject_label = tk.Label(root, text="Email Subject:")
email_subject_label.pack()

email_subject_entry = tk.Entry(root, width=50)
email_subject_entry.pack()

email_body_label = tk.Label(root, text="Email Body:")
email_body_label.pack()

email_body_entry = tk.Entry(root, width=50)
email_body_entry.pack()

email_recipient_label = tk.Label(root, text="Recipient Email:")
email_recipient_label.pack()

email_recipient_entry = tk.Entry(root, width=50)
email_recipient_entry.pack()

send_email_button = tk.Button(root, text="Send Email", command=send_email)
send_email_button.pack()

play_music_button = tk.Button(root, text="Play Music", command=play_music)
play_music_button.pack()

solve_button = tk.Button(root, text="Solve Math Problem", command=solve_math_problem)
solve_button.pack()

root.mainloop()

if __name__ == "__main__":
    assistant()
