import random as rnd
from lammps import lammps
import numpy as np

# Функция, задающая область симуляции
def set_region(xhi, yhi, zhi, xy, xz, yz):
    xy = rnd.randint(0, xhi)
    xz = rnd.randint(0, xhi)
    yz = rnd.randint(0, xhi)

    lmp.command(f'region box prism 0 {xhi} 0 {yhi} 0 {zhi} {xy} {xz} {yz}')

# Функция, задающая начальные параметры для симуляции LAMMPS
def set_start_command():
    lmp.command('units metal')
    lmp.command('atom_style atomic')
    lmp.command('boundary p p p')
    lmp.command('box tilt large')

    set_region(16, 16, 16, 0, 0, 0)

    lmp.file("input.in")

# Количество структур для создания
Nframe = 50
# Количество молекул для размещения внутри области
Nmol = 8
# Количество типов молекул
typeMOL = 2

# Основной цикл, создающий Nframe структур
for number_structures in range(Nframe):
    rnd.seed()
    
    lmp = lammps()
    set_start_command()
    
    # Задаем дамп (выходной файл) с координатами атомов и другими свойствами
    lmp.command(f"dump mydump1 all custom {Nmol} box.lmp id type element x y z #vx vy vz #fx fy fz")
    lmp.command("dump_modify mydump1 append yes element C H O N S Cl")
    
    number_region = 0
    region_list = []

    # Вложенный цикл, размещающий Nmol молекул внутри области
    while number_region < Nmol:
        R = rnd.randint(1, 424251)
        rand = rnd.randint(1, typeMOL)
        MOL = f'MOL_{rand}'
        reg = f'r{rnd.randint(1, 8)}'
        
        # Если регион еще не использовался, добавляем его в список и размещаем молекулу в нем
        if reg not in region_list:
            region_list.append(reg)
            number_region += 1
            print(reg, MOL)
                 
            lmp.command(f'fix 11 all deposit 1 0 1 {R} region {reg} mol {MOL}')
            lmp.command("run 1")
    
    # Закрываем экземпляр LAMMPS после завершения всех итераций
    lmp.close()