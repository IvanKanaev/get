import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
dac = [8, 11, 7, 1, 0, 5, 12, 6]
GPIO.setup(dac, GPIO.OUT)
def dec2bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]
try:
    while True:
        try:
            T = float(input())
            t = T/512
            for value in range(256):
                GPIO.output(dac, dec2bin(value))
                time.sleep(t)
            for value in range(254, 0, -1):
                GPIO.output(dac, dec2bin(value))
                time.sleep(t)
        except ValueError:
            print('введено не числовое значение')
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
