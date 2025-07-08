from machine import I2C, Pin
import time
import math
import ustruct
from collections import deque

# Constants for activity thresholds
LOW_ACTIVITY_THRESHOLD = 0.02
MEDIUM_ACTIVITY_THRESHOLD = 0.1
WINDOW_SIZE = 50  # Number of samples in the moving window
SAMPLE_DELAY = 0.05  # 50 ms between samples = 20 Hz

# Constants for accelerometer readings
ADXL345_ADDRESS = 0x53 # address for accelerometer 
ADXL345_POWER_CTL = 0x2D # address for power control
ADXL345_DATA_FORMAT = 0x31 # address for configure data format
ADXL345_DATAX0 = 0x32 # where the x-axis data starts
ADXL345_RESOLUTION = 0.0039
 
# Initialize I2C (CHANGE NEEDED)
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

# Initialize ADXL345
def init_adxl345():
    i2c.writeto_mem(ADXL345_ADDRESS, ADXL345_POWER_CTL, bytearray([0x08]))  # Set bit 3 to 1 to enable measurement mode
    i2c.writeto_mem(ADXL345_ADDRESS, ADXL345_DATA_FORMAT, bytearray([0x0B]))  # Set data format +/- 8g by trying 0x0C

# Replace with your accelerometer's read function
def read_accel():
    data = i2c.readfrom_mem(ADXL345_ADDRESS, ADXL345_DATAX0, 6)
    x, y, z = ustruct.unpack('<3h', data)
    xr = x*ADXL345_RESOLUTION
    yr = y*ADXL345_RESOLUTION
    zr = z*ADXL345_RESOLUTION
    return xr, yr, zr

def vector_magnitude(x, y, z):
    return math.sqrt(x**2 + y**2 + z**2)

class ActivityMonitor:
    def __init__(self):
        self.magnitude_window = deque(maxlen=WINDOW_SIZE)

    def add_sample(self, x, y, z):
        magnitude = vector_magnitude(x, y, z)
        self.magnitude_window.append(magnitude)

    def get_activity_level(self):
        if len(self.magnitude_window) < 2:
            return "low activity"

        diffs = [abs(self.magnitude_window[i] - self.magnitude_window[i - 1])
                 for i in range(1, len(self.magnitude_window))]

        avg_diff = sum(diffs) / len(diffs)

        if avg_diff < LOW_ACTIVITY_THRESHOLD:
            return "low activity"
        elif avg_diff < MEDIUM_ACTIVITY_THRESHOLD:
            return "medium activity"
        else:
            return "high activity"

# Main loop
activity_monitor = ActivityMonitor()
display_count = 0

while True:
    x, y, z = read_accel()
    activity_monitor.add_sample(x, y, z)
    activity = activity_monitor.get_activity_level()
    if (display_count % 10 == 0)
        print('--------------------')
        print(x, y, z)
        print("X: {}, Y: {}, Z: {}".format(x,y,z))

    if (display_count == 40)
        print('--------------------------------------------------------')
        print("Current Activity:", activity)
        print('--------------------------------------------------------')
        display_count = 0

    time.sleep(SAMPLE_DELAY)
