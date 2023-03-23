import os
import numpy as np
#from collections import Counter

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
    
    f_.close()
    del f_

    return Nframe, Nbest

def get_ediff():
    
    f_ = open('INPUT.dat')
   
    data = []
    for line in f_:
        if len(line) > 1  and  line[0] !='#':
            temp = line.split()
            data.append(temp)
   
    for i in range(len(data)):
        if data[i][0] == 'ediff': 
            ediff = float((data[i][1]))
    f_.close()
    del f_

    return ediff

def get_prefix():
    
    f_ = open('INPUT.dat')
   
    data = []
    for line in f_:
        if len(line) > 1  and  line[0] !='#':
            temp = line.split()
            data.append(temp)
   
    for i in range(len(data)):
        if data[i][0] == 'prefix_in':  in_f  = data[i][1]
        if data[i][0] == 'prefix_out': out_f = data[i][1]

    f_.close()
    del f_
    
    return in_f, out_f

def copy_data(path_remove, prefix_in, prefix_out):

    import os, shutil
    path_result = path_remove + '/Result/' + prefix_out
    path_in = path_remove + '/' + prefix_in

    if not os.path.exists(path_result): 
        os.makedirs(path_result)

    if os.path.exists(path_result + '/Initstr'): 
        shutil.rmtree(path_result + '/Initstr')

    shutil.copytree(path_in, path_result + '/Initstr')


def get_next_available_prefix(base_dir, prefix_base):
        i = 1
        while True:
            prefix_candidate = f"{prefix_base}{i}"
            candidate_dir = os.path.join(base_dir, prefix_candidate)
            if not os.path.exists(candidate_dir):
                break
            i += 1
        return prefix_candidate