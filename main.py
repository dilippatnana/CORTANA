import pyttsx3
import datetime
import speech_recognition as sr
import pyaudio
import wikipedia
import webbrowser
import smtplib
import pywhatkit as kit
import pyjokes
import time
import sys
import openai
import requests

OPENAI_API_KEY = ''
APP_PASSWORD = ''
GMAIL_ACCOUNT = 'dilippatnana1231@gmail.com'

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
        r.pause_threshold = 1
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

    speak("I am Assidesk! How may I help you?")



#Function to send a mail
def mailSent(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    # when you start working with the assistant, save this on your device
    server.login(GMAIL_ACCOUNT, APP_PASSWORD)
    # check READme.md for creating an app password
    server.sendmail(GMAIL_ACCOUNT, to, content)

    server.close()

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

        elif 'send email' in query:
            try:
                speak("please tell me the content of the email")
                content = listen()
                speak(content)
                to = input()
                speak(to)
                mailSent(to, content)
                speak(f"successfully sent the email to {to}")
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
