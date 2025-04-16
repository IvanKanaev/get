import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)
pwm =GPIO.PWM(24, 1000)
pwm.start(0)
try:
    while True:
        try:
            duty_cicle = int(input())
            pwm.ChangeDutyCycle(duty_cicle)
            U = duty_cicle*3.3/100
            print("{:.2f}".format(U))
        except ValueError:
            print('введите числовое значение')
finally:
    pwm.stop()
    GPIO.cleanup()
