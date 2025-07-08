from machine import Pin
import time

class ButtonHandler:
    def __init__(self, pin_number=3):
        self.button = Pin(pin_number, Pin.IN, Pin.PULL_UP)

    def read_button(self):
        press_time = 0
        while self.button.value() == 0:
            press_time += 0.1
            time.sleep(0.1)
            if press_time >= 4:
                return "long_4"
            elif press_time >= 2:
                return "long_2"
        if 0 < press_time < 1:
            return "short"
        return None
