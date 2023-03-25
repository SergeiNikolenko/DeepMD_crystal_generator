import numpy as np
from collections import Counter

def write_poscars(lmp, number_structure, elem_card, gen): 
    
    #cell parametrs
    a = lmp.eval('cellalpha')
    b = lmp.eval('cellbeta')
    o = lmp.eval('cellgamma')

    g = lmp.eval('cella')
    h = lmp.eval('cellb')
    y = lmp.eval('cellc')

    pi = np.pi / 180

    a1 = g
    b1 = h * np.cos(o * pi)
    b2 = h * np.sin(o * pi)

    c1 = y * np.cos(b*pi)
    c2 = y * (np.cos(a*pi)-np.cos(b*pi) * np.cos(o*pi)) / np.sin(o*pi)
    c3 = y * np.sqrt(1+2 * np.cos(a*pi) * np.cos(b*pi) * np.cos(o*pi) - np.cos(a*pi)**2-np.cos(b*pi)**2-np.cos(o*pi)**2) / np.sin(o*pi)

    #coordinates
    xs=[]
    ys=[]
    zs=[]
    atom_type=[]

    for i in range(lmp.system.natoms):
        xss, yss, zss= lmp.atoms[i].position
        at = lmp.atoms[i].type
        xs.append(xss)
        ys.append(yss)
        zs.append(zss)
        atom_type.append(at)
  
    c = Counter(atom_type)
  
    elem_str=''
    elem_count_str=''
    for i in range(len(elem_card)):
        elem_str += elem_card[i] + ' '
        elem_count_str += str(c[i+1]) + ' '
    
    if number_structure < 10:
        name = '00' + str(number_structure)
    elif number_structure < 100:
        name = '0' + str(number_structure)
    elif number_structure < 1000:
        name = str(number_structure)

    
    f_ = open('./Startmol/' + name +'_'+ gen + '.vasp' , 'w')

    f_.write(elem_str + '\n' + '1' + '\n')
    f_.write(str(a1) + ' 0.0 0.0\n')
    f_.write(str(b1) +' ' + str(b2) + ' 0.0\n')
    f_.write(str(c1) +' ' + str(c2) +' ' + str(c3) +'\n')
    f_.write(elem_str + '\n')
    f_.write(elem_count_str + '\n')
    f_.write('Cartesian\n')

    for k in range(len(elem_card)):
        for i in range(len(atom_type)):
            if atom_type[i] == k + 1:
                f_.write(str(xs[i]) + ' ' + str(ys[i]) + ' ' + str(zs[i]) +'\n')
    
    del lmp
   
def write_lammps(lmp, number_structure):
    elements = 'C H O N S'
    lmp.command("dump mydump1 all custom 1 ./Result/lmp_" + str(number_structure) + ".lmp id type element x y z fx fy fz")
    lmp.command("dump_modify mydump1 append yes element C H O N S")
    lmp.command("write_data ./Result/lmp_" + str(number_structure) + ".dat")
    lmp.command('run 0')
    
    del lmp
    
def write_energy_table(pe_str, prefix_out):

    pe_str = dict(sorted(pe_str.items(), key=lambda item: item[1]))

    #print(pe_str)

    with open('./Result/' + prefix_out +'/!best_structures.dat','w') as out:
        for key,val in pe_str.items():
            out.write('{}\t{}\n'.format(key,val))

def write_check_point(point, prefix_out):

    with open('./Result/' + prefix_out + '/!check_point.dat','w') as out:
        out.write(str(point) + '\n')
    
def remove_files(pe_str, path_remove, prefix_out):
    import glob, os

    file_list_old=[]
    file_list_new = []

    for i in glob.glob('./Result/' + prefix_out + '/*.vasp'):
        i = i.split('/')[-1] 
        file_list_old.append(i)
       
    for i in pe_str:
        i = i.split('/')[-1]
        file_list_new.append(i)
    
    #print(file_list_old)
    #print(file_list_new)

    for i in file_list_old:
        if i not in file_list_new:  
            file_remove = '/Result/' + prefix_out + '/' + i 
            path_del =  path_remove + file_remove
            os.remove(path_del)

def convert_vasp_to_qe(path_to_vasp_files):
    
    import os
    from ase.io import read, write
    
    # Преобразование файлов
    for file_name in os.listdir(path_to_vasp_files):
        if file_name.endswith(".vasp"):
            # Загрузка структуры из VASP файла
            atoms = read(os.path.join(path_to_vasp_files, file_name))

            # Сохранение структуры в формате QE в новом файле
            write(os.path.join(path_to_vasp_files, file_name.replace(".vasp", ".in")), atoms, format="espresso-in")
            
            # Удаление файла VASP
            os.remove(os.path.join(path_to_vasp_files, file_name))
            

    # Получить список файлов с расширением ".in"
    files = [f for f in os.listdir(path_to_vasp_files) if f.endswith('.in')]
    print(files)
    # Применить код к каждому файлу
    for filename in files:
        with open(os.path.join(path_to_vasp_files, filename), "r") as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            if 'K_POINTS gamma' in line:
                lines = lines[i + 1:]
                break
        with open(os.path.join(path_to_vasp_files, filename), "w") as f:
            f.writelines(lines)

    print("Конвертация файлов завершена")

