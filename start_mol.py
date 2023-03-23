import random as rnd
import FunctionalFolder.Create as Create

rnd.seed()  # задаем случайное значение для генератора псевдослучайных чисел


init_mol_name, init_mol_count = Create.get_input_mol()
Nframe, Nbest, seed, gen = Create.get_nframe_nbest()  
elem_card = Create.get_elem_card()  

Create.lmp_create_structures(Nframe, init_mol_name, init_mol_count, elem_card, seed, gen)
