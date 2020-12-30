from pynput.keyboard import Key, Controller
import time
import os
from textwrap import wrap
import sys
from pathlib import Path
import pyperclip

keyboard = Controller()

KEY_TIME = 0.0001
def type_char(input_char):
    time.sleep(KEY_TIME)
    keyboard.press(input_char)
    time.sleep(KEY_TIME)
    keyboard.release(input_char)

def ctrl_v():
    time.sleep(KEY_TIME)
    keyboard.press(Key.ctrl)
    time.sleep(KEY_TIME)
    keyboard.press('v')
    time.sleep(KEY_TIME)
    keyboard.release(Key.ctrl)
    keyboard.release('v')

def type_string(input_string):
    type_char(Key.enter)
    time.sleep(KEY_TIME)
    pyperclip.copy(input_string)
    ctrl_v()
    time.sleep(KEY_TIME)
    # for char in input_string:
    #     type_char(char)
    type_char(Key.enter)

def read_file(input_filename):
    return_string = Path(input_filename).read_text()
    return_string = return_string.replace('\n', ' ').replace('\r', '')
    return return_string

def split_strings(input_string):
    print(type(input_string))
    n = 200
    out = [(input_string[i:i+n]) for i in range(0, len(input_string), n)] 
    return out

SLEEP_BETWEEN_TEXT_TIME = 4

def type_file(split_strings):
    for string in split_strings:
        type_string(string)
        time.sleep(SLEEP_BETWEEN_TEXT_TIME)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Incorrect number of arguments, please pass a filename")
        quit()
    time.sleep(5)
    print(f'Reading file: {sys.argv[1]}')
    file_contents = read_file(sys.argv[1])
    strings = split_strings(file_contents)
    type_file(strings)