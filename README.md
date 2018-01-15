# SUNNY-CP 2.2

SUNNY-CP: a Parallel CP Portfolio Solver

sunny-cp [5] is a parallel parallel portfolio solver that allows to solve a
Constraint (Satisfaction/Optimization) Problem defined in the MiniZinc language.
It essentially implements the SUNNY algorithm described in [1][2][3] and extends
its sequential version [4] that attended the MiniZinc Challenge 2014 [6].
sunny-cp is built on top of state-of-the-art constraint solvers, including:
Choco, Chuffed, CPX, G12/LazyFD, G12/FD, G12/Gurobi, G12/MIP, Gecode, HaifaCSP,
JaCoP, iZplus, MinisatID, Mistral, Opturion, OR-Tools, Picat. These solvers are 
not included by default in sunny-cp, except for those already included in the 
MiniZinc bundle (i.e., Chuffed, G12/FD, G12/LazyFD, G12/MIP, and Gecode).
However, sunny-cp provides utilities for adding new solvers to the portfolio and
for customizing their settings. Moreover, sunny-cp enables to use more solvers 
via Docker (see below).

In a nutshell, sunny-cp relies on two sequential steps:

  1. PRE-SOLVING: consists in the parallel execution of a (maybe empty) static
     schedule and the neighborhood computation of underlying k-NN algorithm;

  2. SOLVING: consists in the parallel and cooperative execution of a number of
     the predicted solvers, selected by means of SUNNY algorithm.

sunny-cp won the gold medal in the open track of MiniZinc Challenges 2015, 2016,
and 2017 [6].

## Authors

sunny-cp is developed by Roberto Amadini (University of Melbourne) and Jacopo
Mauro (University of Oslo). For any question or information, please contact us:
* roberto.amadini at unimelb.edu.au
* mauro.jacopo  at gmail.com

## Prerequisites

sunny-cp is tested on 64-bit machines running Ubuntu 12.04, and not yet fully 
portable on other platforms. Some of the main requirements are:

+ Python (version >= 2)
  https://www.python.org/

+ MiniZinc (version >= 2.7.1)
  http://www.minizinc.org/

+ mzn2feat (version >= 1.2.1)
  http://www.cs.unibo.it/~amadini/mzn2feat-1.0.tar.bz2

+ psutil (version >= 2)
  https://pypi.python.org/pypi/psutil

+ click (version >= 6)
  http://click.pocoo.org/

## Contents

+ bin     contains the executables of sunny-cp

+ kb      contains the utilities for the knowledge base of sunny-cp

+ src     contains the sources of sunny-cp

+ solvers contains the utilities for the constituent solvers of sunny-cp

+ test    contains some MiniZinc examples for testing sunny-cp

+ tmp     is aimed at containing the temporary files produced by sunny-cp.

## Bacic Installation

Once downloaded the sources, move into sunny-cp folder and run install.sh:
```
  sunny-cp$ ./install.sh
```
This is a minimal installation script that checks the prerequisites, compiles 
all the python sources of sunny-cp and builds the portfolio of sunny-cp (e.g., 
it creates file SUNNY_HOME/src/pfolio_solvers.py).
If the installation is successful, you will see the following message:
```
  --- Everything went well!
  To complete sunny-cp installation you just have to add/modify the
  environment variables SUNNY_HOME and PATH:
  1. SUNNY_HOME must point to: "$PWD"/sunny-cp
  2. PATH must be extended to include: "$PWD"/bin
```
It is important to set such variables in order to use sunny-cp. Once the 
variables are set, check the installation by typing the command: 
```
  sunny-cp --help
```
for printing the help page.

## Solvers

By default, sunny-cp uses the solvers contained in the MiniZinc bundle, that is:
* G12/CBC
* G12/LazyFD
* G12/FD
* G12/MPI
* [Gecode](http://www.gecode.org/)
* [Chuffed](https://github.com/geoffchu/chuffed)

It is however possible to use, via Docker, the following solvers:
* [OR-Tools](https://code.google.com/p/or-tools/) (version v6.4.4495)
* [Choco](http://choco-solver.org/) (version 4.0.4)
* [Picat](http://picat-lang.org/) CP (version 2.2)
* [Picat](http://picat-lang.org/) SAT (version 2.2)
* [JaCoP](http://jacop.osolpro.com/) (version 4.4)
* [MinisatID](http://dtai.cs.kuleuven.be/krr/software/minisatid) (version 3.11.0)
* [HaifaCSP](http://strichman.net.technion.ac.il/haifacsp/) (version 1.3.0)

Once a solver is installed on your machine, it is easy to add it to 
the portfolio and to customize its settings. For more details, see the README 
file in the SUNNY_HOME/solvers folder and the sunny-cp usage.

Note that sunny-cp does not guarantee that its constituent solvers are bug free.
However, the user can check the soundness of a solution with the command line 
option `--check-solvers`.

## Features

During the presolving phase (in parallel with the static schedule execution) 
sunny-cp extracts a feature vector of the problem in order to compute the 
solvers schedule possibly run in the solving phase. By default, the feature 
vector is extracted by mzn2feat tool. sunny-cp provide the sources of this tool: 
for its installation, decompress the mzn2feat-1.0.tar.bz2 archive and follow the 
instruction in the README file of that folder. However, the user can define its 
own extractor by implementing a corresponding class in src/features.py

## Knowledge Base

The SUNNY algorithm on which sunny-cp relies needs a knowledge base, that
consists of a folder containing the information relevant for the schedule
computation. For the time being the default knowlege base of SUNNY-CP is empty.
However, the user has the possibility of defining its own knowledge bases.

The sunny-cp/kb/mznc1215 folder contains a knowledge base consisting of 76 CSP 
instances and 318 COP instances coming from the MiniZinc challenges 2012--2015.
Moreover, the knowledge base mznc15 used in the MiniZinc Challenges 2016--2017 
is also available. For more details, see the README file in sunny-cp/kb folder.

## Testing

Although a full support for automatic testing is not yet implemented, in the
sunny-cp/test/examples folder there is a number of simple MiniZinc models.
The user can test all the models by running the following command:

```
 test/examples$ ./run_examples
```

The run_examples script also produces output.log and errors.log files in the
test/examples folder, where the standard output/error of the tested models are
respectively redirected.

## Installation with Docker
*** TODO ***


## Acknowledgement

We would like to thank the staff of the former Optimization Research Group of 
NICTA (National ICT of Australia) for granting us the computational resources 
needed for building and testing sunny-cp. We also thank all the developers of 
the constituent solvers without which sunny-cp scould not exists.


## References

  [1]  R. Amadini, M. Gabbrielli, and J. Mauro. SUNNY: a Lazy Portfolio Approach
       for Constraint Solving 2013. In ICLP, 2014.

  [2]  R. Amadini, M. Gabbrielli, and J. Mauro. Portfolio Approaches for
       Constraint Optimization Problems. In LION, 2014.

  [3]  R. Amadini, and P.J. Stuckey. Sequential Time Splitting and Bounds
       Communication for a Portfolio of Optimization Solvers. In CP, 2014.

  [4]  R. Amadini, M. Gabbrielli, and J. Mauro. SUNNY-CP: a Sequential CP
       Portfolio Solver. In SAC, 2015.

  [5]  R. Amadini, M. Gabbrielli, and J. Mauro. A Multicore Tool for Constraint
       Solving. In IJCAI, 2015.

  [6]  MiniZinc Challenge webpage. http://www.minizinc.org/challenge.html
