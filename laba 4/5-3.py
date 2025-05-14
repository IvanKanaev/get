import RPi.GPIO as GPIO
import time

dac = [8, 11, 7, 1, 0, 5, 12, 6]
leds = [2, 3, 4, 17, 27, 22, 10, 9]
leds = leds[::-1]
comp = 14
troyka = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def dec2bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def adc():
    value = 0
    for i in range(7, -1, -1):
        value += 2**i
        GPIO.output(dac, dec2bin(value))
        time.sleep(0.005)
        if GPIO.input(comp) == 1:
            value -= 2**i
    return value

def volume(value):
    level = round(value/256*8)
    return [1 if i < level else 0 for i in range(8)]

try:
    while True:
        value = adc()
        if value != 0:
            GPIO.output(leds, volume(value))

finally:
    GPIO.output(dac, 0)
    GPIO.output(leds, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()
