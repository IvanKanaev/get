import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

GPIO.setmode(GPIO.BCM)

dac = [8, 11, 7, 1, 0, 5, 12, 6]
leds = [2, 3, 4, 17, 27, 22, 10, 9]
comp = 14
troyka = 13

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)


def dec2bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]


def adc():
    t = 0.005
    value = 128
    GPIO.output(dac, dec2bin(value))
    time.sleep(t)
    if GPIO.input(comp):
        value -= 64
    else:
        value += 64
    GPIO.output(dac, dec2bin(value))
    time.sleep(t)
    if GPIO.input(comp):
        value -= 32
    else:
        value += 32
    GPIO.output(dac, dec2bin(value))
    time.sleep(t)
    if GPIO.input(comp):
        value -= 32
    value += 16
    GPIO.output(dac, dec2bin(value))
    time.sleep(t)
    if GPIO.input(comp):
        value -= 8
    else:
        value += 8
    GPIO.output(dac, dec2bin(value))
    time.sleep(t)
    if GPIO.input(comp):
        value -= 4
    else:
        value += 4
    GPIO.output(dac, dec2bin(value))
    time.sleep(t)
    if GPIO.input(comp):
        value -= 2
    else:
        value += 2
    GPIO.output(dac, dec2bin(value))
    time.sleep(t)
    if GPIO.input(comp):
        value -= 1
    else:
        value += 1
    GPIO.output(dac, dec2bin(value))
    time.sleep(t)
    if GPIO.input(comp):
        value -= 1
    return value


try:
    measures = []
    start_time = time.time()
    voltage = 0

    print("Начало зарядки конденсатора")
    GPIO.output(troyka, 1)
    while voltage < 192:
        voltage = adc()
        measures.append(voltage)
        # GPIO.output(leds, dec2bin(voltage))

    print("Начало разрядки конденсатора")
    GPIO.output(troyka, 0)
    while voltage > 128:
        voltage = adc()
        measures.append(voltage)
        # GPIO.output(leds, dec2bin(voltage))

    end_time = time.time()
    experiment_time = end_time - start_time
    period = experiment_time / len(measures)
    rate = 1 / period
    adc_step = 3.3 / 256

    with open('data.txt', 'w') as f:
        for value in measures:
            f.write(f"{value}\n")

    with open('settings.txt', 'w') as f:
        f.write(f"Средняя частота дискретизации: {rate:.2f} Гц\n")
        f.write(f"Шаг квантования АЦП: {adc_step:.5f} В\n")

    print(f"Общая продолжительность эксперимента: {experiment_time:.2f} сек")
    print(f"Период одного измерения: {period:.5f} сек")
    print(f"Средняя частота дискретизации: {rate:.2f} Гц")
    print(f"Шаг квантования АЦП: {adc_step:.5f} В")

    voltage_values = [value / 256 * 3.3 for value in measures]
    time_values = [i * period for i in range(len(measures))]

    plt.figure(figsize=(10, 6))
    plt.plot(time_values, voltage_values)
    plt.title("Процесс заряда и разряда конденсатора")
    plt.xlabel("Время, сек")
    plt.ylabel("Напряжение, В")
    plt.grid()
    plt.show()

finally:
    GPIO.output(leds, 0)
    GPIO.output(dac, 0)
    GPIO.cleanup()
