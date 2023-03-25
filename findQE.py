try:
    import random as rnd
    import os
    import glob

    import FunctionalFolder.Minimaze as Minimaze
    import FunctionalFolder.Output as Output
    import FunctionalFolder.Input as Input

    # Чистим min.log 
    with open("min.log", "w") as log_file:
        log_file.write("")

    rnd.seed()

    Nframe, Nbest = Input.get_nframe_nbest()

    ediff = Input.get_ediff()

    path_remove = os.path.join(os.path.abspath(os.path.dirname(__file__)))

    prefix_in, prefix_out = Input.get_prefix()

    

    base_directory = os.path.join(path_remove, "Result")
    prefix_base = "Result"
    prefix_out = Input.get_next_available_prefix(base_directory, prefix_base)

    Input.copy_data(path_remove, prefix_in, prefix_out)


    
    pe_str = {}

    # Список для хранения имен файлов с исходными структурами
    in_structures = []
    for file in glob.glob(f'./{prefix_in}/*.vasp'): 
        in_structures.append(file)

    # Подсчет количества структур и обработка каждой структуры
    count_structures = 0
    for name_structure in in_structures:
        count_structures += 1
        
        pe_str = Minimaze.check_structure_QE2(name_structure, count_structures, Nbest, pe_str, ediff, prefix_out)
        print(name_structure, count_structures, Nbest, pe_str, ediff, prefix_out)
        # Запись результатов и удаление старых файлов через каждые Nframe структур
        if count_structures % Nframe == 0:
            Output.write_energy_table(pe_str, prefix_out)
            Output.remove_files(pe_str, path_remove, prefix_out)
            Output.write_check_point(count_structures, prefix_out)

    # Запись окончательных результатов и удаление старых файлов
    Output.write_energy_table(pe_str, prefix_out)
    Output.remove_files(pe_str, path_remove, prefix_out)

    print('Расчет оптимизированых структур окончен')
   
    pass
except KeyboardInterrupt:
    print("Программа прервана пользователем")