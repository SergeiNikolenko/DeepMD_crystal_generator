from ase import Atoms
from deepmd.calculator import DP
from ase.io import read
from ase.io.vasp import write_vasp
import random as rnd
import numpy as np

# Загрузить начальную структуру и установить калькулятор
slab_1 = Atoms(read('0500.vasp'), pbc=True, calculator=DP(model="./pot/_mod37A.pb"))

# Получить позиции атомов и параметры ячейки
coord = slab_1.get_positions()
box = slab_1.get_cell()

# Установить параметры
Nat = 32
T = 500.0
steps = 201
thermo = 100
kbT = 1.0 / (T * 8.617333262e-5)
e1 = slab_1.get_potential_energy()

# Цикл Монте-Карло
for istep in range(steps + 1):
    print('step=', istep)

    # Выбрать два случайных атома
    atom1 = rnd.randint(0, Nat - 1)
    atom2 = rnd.randint(0, Nat - 1)

    # Поменять их местами
    coord[atom1], coord[atom2] = coord[atom2], coord[atom1]

    # Создать новый объект Atoms с обновленными координатами
    slab_2 = Atoms('Ti7V7Zr6Nb6Ta6N32', positions=coord, cell=box, pbc=True, calculator=DP(model="./pot/_mod37A.pb"))

    # Рассчитать потенциальную энергию новой структуры
    e2 = slab_2.get_potential_energy()

    # Критерий Метрополиса
    delE = e2 - e1
    if delE < 0:
        e1 = e2
    else:
        betta = np.exp(-delE * kbT)
        R = rnd.random()
        if betta > R:
            e1 = e2
        else:
            # Если не принято, вернуть позиции
            coord[atom1], coord[atom2] = coord[atom2], coord[atom1]

    # Сохранить структуру каждые thermo шагов
    if istep % thermo == 0:
        write_vasp(f'{istep:04}.vasp', slab_2)

print('jr')

