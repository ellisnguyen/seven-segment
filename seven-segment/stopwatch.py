from threading import Timer, Thread
import math
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame import mixer
import time
from .display import *
from .constants import *

class Stopwatch(Thread):
    #Initialize all variables
    def __init__(self):
        super().__init__()
        self.led_blink = False
        self.blink_on = True
        self.led_on = True
        self.time = ""
        self.time_in_seconds = 0.0
        self.got_interrupted = False
        self.timer_is_off = False
        self.stopwatch_on = False
        self.reset_pause = False

    #Runs the stopwatch
    def run(self):
        self.update_time()
        self.blink_led()
        inputs[BUTTON_IN].when_released = self.monitor_button #Keeps LED off until the button is pressed
        while not self.got_interrupted:
            clock_displays(self.timenorm(self.time_in_seconds), True)
        clear_displays()
    
    #Increases time with 100 ms precision
    def update_time(self):
        if not self.got_interrupted and self.stopwatch_on and not self.reset_pause:
            self.time_in_seconds += .1
        Timer(0.1, self.update_time).start()

    #Rounds time to nearest .1 seconds, and ensures the time is in the correct format on the display (000.0)  
    def timenorm(self, seconds):
        t = str(round(seconds, 1)).strip().replace(".", "")
        
        if len(t)<4:
            for i in range(4-len(t)):
                t = "0" + t
        print(t)
        return t

    #Blinks the LED every half second while the stopwatch is counting up
    def blink_led(self):
        if not self.got_interrupted and not self.timer_is_off and self.stopwatch_on:
            set_led(self.led_on)
            self.led_on = not self.led_on
        Timer(0.5, self.blink_led).start()

    '''
    If button is pressed, stopwatch starts counting and LED starts blinking.
    When pressed again, stopwatch stops counting and LED stays on.
    When pressed again, resets display to 000.0, and turns off the LED.
    '''
    def monitor_button(self):
        self.reset_pause = False
        print("released")
        self.stopwatch_on = not self.stopwatch_on
        if not self.stopwatch_on:
            set_led(True)
        if self.stopwatch_on and (self.time_in_seconds > 0.0):
            self.stopwatch_on = False
            self.reset_pause = True
            self.time_in_seconds = 0.0
            set_led(False)

    #Called if Ctrl+C is pressed
    def stop(self):
        self.got_interrupted = True
        clear_displays()

