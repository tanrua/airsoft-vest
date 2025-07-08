from machine import Pin
from neopixel import NeoPixel

class LEDController:
    def __init__(self, pin_number=2, num_leds=5):
        self.pin = Pin(pin_number, Pin.OUT)
        self.np = NeoPixel(self.pin, num_leds)
        self.num_leds = num_leds
        self.color_map = {
            "red": (255, 0, 0),
            "yellow": (255, 255, 0),
            "lime": (50, 205, 50),
            "green": (0, 200, 0),
            "blue": (0, 0, 255),
            "orange": (255, 165, 0),
            "pink": (255, 192, 203),
            "white": (255, 255, 255),
            "off": (0, 0, 0),
        }

    def set_leds(self, colors):
        for i in range(self.num_leds):
            color = self.color_map.get(colors[i], (0, 0, 0))
            self.np[i] = color
        self.np.write()
