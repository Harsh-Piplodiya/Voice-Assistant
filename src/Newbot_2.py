import webbrowser as wb
import socket
import random
import json
import pickle
import numpy as np
import pyttsx3
import nltk
from nltk.stem import WordNetLemmatizer
# import pywintypes
from keras.models import load_model
import datetime
import google
import speech_recognition as sr
import pywhatkit
import calendar
import os
import psutil
import pyjokes
#import frontend as ft


# here we are putting python text-to-speech convertor in 'engine' variable
engine = pyttsx3.init()
# here we get the voices present in the pyttsx3 and put them in 'voices
voices = engine.getProperty('voices')
# here we set the '1' index value voice in the engine as our default voice
engine.setProperty('voice', voices[1].id)


def talk(text):
    # this command is used to talk or repeat the words said by the user
    engine.say(text)

    engine.runAndWait()  # this command will run the speaker/engine and then wait for next input


listener = sr.Recognizer()

lemmit = WordNetLemmatizer()
intents = json.loads(open('G:/Bachelor Project/BCA Voice Asssistant Project/intents.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))

model = load_model('chatbotmodel.h5')


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmit.lemmatize(word) for word in sentence_words]
    return sentence_words


def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)


def pridict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    result = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    result.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in result:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

#---------------------------------To get responses of the query-----------------------------------------------

def get_response(intents_list, intents_json, message):
    if message == None or message == 'None':
        talk("please repeat")
        listen()
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            if i['tag'] == "goodbye":
                result = random.choice(i['responses'])
                print(result)
                talk(result)
                exitBot()
            if i['tag'] == "datetime":
                result = random.choice(i['responses'])
                gettime(result)
            if i['tag']  == "date":
                result = random.choice(i['responses'])
                date(result)    
            if i['tag'] == "summary":
                result = random.choice(i['responses'])
                if "what is a" in message:
                    message = message.replace('what is a', '')
                    g_search(message)
                if "what is" in message:
                    message = message.replace('what is', '')
                    g_search(message)
                if "who is" in message:
                    message = message.replace('who is', '')
                    g_search(message)
                if "what are" in message:
                    message = message.replace('what are', '')
                    g_search(message)
                if "who are" in message:
                    message = message.replace('who are', '')
                    g_search(message)
            if i['tag'] == "note":
                create_note()
            if i['tag'] == "thanks":
                result = random.choice(i['responses'])
                engine.say(str(result))
                engine.runAndWait()
                exitBot()
            if i['tag'] == "google":
                result = random.choice(i['responses'])
                web_search(str(message))
            if i['tag'] == "addtodo":
                todos()
            if i['tag'] == "showtodo":
                show_todo()
            if i['tag'] == "youtube":
                youtube(message)  
            if i['tag'] == "open google":
                google_tab()
            if i['tag'] == "open youtube":
                open_yt()
            if i['tag'] == "open stckovr":
                open_stcovr()
            if i['tag'] == "open gmail":
                open_gmail()
            if i['tag'] == "cpu":
                cpu()     
            if i['tag'] == "glocation":
                glocation()                     
            result = random.choice(i['responses'])
            return result
            break



def create_note():
    print("what do you want to write in the note?")
    engine.say("what do you want to write in the note?")
    engine.runAndWait()
    note = str(listen())
    i = 0
    with open(f"note{i}.txt", 'w') as file:
        file.write(note)
        i += 1
    print(f"succeccfully created the note as note{i-1}.txt")
    engine.say(f"succeccfully created the note as note{i-1} dot txt")
    engine.runAndWait()
    botcall()



def youtube(message):
    msg = message
    if ("play" in msg or "song" in msg or "youtube" in msg or "on youtube" in msg or "search" in msg):
        song_name = msg.replace('play', '')
        song_name = msg.replace('youtube', '')
        song_name = msg.replace('song', '')
        song_name = msg.replace('on youtube', '')
        song_name = msg.replace('search', '')
        #if "play" in message:
            #song_name = message.replace('play', '')
        #if "youtube" in message:
            #song_name = message.replace('youtube', '')
    try:       
        pywhatkit.playonyt(song_name)  
    except Exception:
        engine.say("Please Repeat!") 
    return         



def web_search(message):
    if "google" in message:
        mm = message.replace('google', '')
    if "search" in message:
        mm = message.replace('search', '')
    try:
        wb.open(url=mm)
    except Exception:
        engine.say("Sorry could not understand you, Please repeat!")
    return



def g_search(res):
    import wikipedia
    try:
        info = wikipedia.summary(str(res), auto_suggest=False, sentences=3)
        print(info)
        engine.say(info)
        return info
    except wikipedia.DisambiguationError:
        engine.say(
            str(res)+" can have multiple meaning on what basis you are talking about?")
        engine.runAndWait()
        return
    except KeyError:
        engine.say("Please repeat")
        engine.runAndWait()
        return
    except Exception:
        engine.say("Please repeat")
        engine.runAndWait()
        return


 
def cpu():
    usage = str(psutil.cpu_percent())
    engine.say('CPU usage is at ' + usage)
    engine.runAndWait()
    print('CPU usage is at ' + usage)
    battery = psutil.sensors_battery()
    engine.say("Battery is at")
    engine.runAndWait()
    engine.say(battery.percent)
    engine.runAndWait()
    print("battery is at:" + str(battery.percent))    



month_num = 0
def gettime(result):
    tm = datetime.datetime.now().strftime("%H:%M:%S")
    engine.say(str(tm))
    # engine.say(str(result+tm))
    engine.runAndWait()
    return str(tm)

def convert_to_month_name(month_num):
    month_n = calendar.month_name[month_num]
    return month_n    

def date(result):
    year = int(datetime.datetime.now().year)
    month_num = int(datetime.datetime.now().month)
    date = int(datetime.datetime.now().day)
    month_name = convert_to_month_name(month_num)

    engine.say("The Current Date is: "+ str(date) + str(month_name) + str(year))



todo_list = []
with open('todolist.txt', 'r') as tf:
    for line in tf.readlines():
        if '\n' in line:
            item = line.replace('\n', '')
            todo_list.append(item)
        else:
            todo_list.append(line)



def todos():  # this funtion is used to create the file name todo list
    print("what do you want to add?")
    engine.say("what do you want to add in to do list?")
    engine.runAndWait()
    #ft.ChatApplication.send_message.text_response.insert('what do you want to add in to do list?')

    item = str(listen())
    todo_list.append(item)
    with open('todolist.txt', 'a') as tf:
        tf.write(f'\n{item}')

    print(f"Done ,I added {item} in your to do list")
    engine.say(f"Done ,I added {item} in your to do list")
    engine.runAndWait()



def show_todo():  # this funtion is used to show the file name todo list
    print("Items in your todo list are")
    engine.say("Items in your to do list are")
    for item in todo_list:
        engine.say(item)
    engine.runAndWait()
    botcall()



def google_tab():
        wb.open_new_tab("https://www.google.com")
        engine.say("google is open now")
        engine.runAndWait()

def open_yt():
        wb.open_new_tab("https://www.youtube.com")
        engine.say("youtube is open now")   
        engine.runAndWait()       

def open_stcovr():
        wb.open_new_tab("https://stackoverflow.com/")
        engine.say("Here is stackoverflow") 
        engine.runAndWait()

def open_gmail():
        wb.open_new_tab("gmail.com")
        engine.say("Google Mail open now")
        engine.runAndWait()



def glocation():
    engine.say("What is the Location?")
    engine.runAndWait()
    location = str(listen())
    url = "https://google.nl/maps/place/" + location + "/&amp;"
    wb.get().open(url)
    engine.say("Here is the location of " + location)



def exitBot():
    # main()
    exit()
    # return main()



def listen():  # This funtion listens to user and converts speech into text with speechrecogniton module
    try:
        with sr.Microphone() as source:  # here using sr.Microphone we declare it as a source of audio
            print("Listening....")
            # now the listener listen's to the source
            listener.adjust_for_ambient_noise(source, 0.5)
            voice = listener.listen(source)
            # this recognize_google command converts voice to text using google
            cmd = listener.recognize_google(voice)
            cmd = cmd.lower()

            return cmd
    except Exception:
        engine.say(random.choice(["Sorry, can't understand you", "i apologize as i could not understand you",
                                  "Please give me more information", "you were saying...",
                                  "Not sure I understand", "can you repeat yourself, please", "sorry, i did not get you"]))


def botcall():  # This funtion is to call the bot for input
    while True:
  
        message = str(listen())
        ints = pridict_class(message)
        res = get_response(ints, intents, message)
        talk(res)
        print(res)
        botcall()
    # main()


def botcallchat(msg):  # This funtion is to call the bot for input
    # message=input("")
    # message=taking_command()

    message = msg
    ints = pridict_class(message)
    res = get_response(ints, intents, message)
    talk(res)
    return (res)

def start():
    engine.say('BOT Initiated')
    engine.runAndWait()
    # main()

#botcall()
