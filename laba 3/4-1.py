import RPi.GPIO as GPIO

dac = [8, 11, 7, 1, 0, 5, 12, 6]
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]
try:
    while True:
        a = input()
        if a == 'q':
            break
        try:
            number = float(a)
            if number % 1 != 0:
                print('введено не целое число')
                continue
            number = int(a)
            if number < 0:
                print('введено отрицательное значение')
                continue
            if number > 255:
                print('введено значение больше 255')
                continue
            GPIO.output(dac, decimal2binary(number))
            print("{:.4f}".format(number/256*3.3))
        except ValueError:
            print('введено не числовое значение')
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
