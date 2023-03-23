import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Читаем данные из файла
with open('min.log', 'r') as f:
    lines = f.readlines()

steps = []
energies = []
fmaxs = []

for line in lines:
    if line.startswith('BFGS:'):
        parts = line.split()
        steps.append(int(parts[1]))
        energies.append(float(parts[3]))
        fmaxs.append(float(parts[4]))

# Удаляем дубликаты на оси x
unique_steps, unique_indices = np.unique(steps, return_index=True)
unique_energies = np.array([energies[i] for i in unique_indices])
unique_fmaxs = np.array([fmaxs[i] for i in unique_indices])

# Создаем функции интерполяции для энергии и максимальной силы
energies_interp = interp1d(unique_steps, unique_energies, kind='quadratic')
fmaxs_interp = interp1d(unique_steps, unique_fmaxs, kind='quadratic')

# Создаем новые массивы значений для более плавной интерполяции
new_steps = np.linspace(unique_steps[0], unique_steps[-1], num=1000, endpoint=True)
new_energies = energies_interp(new_steps)
new_fmaxs = fmaxs_interp(new_steps)

# Вычисляем среднее значение для каждой оси
avg_energy = np.mean(energies)
avg_fmax = np.mean(fmaxs)

# Создаем график
fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Steps')
ax1.set_ylabel('Energy', color=color)
ax1.plot(new_steps, new_energies, color=color)
ax1.axhline(y=avg_energy, color='gray', linestyle='--')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()

color = 'tab:blue'
ax2.set_ylabel('fmax', color=color)
ax2.plot(new_steps, new_fmaxs, color=color)
ax2.axhline(y=avg_fmax, color='gray', linestyle='--')
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
plt.show()