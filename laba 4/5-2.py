import RPi.GPIO as GPIO
import time

dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)


def dec2bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]


def adc():
    value = 128
    GPIO.output(dac, dec2bin(value))
    time.sleep(0.001)
    if GPIO.input(comp) == 1:
        value -= 64
    else:
        value += 64

    GPIO.output(dac, dec2bin(value))
    time.sleep(0.001)
    if GPIO.input(comp) == 1:
        value -= 32
    else:
        value += 32

    GPIO.output(dac, dec2bin(value))
    time.sleep(0.001)
    if GPIO.input(comp) == 1:
        value -= 32
    else:
        value += 16

    GPIO.output(dac, dec2bin(value))
    time.sleep(0.001)
    if GPIO.input(comp) == 1:
        value -= 8
    else:
        value += 8
    GPIO.output(dac, dec2bin(value))
    time.sleep(0.001)
    if GPIO.input(comp) == 1:
        value -= 4
    else:
        value += 4
    GPIO.output(dac, dec2bin(value))
    time.sleep(0.001)
    if GPIO.input(comp) == 1:
        value -= 2
    else:
        value += 2
    GPIO.output(dac, dec2bin(value))
    time.sleep(0.001)
    if GPIO.input(comp) == 1:
        value -= 1
    else:
        value += 1
    GPIO.output(dac, dec2bin(value))

    return value


try:
    while True:
        value = adc()
        voltage = 3.3 * value / 256
        if value != 0:
            print(f"Value: {value}, Voltage: {voltage:.2f}V")

finally:
    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()
