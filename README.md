# Traversal Distance Python Library
The traversal distance is a generalization of Fréchet distance for the graph vs graph case. More formally, given two embedded, connected graphs $H = (V_H ,E_H)$ and $G = (V_G,E_G)$ with straight edges, identifying $H$ and $G$ with the points lying on their edges we will call a mapping $f : [0,1] \rightarrow H $ which is continuous and surjective, a traversal of $H$ . A continuous (but not necessarily surjective) mapping $g : [0,1] \rightarrow G$ will be called a partial traversal of $G$. The traversal distance from $H$ to $G$ is defined as 
$ \delta_T(H, G)=\inf _{f, g} \max _{t \in[0,1]}\|f(t)-g(t)\|, $
where $f$ ranges over all traversals of $H$ and $g$ over all partial traversals of $G$.

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

# Publication:
Alt H., Efrat A., Rote G., and Wenk C., Matching Planer maps, Journal of Algorithms, Volume 49, Issue 2, November 2003, Pages 262-283
https://doi.org/10.1016/S0196-6774(03)00085-3

### Authors
**Dr. Carola Wenk** 
Tulane University
cwenk@tulane.edu

**Erfan Hosseini Sereshgi** 
Tulane University
shosseinisereshgi@tulane.edu

**Will Rodman** 
Tulane University
wrodman@tulane.edu

**Rena Repenning** 
Morgan Stanley
renarepenning.com

**Emily Powers**
Tulane University
epowers3@tulane.edu

### Lisence
MIT License • Copyright (c) 2022 Computational Geometry @ Tulane
