import pyttsx3
import datetime
import speech_recognition as sr
import pyaudio
import wikipedia
import webbrowser
import pywhatkit as kit
import pyjokes
import time
import sys
import openai
import requests
import smtplib, ssl
import getpass
from email.message import EmailMessage

OPENAI_API_KEY = 'Your app password'
APP_PASSWORD = 'Your app password'
GMAIL_ACCOUNT = 'dilippatnana1231@gmail.com'
SMTP_SERVER = "smtp.gmail.com"
PORT = 587  # For starttls

# OpenAI ChatGPT API credentials
openai.api_key = OPENAI_API_KEY

print("Your Assistant is starting......")

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 190)


def listen():
    # takes microphone command and converts to string

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I am listening....")
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 0.8
        audio = r.listen(source)

    try:
        print("Recognising.....")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print("I am sorry I don't understand, Say that again please...")
        return "None"
    return query

#Funtion to make text to speech
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    print(audio)

#Function to great the user
def wish_user():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")

    elif hour >= 12 and hour < 16:
        speak("Good Afternoon")

    else:
        speak("Good Evening")

    speak("I am Cortana! How may I help you?")


#Function to send a mail
def mailSent():
    speak("please enter your email")
    sender_email = input("Enter your email: ")
    # speak("please enter your password")
    # password = getpass.getpass(prompt="Enter your password: ")
    password = APP_PASSWORD
    speak("please enter receiver's email")
    receiver_email = input("Enter the email: ")

    speak("what do you want to send? Please enter the body of the mail.")
    message = input("BODY OF THE MAIL:\n")


    em = EmailMessage()
    em['From'] = sender_email
    em['To'] = receiver_email
    em.set_content(message)
    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER,PORT,context=context)
        server.login(sender_email, password)
        # Send the mail
        server.sendmail(sender_email, receiver_email, message)

    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()

def chat_with_gpt(prompt):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=100,
        temperature=0.7,
        n=1,
        stop=None,
        echo=True
    )

    return response.choices[0].text.strip()


if __name__ == '__main__':

    wish_user()
    while True:
        query = listen().lower()

        if 'wiki' in query:
            speak('Give me sometime I am looking into Wikipedia')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=5)
            speak("This is what I found!")
            speak(results)
            print(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'search google' in query:
            webbrowser.open("google.com")

        elif 'play music' in query:
            webbrowser.open("spotify.com")
        
        elif "talk" in query:
                speak("what do you want to talk with me?")
                chat_prompt = listen()
                if "thank you" in chat_prompt:
                    speak("OK sure")
                    break
                else:
                    gpt_response = chat_with_gpt(chat_prompt)
                    print(gpt_response)
                    speak(gpt_response)

        elif 'time' in query:
            time = datetime.datetime.now().strftime("%H:%M")
            speak(f"Its {time} now")

        elif 'date today' in query:
            date = datetime.datetime.today()
            speak(f"Today is {date}")

        elif 'send a mail' in query:
            try:
                mailSent()
                speak(f"successfully sent the email")
            except Exception as e:
                print(e)
                speak("sorry! i was unable to send the mail")

        elif 'whatsapp message' in query:  # you should be logged in into whatsapp web for this
            speak("To whom should I send the message?")
            number = int(input(""))
            speak("Tell me the message please")
            message = listen()
            speak("At what time should i send it? (24 hours system)")
            hr = int(input("Hours: "))
            mins = int(input("Minutes: "))
            # this should be in the format ("+91xxxxxxxxxx","This is message", 15, 20)
            kit.sendwhatmsg(number, message, hr, mins)

        elif 'open facebook' in query:
            webbrowser.open("facebook.com")

        elif 'open google classroom' in query:
            webbrowser.open("https://classroom.google.com/u/1/h")

        elif 'joke' in query:
            joke = pyjokes.get_joke()
            speak(joke)

        elif 'no thanks' in query: 
            speak("thanks for using me! Have a good day")
            sys.exit()
        
        else:
            speak("Sorry, I didn't understand.")

        time.sleep(5)
        speak("do you have any other work?")
