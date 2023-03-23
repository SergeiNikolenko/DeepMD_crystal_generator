from ase import Atoms
from deepmd.calculator import DP
from ase.optimize import BFGS
from ase.io import read
from ase.io.vasp import write_vasp
from ase.constraints import UnitCellFilter

# Загрузить структуру из файла VASP и установить калькулятор DeepMD
slab = Atoms(read('0500.vasp'), pbc=True, calculator=DP(model="./Specific/graph_mod3.pb"))

# Вывести параметры ячейки
print(slab.get_cell())

# Установить фильтр UnitCellFilter и оптимизировать ячейку и атомные позиции с использованием алгоритма BFGS
uf = UnitCellFilter(slab)
relax = BFGS(uf, logfile='None.log')
relax.run(fmax=0.07)

# Получить оптимизированные позиции атомов и параметры ячейки
coord = slab.get_positions()
print(slab.get_positions())
box = slab.get_cell()
print(slab.get_cell())

# Создать новый объект Atoms с оптимизированными позициями атомов и параметрами ячейки
slab_new = Atoms('C36H44O8N2S2', positions=coord, cell=box)

# Сохранить оптимизированную структуру в файл VASP
write_vasp('00.vasp', slab_new)


