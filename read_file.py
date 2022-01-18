import keyboard
import pyperclip
import time
import os
from textwrap import wrap
import sys
from pathlib import Path

KEY_DELAY = .0001
def type_string(input_string):
    '''
    Checks which keys are currently pressed,
    Releases pressed keys,
    Copies a string to the clipboard,
    Presses enter,
    Copy pastes the next string,
    Presses enter,
    Presses original pressed keys
    '''
    pyperclip.copy(input_string)
    scan_codes = keyboard.stash_state()
    time.sleep(KEY_DELAY)
    keyboard.send('enter', do_press=True, do_release=True)
    time.sleep(KEY_DELAY)
    keyboard.send('ctrl+v', do_press=True, do_release=True)
    time.sleep(KEY_DELAY)
    keyboard.send('enter', do_press=True, do_release=True)
    time.sleep(KEY_DELAY)
    keyboard.restore_state(scan_codes)


def read_file(input_filename):
    '''
    Reads the file to a string, replacing newline characters with spaces
    '''
    return_string = Path(input_filename).read_text(encoding='utf-8')
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
