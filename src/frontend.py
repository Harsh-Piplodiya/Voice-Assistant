import customtkinter as ctk
import speech_recognition as sr
from Newbot_2 import pridict_class, get_response, talk
import json
import threading
from customtkinter import *
intents = json.loads(open('path of the JSON file/intents.json').read())
root = ctk.CTk(fg_color="#2B2B2B")
root.geometry("400x580+950+110")
root.title("Voice Assistant")
root.iconbitmap('Path of boticon.ico')


u = 0
b = 1

listener = sr.Recognizer()


def listen():
    try:
        with sr.Microphone() as source:
            print("Listening....")
            listener.adjust_for_ambient_noise(source, 0.2)
            voice = listener.listen(source)
            cmd = listener.recognize_google(voice)
            cmd = cmd.lower()
            return cmd
    except Exception:
        pass


def botcall():
    btn.configure(state=DISABLED)


    global b
    global u
    message = str(listen())
    user_label = CTkLabel(user_message, text=message, justify='right',
                          wraplength=100, bg_color="#74bcf4", corner_radius=10)
    user_label.grid(row=u, sticky=NE, padx=10, pady=10)
    u += 1
    ints = pridict_class(message)
    res = get_response(ints, intents, message)
    b += 1
    bot_label = CTkLabel(bot_message, text=res, justify='left',
                         wraplength=200, bg_color="#b49577", corner_radius=10)
    bot_label.grid(row=b, sticky=NW, padx=10, pady=10)
    talk(res)
    print(res)
    btn.configure(state=NORMAL)


def start_bot():
    bot_thread = threading.Thread(target=botcall)
    bot_thread.start()


def light_dark(value):
    if value == "Light":
        ctk.set_appearance_mode("light")
        root.configure(fg_color='white')
    elif value == "Dark":
        ctk.set_appearance_mode("dark")
        root.configure(fg_color='#2B2B2B')


# Create a frame to hold the label and button
f1 = CTkFrame(root)
f1.pack()

segemented_button = ctk.CTkSegmentedButton(master=f1,
                                           values=["Light", "Dark"],
                                           command=light_dark)
segemented_button.pack(padx=20, pady=10, side=TOP)
segemented_button.set("Light")


# Create a frame to hold the messages
msg_frame = CTkFrame(f1)
msg_frame.pack()

# Create a Listbox widget and attach a Scrollbar to it
msg_listbox = CTkScrollableFrame(
    msg_frame, bg_color="#f2f2f2", width=400, height=400)
msg_listbox.pack()

user_message = CTkFrame(msg_listbox, width=200)
user_message.pack(side=RIGHT, anchor=NE, fill=BOTH)
bot_message = CTkFrame(msg_listbox, width=200)
bot_message.pack(side=LEFT, anchor=NW, fill=BOTH)
text = CTkEntry(f1,corner_radius=10,width=250)
text.pack(side=LEFT,pady=30)
def botcallchat():  # This funtion is to call the bot for input
 
    message = text.get()

    global b
    global u

    user_label = CTkLabel(user_message, text=message, justify='right',
                          wraplength=100, bg_color="#74bcf4", corner_radius=8)
    user_label.grid(row=u, sticky=NE, padx=10, pady=10)
    u += 1
    ints = pridict_class(message)
    res = get_response(ints, intents, message)
    b += 1
 
    bot_label = CTkLabel(bot_message, text=res, justify='left',
                         wraplength=200, bg_color="#b49577", corner_radius=8)
    bot_label.grid(row=b, sticky=NW, padx=10, pady=10)
    talk(res)
    print(res)

    
    
from PIL import ImageTk,Image
butsub=CTkButton(f1, text='Send', command=botcallchat)
butsub.pack(side=RIGHT)
btn = CTkButton(root,text=None,image=ImageTk.PhotoImage(Image.open('path of bmic.png').resize((30,30))), command=start_bot,width=10,height=10)
btn.pack(side=BOTTOM)

#-----------------------------------------------------------------------------------------------------------------------------------------------------

import random
def wakeword():
    while True:
        try:
            with sr.Microphone() as source:
                print("Detecting")
                listener.adjust_for_ambient_noise(source, 0.1)
                voice = listener.listen(source)
                cmd = listener.recognize_google(voice,with_confidence=False,show_all=False)
                cmd = cmd.lower()
                if 'robin' in cmd:
                    talk("yes")
                    botcall()
        except Exception:
            pass
        if event.is_set():
            break
wake=threading.Thread(target=wakeword)
wake.start()
event=threading.Event()
root.mainloop()
event.set()