import os
from ase.io.vasp import read_vasp
from ase.io.espresso import write_espresso_in

# определяем текущую директорию
directory = os.getcwd()

# цикл по всем файлам в текущей директории
for filename in os.listdir(directory):
    if filename.endswith('.vasp'):
        # определяем путь к файлам VASP и QE
        vasp_file = os.path.join(directory, filename)
        qe_file = os.path.join(directory, os.path.splitext(filename)[0] + '.in')

        # загружаем файл VASP в объект ASE Atoms
        atoms = read_vasp(vasp_file)

        # записываем объект Atoms в формат QE и записываем в файл
        with open(qe_file, 'w') as f:
            write_espresso_in(atoms=atoms, fd=f)
