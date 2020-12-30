from pynput.keyboard import Key, Controller
import keyboard
import pyperclip
import time
import os
from textwrap import wrap
import sys
from pathlib import Path

pynput_keyboard = Controller()

KEY_TIME = 0.0001

def type_char(input_char):
    '''
    Types a character to a screen using delay
    before pressing key and before releasing key
    '''
    time.sleep(KEY_TIME)
    pynput_keyboard.press(input_char)
    time.sleep(KEY_TIME)
    pynput_keyboard.release(input_char)

def ctrl_v():
    '''
    Presses ctrl+v with three delays to help with 
    key order
    '''
    time.sleep(KEY_TIME)
    pynput_keyboard.press(Key.ctrl)
    time.sleep(KEY_TIME)
    pynput_keyboard.press('v')
    time.sleep(KEY_TIME)
    pynput_keyboard.release(Key.ctrl)
    pynput_keyboard.release('v')

def type_string(input_string):
    '''
    Checks which keys are currently pressed,
    Releases pressed keys,
    Copies a string to the clipboard,
    Presses enter,
    Pastes the string from the keyboard,
    Presses enter,
    Presses original pressed keys
    '''
    # List of keys to check since I can't find a way to 
    # check all of the keys
    check_keys = 'asdwer '
    keys = []
    for key in check_keys:
        if keyboard.is_pressed(key):
            keys.append(key)
    print(keys)
    for key in keys:
        time.sleep(KEY_TIME)
        pynput_keyboard.release(key)
    pyperclip.copy(input_string)
    type_char(Key.enter)
    ctrl_v()
    type_char(Key.enter)
    # for key in keys:
    #     time.sleep(KEY_TIME)
    #     pynput_keyboard.press(key)


def read_file(input_filename):
    '''
    Reads the file to a string, replacing newline characters with spaces
    '''
    return_string = Path(input_filename).read_text()
    return_string = return_string.replace('\n', ' ').replace('\r', '')
    return return_string

def split_strings(input_string, n=195):
    ''' 
    Using whitespace as delimiter, splits string into strings with a maximum
    character limit n based on full words
    '''
    words = input_string.split()
    out = []
    string = words[0]
    for i in range(1, len(words)):

        # If the string is not full, tack it on
        if ((len(string) + len(words[i]) + 1 ) < n):
            string = string + ' ' + words[i]
        
        # Otherwise, save the string and start a new string
        else:
            out.append(string)
            string = words[i]

    # Save the last string to out
    out.append(string)
    return out

SLEEP_BETWEEN_TEXT_TIME = 6

def type_file(split_strings):
    '''
    Using a list of strings to print, prints the list and sleeps between prints
    '''
    for string in split_strings:
        type_string(string)
        time.sleep(SLEEP_BETWEEN_TEXT_TIME)


if __name__ == "__main__":
    '''
    Sleeps for 5 seconds to allow for alt+tab
    Starts printing file contents to screen
    Although many blocks can be pasted before a delay is needed,
    delaying between every block including the first allows people to read it
    '''
    if len(sys.argv) != 2:
        print("Incorrect number of arguments, please pass a filename")
        quit()
    time.sleep(5)
    print(f'Reading file: {sys.argv[1]}')
    file_contents = read_file(sys.argv[1])
    strings = split_strings(file_contents)
    type_file(strings)