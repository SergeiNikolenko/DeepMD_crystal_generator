#!/bin/bash
for input_file in *.in; do
    output_file=${input_file%.in}.out
    mpirun -np 16 pw.x -in $input_file > $output_file
done