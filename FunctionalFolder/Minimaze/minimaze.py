from lammps import PyLammps
import FunctionalFolder.Output as Output

# Убрать лишний вывод в терминале 
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

from ase import Atoms
from deepmd.calculator import DP
from ase.optimize import BFGS
from ase.io import read
from ase.io.vasp import write_vasp
from ase.constraints import UnitCellFilter


def check_structure(structure, count_structures, Nbest, pe_str, ediff, prefix_out):

     name_structure = structure
     #print(name_structure)

     structure = Atoms(read(name_structure), pbc=True, calculator=DP(model="./Specific/graph_mod5.pb"))
  
     uf = UnitCellFilter(structure)
     relax = BFGS(uf, logfile = 'min.log')
     relax.run(fmax=ediff)

     pe = structure.get_potential_energy()
    
     if count_structures <= Nbest:
          name_structure = name_structure.split('/')[-1]
          pe_str[str(name_structure)] = float(pe)
          coord = structure.get_positions()
          box = structure.get_cell()

          card = structure.get_chemical_symbols()

          elem_card = get_ase_elem_card(card)
          
          structure_new = Atoms(elem_card, positions = coord, cell = box)
          write_vasp('./Result/' + prefix_out + '/' + name_structure, structure_new)
          
     else:
          pe_str = dict(sorted(pe_str.items(), key=lambda item: item[1]))
        
          keys_list = list(pe_str.keys())
          key_max_energy = keys_list[-1]
          pe_max = pe_str[str(key_max_energy)]
        
          if pe < pe_max:
               del pe_str[str(key_max_energy)]

               name_structure = name_structure.split('/')[-1]
               pe_str[str(name_structure)] = float(pe)

               coord = structure.get_positions()
               box = structure.get_cell()
               card = structure.get_chemical_symbols()
               elem_card = get_ase_elem_card(card)
               structure_new = Atoms(elem_card, positions = coord, cell = box)
               write_vasp('./Result/' + prefix_out + '/' + name_structure, structure_new)

     return (pe_str)

def get_ase_elem_card(card):

     card_dict ={}
     for i in card:
          if i in card_dict:
               card_dict[i] += 1
          else:
               card_dict[i] = 1

     card_ase = list(card_dict.items())

     card = ''
     for i in range(len(card_ase)):
          card+=str(card_ase[i][0]) + str(card_ase[i][1])

     return card
