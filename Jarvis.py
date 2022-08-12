import datetime
import os
import googlesearch
import pyttsx3
import speech_recognition as sr
import wikipedia as wiki
from googlesearch import search
import webbrowser
import pickle
import mailer

activate = True



# This is the code for the voice of the assistant.
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 165)


def speak(audio):
    """
    The function takes in a string of text, converts it to speech, and plays it back to you

    :param audio: The audio to be played
    """
    engine.say(audio)
    engine.runAndWait()

def switch():
    """
    If the variable activate is true, then call the function operate. Otherwise, call the function speak
    with the argument "good day to you sir... i am exiting"
    """
    if activate:
        operate()
    else:
        speak("good day to you sir... i am exiting")

def option():
    """
    If the user enters "no" then the global variable activate is set to False, otherwise it is set to
    True.
    """
    option = input("you want to search more..? yes / no\n")
    global activate
    if "no" in option:
        activate = False
    else:
        activate = True
    switch()
    

def take_command(txt=None):
    """
    It takes the audio input from the microphone and converts it into text
    :return: A string
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("i am listening......")
        if(txt != None):
            speak(txt)
        r.pause_threshold = 1
        audio = r.listen(source, phrase_time_limit=4)

    # Trying to recognize the audio input from the microphone and convert it into text. If it fails,
    # it returns "None"
    try:
        text = r.recognize_google(audio, language="en-in")
        print(f"User said : {text}\n")
    except Exception as e:
        # print(e)
        return "None"
    return text


def wish_me():
    """
    If the current time is between 12:00 AM and 12:00 PM, say "Good Morning", if it's between 12:00 PM
    and 4:00 PM, say "Good Afternoon", and if it's between 4:00 PM and 6:00 PM, say "Good Evening"
    """
    time = int(datetime.datetime.now().hour)
    if 12 > time >= 0:
        speak("Good Morning!")
    elif 16 > time >= 12:
        speak("Good Afternoon!")
    elif 18 > time >= 16:
        speak("Good Evening!")
    speak("Hi I am Jarvis your personal assistant!. How may i help you..?")


def take_user_input(txt):
    """
    It takes a string as input and speaks it out loud

    :param txt: The text to be spoken
    :return: The user input
    """
    speak(txt)
    return input()


def send_email():
    """
    It takes the email address of the person you want to send the email to, and then it sends an email
    to that person
    TODO : here you need to create a mycridential pickel by providing your email and app password

    :param to: The email address of the recipient
    :type to: str
    """

    try:
        details = pickle.load(open("mycridentials.pkl", "rb"))
        mail = mailer.Mailer(email=details[0], password=details[1])
        mail.send(receiver=take_user_input("whom you want to send? please type it"), subject=take_command(
            "what is the subject"), message=take_command("what is the message"))
        speak("email has been sent sir")
    except Exception as e:
        print(e)
        speak("something went wrong")

def operate():
    txt = take_command().lower()

    # quiting the loop
    if "exit" in txt or "quit" in txt:
        speak("good day to you sir exiting")

    # if the user didnt say anything it will the function again
    elif txt == "none":
        speak("say it again")
        operate()

    # searchin in wikipedia
    elif "wikipedia" in txt:
        txt = txt.replace("wikipedia", "")
        result = wiki.summary(txt, sentences=2)
        speak(result.split("\n")[0])


    # Searching for the first result of the search query and opening it in the browser.
    elif "play" in txt:
        print("palying in browser")
        for i in search(txt, stop=1):
            print(webbrowser.open(i))

    # Opening the application that is given by the user.
    elif "app" in txt:
        app = txt.split()[1]
        os.system(f"{app}.exe")

    # Opening the website that is given by the user.
    elif ".com" in txt or ".net" in txt or ".org" in txt:
        li = txt.split(" ")
        webbrowser.open(li[-1].strip())

    # Sending an email to the email address that is given by the user.
    elif "mail" in txt:
        li = txt.split()
        speak("sending email sir")
        send_email()

    # it will tell current time
    elif "time" in txt:
        s = datetime.datetime.now().strftime("%H:%M")
        s = s.split(":")
        hour = int(s[0]) - 12 if int(s[0]) > 12 else int(s[0])
        min = int(s[1])
        if int(s[0]) > 12:
            final_str = f"its {hour} : {min} pm"
        else:
                final_str = f"its {hour} : {min} am"
        speak(final_str)

    else:
        # it will search in web
        speak("here what i found in google")
        for i in googlesearch.search(txt, stop=1):
            webbrowser.open(i)
    
    option()

# Calling the functions wish_me() and operate()

wish_me()
operate()

