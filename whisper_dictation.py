#!.venv/bin/python
# -*- coding: utf-8 -*-
##
## Copyright 2023 Henry Kroll <nospam@thenerdshow.com>
## 
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
## 
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
## MA 02110-1301, USA.
##
import pyautogui
import pyperclip
import os, shlex, time, queue, sys, re
import webbrowser
import tempfile
import threading
import subprocess
api_key = os.getenv("OPENAI_API_KEY")
if (api_key):
    import openai
    openai.api_key = api_key
    
# command launchers for various platforms
commands = {
"windows": {
    "file manager":  "start explorer",
    "terminal":     "start cmd",
    "browser":      "start iexplore",
    "a web browser":  "start iexplore",
    },

"linux": {
    "file manager":  "nemo --no-desktop&",
    "terminal":     "xterm -bg gray20 -fg gray80 -fa 'Liberation Sans Mono' -fs 12 -rightbar&",
    "browser":      "htmlview&",
    "a web browser":  "htmlview&",
    },
}


def check_command(command):
    try:
        subprocess.check_output(["which", command])
        return True
    except subprocess.CalledProcessError:
        return False

# fix race conditions
audio_queue = queue.Queue()
listening = True

# init whisper_jax
from whisper_jax import FlaxWhisperPipline

# https://huggingface.co/models?sort=downloads&search=whisper
# openai/whisper-tiny       39M Parameters
# openai/whisper-tiny.en    39M Parameters
# openai/whisper-base       74M
# openai/whisper-small.en   244M
# openai/whisper-medium.en  769M
# openai/whisper-large      1550M
# openai/whisper-large-v2   1550M
pipeline = FlaxWhisperPipline("openai/whisper-small.en")

def gettext(f):
    outputs = pipeline(f,  task="transcribe", language="English")
    return outputs['text']
    
def pastetext(t):
    # copy text to clipboard
    pyperclip.copy(t)
    # paste text in window
    pyautogui.hotkey('ctrl', 'v')

def preload():
    gettext("click.wav")

print("Start speaking. Text should appear in the window you are working in.")
print("Say \"Stop listening.\" or press CTRL-C to stop.")

def chatGPT(prompt):
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[ {"role": "user", "content": prompt} ]
    )
    completion = completion.choices[0].message.content
    print(completion)
    pastetext(completion)
    if check_command("mimic3"):
        os.system("mimic3 " + shlex.quote(completion))

def transcribe():
    global commands
    while True:
        # transcribe audio from queue
        if f := audio_queue.get():
            t = gettext(f); print('\r' + t)
            # delete temporary audio file
            os.remove(f)
            
            # process spoken commands
            # see list of commands at top of file :)
            tl = t.lower()
            if match := re.search(r"[^\w\s]$", tl):
                tl = tl[:match.start()] # remove punctuation
            # Open terminal.
            if s:=re.search("(peter|computer).? open ", tl):
                q = tl[s.end():] # get program name
                os.system(commands[sys.platform][q])
            # Close window. Okay.
            elif s:=re.search("(peter|computer).? closed? window", tl):
                pyautogui.hotkey('alt', 'F4')
            # Search the web.
            elif s:=re.search("(peter|computer).? search the web for ", tl):
                q = tl[s.end():] # get search query
                webbrowser.open('https://you.com/search?q=' + re.sub(' ','%20',q) + '"')
             # Unknown command, ask Chat-GPT
            elif s:=re.search("(peter|computer).? ", tl):
                chatGPT(tl[s.end():])
            elif re.search("^.new paragraph.?$", tl):
                pyautogui.hotkey('enter')
                pyautogui.hotkey('enter')
            # Stop listening.
            elif re.search("listening", tl) and len(t) < 18:
                break
            else:
                pastetext(t)
        else: time.sleep(1)
        
def recorder():
    # If it wasn't for Gst conflict with pyperclip,
    # we could import record.py instead of os.system()
    # from record import Record
    # rec = Record()
    
    global listening
    while listening:
        # record some (more) audio to queue
        temp_name = tempfile.gettempdir() + '/' \
        + next(tempfile._get_candidate_names()) + ".mp3"
        
        # If it wasn't for Gst conflict with pyperclip
        # we could call recmain in record.py directly
        # rec.to_file(temp_name)
        
        # but instead, we have to call os.system()
        os.system("./record.py " + temp_name)

        # oh well, moving on, let's make sure we got something
        if not os.path.getsize(temp_name):
            if os.path.exists(temp_name):
                os.remove(temp_name)
            break
        else: audio_queue.put(temp_name)

record_thread = threading.Thread(target=recorder)
record_thread.start()

# preload whisper_jax for subsequent speedup
preload_thread = threading.Thread(target=preload)
preload_thread.start()

transcribe()
print("Stopping... Make some noise to return to command prompt.")
listening = False
record_thread.join()
