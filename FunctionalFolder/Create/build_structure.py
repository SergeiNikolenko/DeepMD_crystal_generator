import random as rnd
from lammps import lammps
from lammps import PyLammps

import FunctionalFolder.Output as Output

def lmp_create_structures(Nframe, init_mol_name, init_mol_count, elem_card, seedrnd, gen):
    number_structure = 0
    while number_structure < (Nframe +1 ):
       
        L = lammps() 
        lmp = PyLammps(ptr=L)
        insert_mol(lmp, init_mol_name, init_mol_count, seedrnd)

        valid = validation(lmp)
    
        if valid :
            continue

        Output.write_poscars(lmp, number_structure, elem_card, gen)

        number_structure += 1  

def get_input_mol():
    
    f_ = open('INPUT.dat')
    mol_name =[]
    mol_count = []

    data = []
    for line in f_:
        if len(line) > 1  and  line[0] !='#':
            temp = line.split()
            data.append(temp)
    
    for i in range(len(data)):
        if data[i-1][0] == '%molecules':
            while data[i][0] != '%end':
                mol_name.append(data[i][0])
                mol_count.append(int(data[i][1]))
                i+=1
    f_.close()
    del f_
        
    return mol_name, mol_count

def get_nframe_nbest():
    
    f_ = open('INPUT.dat')
   
    data = []
    for line in f_:
        if len(line) > 1  and  line[0] !='#':
            temp = line.split()
            data.append(temp)
    Nframe=0
    Nbest=0
    for i in range(len(data)):
        if data[i][0] == 'Nframe': Nframe = int(data[i][1])
        if data[i][0] == 'Nbest':  Nbest = int(data[i][1])
        if data[i][0] == 'seed':  seed = int(data[i][1])
        if data[i][0] == 'gen':   gen = str(data[i][1])


    f_.close()
    del f_
        
    return Nframe, Nbest, seed, gen

def insert_mol(lmp, init_mol_name, init_mol_count, seedrnd):

    set_start_command(lmp)

    Nmol = sum(init_mol_count)

    j=1
    for i in init_mol_name:
        lmp.command('molecule MOL_' + str(j) + ' ./Specific/' + str(i))
        j+=1

    Nreg = calc_region(lmp, init_mol_name, Nmol)
    
    seed = rnd.randint(0, seedrnd)

    number_region = 0
    region_list = []
    tru_number_region = 0
    mol_number = 0

    while number_region < Nmol:
        
        tru_number_region += init_mol_count[mol_number] 

        insert_mol = 1
        while insert_mol: 
        
            R = rnd.randint(1, seed)
            MOL = 'MOL_' + str(mol_number + 1)

            rand = rnd.randint(1, Nreg)
            reg = 'r' + str(rand)

            if reg not in region_list:
                region_list.append(reg)
                number_region +=1
                           
                #lmp.command('fix 11 all deposit 1 0 1 ' + str(R) + ' region ' + str(reg) + ' mol ' + str(MOL))
                lmp.command('fix 11 all deposit 1 0 1 ' + str(R) + ' region box near 1.5  mol ' + str(MOL))

                lmp.command("run 1")
                       
            if number_region == tru_number_region:
                insert_mol = 0
        
        mol_number+=1
    
    del lmp

def calc_region(lmp, init_mol_name, Nmol):
   
    mol_size = round(calc_box_size(init_mol_name))
    xhi = mol_size

    Nmolt=Nmol

    if Nmol == 3 : Nmolt=4
    if Nmol == 5 : Nmolt=6
    if Nmol == 7 : Nmolt=8
    if Nmol == 11: Nmolt=12
    if Nmol == 13: Nmolt=14
    if Nmol == 15: Nmolt=16


    if Nmolt == 1: 
        yhi = xhi
        zhi = xhi
        region_count = 1
    if Nmolt == 2:
        zhi = xhi
        yhi = xhi
        xhi = 2 * xhi
        region_count = 2
    if Nmolt == 4:
        zhi =  xhi
        yhi = 2 * xhi
        xhi = 2 * xhi
        region_count = 4
    
    if Nmolt == 6:
        zhi = xhi
        yhi = 2 * xhi
        xhi = 3 * xhi
        region_count = 6
    
    if Nmolt == 8:
        zhi = 2 * xhi
        yhi = 2 * xhi
        xhi = 2 * xhi
        region_count = 8
    
    if Nmolt == 9:
        zhi = 3 * xhi
        yhi = 3 * xhi
        xhi = 3 * xhi
        region_count = 9
    
    if Nmolt == 10:
        zhi =  xhi
        yhi = 2 * xhi
        xhi = 5 * xhi
        region_count = 10
    
    if Nmolt == 12:
        zhi = 2 * xhi
        yhi = 2 * xhi
        xhi = 3 * xhi
        region_count = 12
    
    if Nmolt == 14:
        zhi = 1 * xhi
        yhi = 2 * xhi
        xhi = 7 * xhi
        region_count = 14
    
    if Nmolt == 16:
        zhi = 2 * xhi
        yhi = 2 * xhi
        xhi = 4 * xhi
        region_count = 16
   
    xy= rnd.randint(0, round(xhi/2))
    xz= rnd.randint(0, round(xhi/2))
    yz= rnd.randint(0, round(xhi/2))

    lmp.command('region box prism 0 ' + str(xhi) +' 0 ' + str(yhi) +' 0 ' + str(zhi) + ' ' + \
          str(xy) + ' ' + str(xz) + ' ' + str(yz))

    set_mass_mol(lmp)

    scale_x = int(xhi / mol_size)
    scale_y = int(yhi / mol_size)
    scale_z = int(zhi / mol_size)

    region_id = 0
    for i in range(scale_x):
        for j in range(scale_y):
            for k in range(scale_z):
                region_id +=1 
                xr = mol_size * (0.5 + i) 
                yr = mol_size * (0.5 + j) 
                zr = mol_size * (0.5 + k)

                lmp.command('region ' + 'r' + str(region_id) + ' block ' + str(xr) + ' ' + str(xr + 0.25) + \
                ' ' + str(yr) + ' ' + str(yr + 0.25) + ' ' + str(zr) + ' ' + str(zr + 0.25))
    del lmp           
    
    return region_count

def calc_mol_size(file_name):
    f_=open('./Specific/' + file_name)
  
    data = []
    k=0
    for line in f_:
        k+=1
        line = line[0: len(line)-1]
        temp = line.strip()
        data.append(temp)
    
    temp = data[2].split()
    Nat = int(temp[0])

    x=[]
    y=[]
    z=[]
    for i in range(Nat):
        temp=data[i+6].split()
        x.append(float(temp[1]))
        y.append(float(temp[2]))
        z.append(float(temp[3]))
    
    minx = min(x)
    miny = min(y)
    minz = min(z)

    maxx = max(x)
    maxy = max(y)
    maxz = max(z)
    
    delx = abs(maxx - minx)
    dely = abs(maxy - miny)
    delz = abs(maxz - minz)

    f_.close()
    del f_

    return max(delx, dely, delz)

def calc_box_size(init_mol):

    box_size = 0
    for i in init_mol:
        temp = calc_mol_size(i)
        if temp > box_size : box_size = temp
    
    return box_size 

def set_start_command(lmp):
    lmp.command('units metal')
    lmp.command('atom_style atomic')
    lmp.command('boundary p p p')
    lmp.command('box tilt large')
    del lmp

def set_mass_mol(lmp):

    f_ = open('INPUT.dat')
    elem_name =[]
    elem_mass = []

    data = []
    for line in f_:
        if len(line) > 1  and  line[0] !='#':
            temp = line.split()
            data.append(temp)
    
    for i in range(len(data)):
        if data[i-1][0] == '%elements':
            while data[i][0] != '%end':
                elem_name.append(data[i][0])
                elem_mass.append(data[i][1])
                i+=1

    lmp.command('create_box ' + str(len(elem_name)) +' box')

    k = 0
    for i in elem_mass:
        k = k + 1
        lmp.command('mass ' + str(k) + ' ' + i)

    #lmp.command('timestep 0.0001')
    #lmp.command('neighbor  1.0 bin')
    lmp.command('pair_style lj/cut 2.5')
    lmp.command('pair_coeff  * * 1 1')

    del lmp

    return elem_name

def validation(lmp):

    error = 0
 
    x=[]
    y=[]
    z=[]
    for i in range(lmp.system.natoms):
        xs, ys, zs = lmp.atoms[i].position
        x.append(float(xs))
        y.append(float(ys))
        z.append(float(zs))
    
    for i in range(1, len(x)):
        for j in range(i+1, len(x)):

            R = (x[i] - x[j])**2.0 + (y[i] - y[j])**2.0 +(z[i] - z[j])**2.0

            if R < 0.6: 
                error = 1
                break    
            
    del lmp

    return error

def get_elem_card():

    f_ = open('INPUT.dat')
    elem_name =[]

    data = []
    for line in f_:
        if len(line) > 1  and  line[0] !='#':
            temp = line.split()
            data.append(temp)
    
    for i in range(len(data)):
        if data[i-1][0] == '%elements':
            while data[i][0] != '%end':
                elem_name.append(data[i][0])
                i+=1
    
    f_.close()
    del f_
    
    return elem_name
      
   

    