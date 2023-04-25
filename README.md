# Traversal Distance Python Library

### Command Line
To run the program, run a command line execution in the package with format:
```
python3 main.py <graph 1 filename: str> <graph 2 filename: str> <epsilon: float>
```

**Flags:**
* `-l` type: *str* logs the computation of the Traversal Distance to .log files.
* `-p` plots graph 1 and graph 2.

### Sample Inputs
Sample graph and curve files can be copied and pasted into the command line.
1. samples/paris/arc_de_triomphe samples/paris/vehicle
2. samples/athens/groundtruth samples/athens/kevin
3. samples/chicago/groundtruth samples/chicago/james

### Example
```
python3 main.py samples/athens/groundtruth samples/athens/kevin 300.0 -p
```
**Graphs Plotted:**
![Image](/docs/plot.jpg?raw=true)

**Traversal Distance Output:**
![Image](/docs/output.jpg?raw=true)

### Authors
**Dr. Carola Wenk** 
Tulane University
cwenk@tulane.edu

**Erfan Hosseini** 
Tulane University
shosseinisereshgi@tulane.edu

**Will Rodman** 
Tulane University
wrodman@tulane.edu

**Rena Repenning** 
Morgan Stanly
renarepenning.com

**Emily Powers**
Tulane University
epowers3@tulane.edu

### Lisence
MIT License • Copyright (c) 2022 Computational Geometry @ Tulane
