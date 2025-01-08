# DeepMD Crystal Generator

This repository provides a toolkit for modeling **co-crystals** using machine learning techniques. It includes efficient scripts tailored for **DeepMD** and **ACE**, optimized for execution on computational clusters with **Slurm** and **Screen**.

## Features

- **Crystal Structure Modeling**: Supports co-crystal generation and optimization.  
- **Integration with Quantum Espresso (QE)**: Provides utilities for converting data to QE format for further quantum mechanical simulations.  
- **Cluster Execution**: Optimized for large-scale computations on HPC clusters using Slurm and Screen.  
- **Preprocessing and Postprocessing Scripts**: Includes scripts for preparing input data and visualizing results.

## Repository Structure

- `FunctionalFolder/` – Contains functional scripts for specific tasks related to co-crystal modeling.  
- `Specific/` – Custom scripts for specialized modeling scenarios.  
- `old_script/` – Archive of older versions of scripts used in early stages of development.  
- `qe/` – Scripts and utilities for integration with **Quantum Espresso**.  
- `find.py` – Script for searching and filtering generated crystal structures based on specific criteria.  
- `plot_all_min.py` – Script for plotting the minimum energy configurations of generated crystals.  
- `run_multiple_times.py` – Utility for running multiple iterations of the generation process.  
- `start_mol.py` – Script for initializing molecular structures for modeling.  
- `vasp_to_QE.py` – Converter from **VASP** output to **Quantum Espresso** input format.  
- `INPUT.dat` – Example input file for the generator.

## Requirements

- Python 3.8+  
- DeepMD  
- Quantum Espresso  
- Slurm (for cluster execution)  
- Additional Python packages (listed in `requirements.txt` if available)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SergeiNikolenko/DeepMD_crystal_generator.git
   cd DeepMD_crystal_generator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Generating Crystals

To start the generation process, use the following command:
```bash
python start_mol.py --input INPUT.dat
```

### Running Multiple Iterations

To run multiple iterations of the process:
```bash
python run_multiple_times.py --iterations 10
```

### Converting VASP Output to QE Input

Use the following script to convert VASP output files to Quantum Espresso input format:
```bash
python vasp_to_QE.py --input vasp_output_file --output qe_input_file
```

## Contribution

Contributions are welcome! If you would like to improve the scripts or add new functionality, feel free to fork the repository and create a pull request.

## License

This project is licensed under the MIT License.
