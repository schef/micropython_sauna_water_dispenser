import time
from machine import Pin

GPIO_ENABLE = 27
GPIO_CLOCK = 26
GPIO_DIRECTION = 28

gpio_enable = None
gpio_clock = None
gpio_direction = None


def get_millis():
    return time.ticks_ms()


def millis_passed(timestamp):
    return time.ticks_diff(time.ticks_ms(), timestamp)


def set_enable(state):
    gpio_enable.value(int(not state))


def set_clock(state):
    gpio_clock.value(int(state))


def set_direction(state):
    gpio_direction.value(int(state))


def init():
    print("init")
    global gpio_enable, gpio_clock, gpio_direction
    gpio_enable = Pin(GPIO_ENABLE, Pin.OUT)
    set_enable(False)
    gpio_clock = Pin(GPIO_CLOCK, Pin.OUT)
    gpio_direction = Pin(GPIO_DIRECTION, Pin.OUT)


def rotate_degrees(degrees, speed = 1.0):
    #full circle = 3200hz for 500ms
    freqhz = 5000 * speed
    duration = (1000 / (freqhz / 1600)) * (degrees / 360)

    direction = bool(duration > 0)

    print(f"deg={degrees}; speed={speed}; freq={freqhz}; dur={duration}; dir={direction}")

    if duration < 0: duration = duration * -1

    set_enable(True)

    set_direction(direction)
    run_clock(freqhz, duration)

    set_direction(True)
    set_enable(False)


def run_clock(freqhz, duration_ms):
    period_us = (1000000 / freqhz)
    sleep_us = int(period_us / 2)
    for i in range(int((duration_ms * 1000) / period_us)):
        set_clock(True)
        time.sleep_us(sleep_us)
        set_clock(False)
        time.sleep_us(sleep_us)


def test_clock(num=5000, sleep=100):
    for i in range(num):
        set_clock(True)
        time.sleep_us(sleep)
        set_clock(False)
        time.sleep_us(sleep)


def run():
    pass
