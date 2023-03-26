import os
from ase import Atoms
from ase.optimize import BFGS
from ase.io import read
from ase.io.vasp import write_vasp, read_vasp
from ase.constraints import UnitCellFilter
from ase.calculators.espresso import Espresso

def check_structure_QE(structure_path, count_structures, Nbest, pe_str, ediff, prefix_out):
    
    # Считываем структуру из файла POSCAR
    structure = read_vasp(structure_path)
    
    # Настройка калькулятора
    pseudo_path = os.path.abspath('Specific/pseudo') 
    pseudopotentials = {'C': 'C.UPF',
                        'H': 'H.UPF',
                        'N': 'N.UPF',
                        'O': 'O.UPF',
                        'S': 'S.UPF'}
    input_data={
                        'control': {
                            'calculation': 'vc-relax',
                            'restart_mode': 'from_scratch',
                            'verbosity': 'high',
                            'prefix': 'qe',
                            'tprnfor': True,
                            'tstress': True,
                        },
                        'system': {
                            'ecutwfc': 10,
                            'ecutrho': 40,
                        },
                        'electrons': {
                            'conv_thr': ediff,
                        },
                        'ions': {
                            'ion_dynamics': 'bfgs',
                        },
                        'k_points': {
                            'generation': 'monkhorst-pack',
                            'gamma': False,
                            'kpoints': [2, 2, 2],
                        },
                    }
    calc = Espresso(pseudopotentials=pseudopotentials,
                    pseudo_dir=pseudo_path,
                    input_data=input_data)
 

    # Устанавливаем калькулятор для объекта Atoms
    structure.set_calculator(calc)

    uf = UnitCellFilter(structure)
    # Оптимизируем структуру
    relax = BFGS(uf, logfile='min.log')
    relax.run(fmax=ediff)

    # Получаем потенциальную энергию
    pe = structure.get_potential_energy()

    if count_structures <= Nbest:
        # Добавляем структуру в список лучших структур
        name_structure = structure_path.split('/')[-1]
        pe_str[name_structure] = float(pe)

        # Записываем структуру в файл в формате VASP
        write_vasp(prefix_out + '/' + name_structure, structure)
    else:
        # Заменяем структуру с наибольшей потенциальной энергией, если текущая энергия меньше
        pe_str = dict(sorted(pe_str.items(), key=lambda item: item[1]))
        keys_list = list(pe_str.keys())
        key_max_energy = keys_list[-1]
        pe_max = pe_str[key_max_energy]

        if pe < pe_max:
            del pe_str[key_max_energy]

            name_structure = structure_path.split('/')[-1]
            pe_str[name_structure] = float(pe)

            write_vasp(prefix_out + '/' + name_structure, structure)

    return pe_str
