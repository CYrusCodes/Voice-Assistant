
import speech_recognition as sr

from ShazamAPI import Shazam
import sounddevice as sd
from scipy.io.wavfile import write

import pyttsx3
import webbrowser
import wikipedia
#import subprocess
import pyjokes
import os
import operator
import requests
import ctypes
import datetime
from ecapture import ecapture as ec
#from ShazamAPI import Shazam
# speaker = win32com.client.Dispatch("SAPI.SpVoice")

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
print(voices[1].id)
engine.setProperty('voice', voices[0].id)
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

#it calculates numbers
def get_operator_fn(op):
        return {
        '+' : operator.add,
        '-' : operator.sub,
        'x' or 'X' : operator.mul,
        'divided' :operator.__truediv__,
        'Mod' : operator.mod,
        'mod' : operator.mod,
        '^' : operator.xor,
        }[op]

def eval_binary_expr(*args):
     op1,op2 = int(args[1]), int(args[3])
     oper=args[2]
     return get_operator_fn(oper)(op1, op2)



def record():
    freq = 44100
    # Recording duration
    duration = 10

    # Start recorder with the given values
    # of duration and sample frequency
    recording = sd.rec(int(duration * freq),
                    samplerate=freq, channels=2)
    print("working on it................")
    # Record audio for the given number of seconds
    sd.wait()
    # file with the given sampling frequency
    write("recording0.wav", freq, recording)

def recog():
    mp3_file_content_to_recognize = open(r'C:\Users\Subham Dey\recording0.wav', 'rb').read()
    shazam = Shazam(mp3_file_content_to_recognize)
    recognize_generator = shazam.recognizeSong()
   
    try:
        name=next(recognize_generator)[1]['track']['share']['subject']
       
        print(name) # current offset & shazam response to recognize requests
        speak("it's"+name)
    except:
        speak("could not find")
        print("could not find")



def takeCommand():  #will take command from user recognizing what is being said 
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1) 
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
       # r.adjust_for_ambient_noise(source, duration=5)
        print("working")
  
    try:
        print("Recognizing...")   
        query = r.recognize_google(audio, language ='en-in')
        print(f"User said: {query}\n")
  
    except Exception as e:
        print(e)   
        print("Unable to Recognize your voice.") 
        return "None"
     
    return query

if __name__=="__main__":
    #clear = lambda: os.system('cls')
    speak("hi, how may I help you")
    query = takeCommand().lower()

    if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences = 3)
            speak("According to Wikipedia")
            print(results)
            speak(results)
    elif 'open google' in query:
            speak("Here you go to Google\n")
            first_url = 'https://www.google.com/'
            webbrowser.open_new_tab(first_url)
    elif "open youtube" in query:
            speak("Here you go to youtube\n")
            first_url = 'https://www.youtube.com/'
            webbrowser.open_new_tab(first_url)
    elif "in youtube" in query:
            speak("song name please")
            query1 = takeCommand().lower()
            name=query1.split()
            str=''
            for i in range(len(name)):
                    if(i==len(name)-1):
                        str=str+name[i]
                    else:
                        str=str+name[i]+'+'
            first_url = 'https://www.youtube.com/results?search_query='+str
            webbrowser.open_new_tab(first_url)        
    elif 'joke' in query:
            joke=pyjokes.get_joke()
            print(joke)
            speak(joke)

    
    elif "calculate" in query:
        #  query.replace("calculate", "",10)
          answer=eval_binary_expr(*(query.split()))
          print(answer)
          speak(answer)

    elif "camera" in query or "take a photo" in query or "capture a photo" in query:
            speak("smile please")
            ec.capture(0, "Jarvis Camera ", "img.jpg")
    
    elif "where is" in query:
            query = query.replace("where is", "")
            location = query
            speak("User asked to Locate")
            speak(location)
            webbrowser.open("https://www.google.com/search?q=" + location)

    elif "write a note" in query:
            speak("What should i write, sir")
            note = takeCommand()
            file = open('jarvis.txt', 'w')
            try:
                speak("Sir, Should i include date and time")
                snfm = takeCommand()
                if 'yes' in snfm or 'sure' in snfm:
                    strTime = datetime.datetime.now().strftime("% H:% M:% S")
                    file.write(strTime)
                    file.write(" :- ")
                    file.write(note)
                else:
                    file.write(note)
            except:
                  file.write(note)

   

    elif "lock" in query:
                speak("locking the device")
                ctypes.windll.user32.LockWorkStation()
    elif "what is this song" or "recognise this song" in query:
         #song recogniser
         speak("play the song....")
         record()
         recog()
    else:
          speak("did not get")
          print("did not get")
