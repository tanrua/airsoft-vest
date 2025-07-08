import tm1637_6_digit as tm1637
import time
import datetime
from machine import Pin

from led_controller import LEDController
from button_handler import ButtonHandler
from activity_monitor import ActivityMonitor
from game_state_manager import *  # contains GameStateManager and state constants

PIN_DISPLAY_CLK = 29
PIN_DISPLAY_DIO = 27
PIN_LEDS = 1
PIN_BUTTON = 31

# === Hardware Setup ===
tm = tm1637.TM1637(clk=Pin(PIN_DISPLAY_CLK), dio=Pin(PIN_DISPLAY_DIO))  # Adjust pins as needed
leds = LEDController(PIN_LEDS, 5)
button = ButtonHandler(PIN_BUTTON)
activity_monitor = ActivityMonitor()
game = GameStateManager()

# === Initialization ===
tm.show("setup")
leds.set_leds(["off"] * 5)

def display_time_remaining():
    timestring = str(datetime.timedelta(seconds=game.time_remaining))
    formatted_time = timestring.split(":")
    tm.numbers(int(formatted_time[0]), int(formatted_time[1]), int(float(formatted_time[2])))

def display_led_progress(count):
    count = max(0, min(count, 5))
    leds.set_leds(["red"] * count + ["green"] * (5 - count))

# === Main Game Loop ===
while True:
    time.sleep(1.0 / game.tps)
    game.time_tick += 1

    if 0 <= game.time_tick < game.tps:
        game.time_remaining = max(0, game.time_remaining - 1)
        display_time_remaining()
        game.time_tick = 0

    if game.time_remaining == 0:
        game.state = STATE_GAMEOVER

    x, y, z = activity_monitor.read_accel()
    activity_monitor.add_sample(x, y, z)
    activity = activity_monitor.get_activity_level()
    active = activity != "low activity"

    btn = button.read_button()

    if game.state == STATE_SETUP:
        if btn == "short":
            game.time_remaining += game.time_add
            display_time_remaining()
        elif btn == "long_2":
            for _ in range(2):
                tm.show("start")
                time.sleep(2)
                tm.show("game")
            display_time_remaining()
            leds.set_leds(["blue"] * 5)
            game.state = STATE_STANDBY

    elif game.state == STATE_STANDBY:
        if btn == "long_4":
            for _ in range(5):
                leds.set_leds(["off"] * 5)
                time.sleep(0.6)
                leds.set_leds(["blue"] * 5)
                time.sleep(0.6)
            for i in range(1, 6):
                leds.set_leds(["green"] * i + ["blue"] * (5 - i))
                time.sleep(0.4)
            leds.set_leds(["green"] * 5)
            time.sleep(1)
            for _ in range(5):
                time.sleep(0.6)
                leds.set_leds(["off"] * 5)
                tm.show("      ")
                time.sleep(0.6)
                leds.set_leds(["green"] * 5)
                display_time_remaining()
            game.state = STATE_COLD
            game.time_tick = 0

    elif game.state == STATE_HOT:
        if not active:
            game.cooldown_counter = 0
            game.state = STATE_COOLING
        else:
            game.hot_counter += 1
            if game.hot_counter >= 30 * game.tps:
                game.hot_counter = 0
                game.state = STATE_INCREMENT_LED

    elif game.state == STATE_COOLING:
        if not active:
            game.cooldown_counter += 1
            if game.cooldown_counter >= 2 * game.tps:
                game.cold_counter = game.warming_counter = 0
                game.state = STATE_COLD
        else:
            game.hot_counter = 0
            game.state = STATE_HOT

    elif game.state == STATE_COLD:
        if not active:
            game.cold_counter += 1
            if game.warming_counter > 0:
                game.warming_counter -= 1
        else:
            game.cold_counter += 1
            game.warming_counter += 1

        if game.cold_counter >= 60 * game.tps:
            game.cold_counter = game.hot_counter = 0
            game.state = STATE_DECREMENT_LED
        elif game.warming_counter >= 2 * game.tps:
            game.hot_counter = 0
            game.state = STATE_HOT

    elif game.state == STATE_INCREMENT_LED:
        for _ in range(3):
            leds.set_leds(["yellow"] * 5)
            time.sleep(0.5)
            display_led_progress(game.current_led_count)
            time.sleep(0.5)
        for _ in range(5):
            time.sleep(0.5)
            display_led_progress(game.current_led_count)
            time.sleep(0.5)
            display_led_progress(game.current_led_count + 1)
        game.current_led_count += 1
        if game.current_led_count == 5:
            tm.show("DANGER")
            for _ in range(5):
                leds.set_leds(["off"] * 5)
                time.sleep(0.6)
                leds.set_leds(["red"] * 5)
                time.sleep(0.6)
            game.time_remaining = max(0, game.time_remaining - game.time_loss)
        game.reset_counters()
        game.state = STATE_COLD

    elif game.state == STATE_DECREMENT_LED:
        if game.current_led_count > 0:
            for _ in range(3):
                leds.set_leds(["lime"] * 5)
                time.sleep(0.5)
                display_led_progress(game.current_led_count)
                time.sleep(0.5)
            for _ in range(5):
                time.sleep(0.5)
                display_led_progress(game.current_led_count)
                time.sleep(0.5)
                display_led_progress(game.current_led_count - 1)
            game.current_led_count -= 1
        game.reset_counters()
        game.state = STATE_COLD

    elif game.state == STATE_GAMEOVER:
        for _ in range(10):
            tm.show("      ")
            leds.set_leds(["off"] * 5)
            time.sleep(0.6)
            tm.show("000000")
            leds.set_leds(["red"] * 5)
            time.sleep(0.6)
        for msg in ["you", "let", "them", "die"]:
            tm.show(msg)
            time.sleep(1.5)
        time.sleep(2)
        while True:
            tm.show("      ")
            leds.set_leds(["off"] * 5)
            time.sleep(1.5)
            tm.show("GAME")
            leds.set_leds(["red"] * 5)
            time.sleep(1.5)
            tm.show("      ")
            leds.set_leds(["off"] * 5)
            time.sleep(1.5)
            tm.show("OVER")
            leds.set_leds(["red"] * 5)
            time.sleep(1.5)
