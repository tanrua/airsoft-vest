import math
from collections import deque

# Constants for activity thresholds
LOW_ACTIVITY_THRESHOLD = 0.02
MEDIUM_ACTIVITY_THRESHOLD = 0.1
WINDOW_SIZE = 30

class ActivityMonitor:
    def __init__(self):
        self.magnitude_window = deque(maxlen=WINDOW_SIZE)

    def read_accel(self):
        # Replace with actual sensor reading logic
        return (0.0, 0.0, 1.0)

    def add_sample(self, x, y, z):
        magnitude = math.sqrt(x**2 + y**2 + z**2)
        self.magnitude_window.append(magnitude)

    def get_activity_level(self):
        if len(self.magnitude_window) < 2:
            return "low activity"
        diffs = [abs(self.magnitude_window[i] - self.magnitude_window[i - 1])
                 for i in range(1, len(self.magnitude_window))]
        avg_diff = sum(diffs) / len(diffs)
        if avg_diff < LOW_ACTIVITY_THRESHOLD:
            return "low"
        elif avg_diff < MEDIUM_ACTIVITY_THRESHOLD:
            return "medium"
        else:
            return "high"
