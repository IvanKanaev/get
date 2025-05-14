import matplotlib.pyplot as plt
import numpy as np

with open('settings.txt', 'r') as file:
    settings_lines = file.readlines()
    rate = float(settings_lines[0].split(':')[1].strip().split()[0])
    adc_step = float(settings_lines[1].split(':')[1].strip().split()[0])

period = 1.0 / rate

measures = np.loadtxt('data.txt', dtype=int)
voltage_values = measures * adc_step
time_values = np.array([i * period for i in range(len(measures))])

fig, ax = plt.subplots(figsize=(10, 6), dpi=100)

ax.plot(time_values, voltage_values, 'b-', linewidth=1, label='V(t)')
ax.scatter(time_values[::20], voltage_values[::20], marker='s', c='blue', s=10)

ax.set_xlim(time_values.min(), time_values.max())
ax.set_ylim(voltage_values.min(), voltage_values.max() + 0.2)

ax.grid(which='major', color='k', linestyle='-')
ax.grid(which='minor', color='gray', linestyle=':')
ax.minorticks_on()

ax.set_title("Процесс заряда и разряда конденсатора в RC цепи", pad=20)
ax.set_xlabel("Время, сек")
ax.set_ylabel("Напряжение, В")

ax.legend(shadow=False, loc='upper right')

plt.savefig('graph.png')
plt.savefig('graph.svg')

plt.show()

