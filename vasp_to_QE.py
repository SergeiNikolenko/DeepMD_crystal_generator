import os
from ase.io import vasp, write

# переходим в папку Result
os.chdir('Result')

# выводим список имеющихся папок
folders = sorted([folder for folder in os.listdir() if folder.startswith('Result')])
for i, folder in enumerate(folders):
    print(f'{i+1}. {folder}')

# запрашиваем у пользователя номер папки
folder_number = int(input('Введите номер папки: '))

# переходим в выбранную папку и преобразуем файлы .vasp в файлы input
folder_name = folders[folder_number-1]
os.chdir(folder_name)

vasp_files = [file for file in os.listdir() if file.endswith('.vasp')]
for file in vasp_files:
    atoms = vasp.read_vasp(file)
    input_file = file.replace('.vasp', '.in')
    write(input_file, atoms, format='espresso-in', symmetry='none')


import os
import shutil

# Возвращаемся в директорию со скриптом
os.chdir('../../')

# Создаем папку qe, если ее нет
if not os.path.exists('qe'):
    os.mkdir('qe')

# Заходим в папку qe
os.chdir('qe')

# Создаем папку folder_name, если ее нет
folder_name = folder_name
if not os.path.exists(folder_name):
    os.mkdir(folder_name)

# Копируем нужные файлы
for file in os.listdir('../Result/{}'.format(folder_name)):
    if file.endswith('.in'):
        shutil.copy('../Result/{}/{}'.format(folder_name, file), '{}/{}'.format(folder_name, file))
