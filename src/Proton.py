import pyttsx3
import speech_recognition as sr
from datetime import date
import time
import webbrowser
import datetime
from pynput.keyboard import Key, Controller
import pyautogui
import sys
import os
import smtplib
import wikipedia
import  Gesture_Controller
import app
from threading import Thread
import webbrowser
import subprocess



today = date.today()
r = sr.Recognizer()
keyboard = Controller()
engine = pyttsx3.init('sapi5')
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


is_awake = True 

def reply(audio):
    app.ChatBot.addAppMsg(audio)
    print(audio)
    engine.say(audio)
    engine.runAndWait()

def wish():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        reply("Good Morning!")
    elif hour>=12 and hour<18:
        reply("Good Afternoon!")   
    else:
        reply("Good Evening!")  
        
    reply("I am Proton, how may I help you?")

with sr.Microphone() as source:
        r.energy_threshold = 500 
        r.dynamic_energy_threshold = False

def record_audio():
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        voice_data = ''
        audio = r.listen(source,phrase_time_limit=5)

        try:
            voice_data = r.recognize_google(audio)
        except sr.RequestError:
            reply('Sorry my Service is down. Plz check your Internet connection')
        except sr.UnknownValueError:
            print('cant recognize')
            pass
        return voice_data.lower()

def respond(voice_data):
    global file_exp_status, files, is_awake, path
    print(voice_data)
    voice_data.replace('proton','')
    app.eel.addUserMsg(voice_data)

    if is_awake==False:
        if 'wake up' in voice_data:
            is_awake = True
            wish()

    elif 'hello' in voice_data:
        wish()

    elif 'left click' in voice_data:
        pyautogui.click()

    elif 'right click' in voice_data:
        pyautogui.click(button = 'right')

    elif 'double click' in voice_data:
            pyautogui.doubleClick()

    elif 'what is your name' in voice_data:
        reply('My name is Proton!')

    elif 'date' in voice_data:
        reply(today.strftime("%B %d, %Y"))

    elif 'time' in voice_data:
        reply(str(datetime.datetime.now()).split(" ")[1].split('.')[0])

    elif 'search' in voice_data:
        reply('Searching for ' + voice_data.split('search')[1])
        url = 'https://google.com/search?q=' + voice_data.split('search')[1]
        try:
            webbrowser.get().open(url)
            reply('This is what I found Sir')
        except:
            reply('Please check your Internet')

    elif 'location' in voice_data:
        reply('Which place are you looking for ?')
        temp_audio = record_audio()
        app.eel.addUserMsg(temp_audio)
        reply('Locating...')
        url = 'https://google.nl/maps/place/' + temp_audio + '/&amp;'
        try:
            webbrowser.get().open(url)
            reply('This is what I found Sir')
        except:
            reply('Please check your Internet')

    elif ('bye' in voice_data) or ('by' in voice_data):
        reply("Good bye Sir! Have a nice day.")
        is_awake = False

    elif ('exit' in voice_data) or ('terminate' in voice_data):
        if Gesture_Controller.GestureController.gc_mode:
            Gesture_Controller.GestureController.gc_mode = 0
        app.ChatBot.close()
        sys.exit()
    
    elif "open youtube" in voice_data:
        reply("Here you go to Youtube\n")
        url = "https:\\www.youtube.com"
        webbrowser.get().open(url)

    elif "who am I" in voice_data:
        reply("If you talk then definitely your human.")
   
    elif 'launch gesture recognition' in voice_data:
        if Gesture_Controller.GestureController.a:
            reply('Gesture recognition is already active')
        else:
            gc = Gesture_Controller.GestureController()
            t = Thread(target = gc.start)
            t.start()
            reply('Launched Successfully')

    elif 'stop gesture recognition' or 'top gesture recognition' or'stock gesture reognition' in voice_data:
        if Gesture_Controller.GestureController.a:
            Gesture_Controller.GestureController.a = 0
            reply('Gesture recognition Stopped')
        else:
            reply('Gesture recognition is already inactive')
        
    elif 'copy' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('c')
            keyboard.release('c')
        reply('Copied')
          
    elif 'page' in voice_data or 'pest'  in voice_data or 'paste' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('v')
            keyboard.release('v')
        reply('Pasted')                                    
       

    elif 'open word' or 'open world' in voice_data:
        c = "D:\\Shivakumar L S Offer letter.pdf"
        os.startfile(c)

    elif "open notepad" in voice_data:
        subprocess.Popen('notepad')

                   
    else: 
        reply('I am not functioned to do this !')



t1 = Thread(target = app.ChatBot.start)
t1.start()


while not app.ChatBot.started:
    time.sleep(0.5)

wish()
voice_data = None
while True:
    if app.ChatBot.isUserInput():

        voice_data = app.ChatBot.popUserInput()
    else:
     
        voice_data = record_audio()

   
    if 'proton' in voice_data:
        try:
            respond(voice_data)
        except SystemExit:
            reply("Exit Successfull")
            break
        except:
            print("EXCEPTION raised while closing.") 
            break