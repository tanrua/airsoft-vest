import neopixel, machine
import time
from picozero import pico_led, Button

for _ in range(5):
    pico_led.on()
    time.sleep(0.25)
    pico_led.off()
    time.sleep(0.25)

np = neopixel.NeoPixel(machine.Pin(0), 5)
color = (255, 0, 0)  

print("doing something")

np[0] = (255, 0, 0)
np[1] = (255, 0, 0)
np[3] = (255, 0, 0)
np[4] = (255, 0, 0)
np.write()

time.sleep(10)
