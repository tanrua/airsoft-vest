STATE_SETUP = 0
STATE_STANDBY = 1
STATE_HOT = 2
STATE_COOLING = 3
STATE_COLD = 4
STATE_INCREMENT_LED = 5
STATE_DECREMENT_LED = 6
STATE_GAMEOVER = 7

class GameStateManager:
    def __init__(self):
        self.state = STATE_SETUP
        self.time_remaining = 0
        self.time_tick = -1
        self.current_led_count = 0
        self.hot_counter = 0
        self.cooldown_counter = 0
        self.cold_counter = 0
        self.warming_counter = 0
        self.tps = 4
        self.time_add = 900 #15m
        self.time_loss = 300 #5m

    def reset_counters(self):
        self.hot_counter = 0
        self.cooldown_counter = 0
        self.cold_counter = 0
        self.warming_counter = 0
