# Nexss Programmer package: Speak
# uses great package pyttsx3 (MPL-2.0 License).

import platform
import json
import sys
import io
import os

import pyttsx3

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # 0,1,2,3

sys.path.append(os.path.join(os.getenv("NEXSS_PACKAGES_PATH"), "Nexss", "Lib"))

from NexssLog import nxsInfo, nxsOk, nxsWarn, nxsError
from NexssInstall import nxsEnsure

nxsEnsure('pyttsx3')

# STDIN
NexssStdin = sys.stdin.read()

parsedJson = json.loads(NexssStdin)


if "_voices" in parsedJson.keys():
    engine = pyttsx3.init() # object creation
    voices = engine.getProperty('voices') 
    print(voices)
    sys.exit(0)

if "_speak" not in parsedJson.keys():
    if "nxsIn" in parsedJson.keys():
        parsedJson['_speak'] = " ".join(parsedJson['nxsIn'])
        del parsedJson['nxsIn']
    else:
        nxsError('No text to speak. Pass text as parameters or as argument --_speak')
        sys.exit(1)

engine = pyttsx3.init() # object creation

_rate = 115
if "_rate" in parsedJson.keys():
    _rate = parsedJson["_rate"]
engine.setProperty('rate', _rate) 

_pitch = 115
if "_pitch" in parsedJson.keys():
    _pitch = parsedJson["_pitch"]
engine.setProperty('pitch', _pitch) 

_type = 0
if "_type" in parsedJson.keys():
    _type = parsedJson["_type"]

voices = engine.getProperty('voices') 
engine.setProperty('voice', voices[_type].id)

_volume = 1.0
if "_volume" in parsedJson.keys():
    _volume = parsedJson["_volume"]

engine.setProperty('volume', _volume) 

engine.say(parsedJson['_speak'] )
engine.runAndWait()
engine.stop()

NexssStdout = json.dumps(parsedJson, ensure_ascii=False).encode(
    'utf8', 'surrogateescape')
# STDOUT
print(NexssStdout.decode('utf8', 'surrogateescape'))
