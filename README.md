# SUNNY-CP: a CP Portfolio Solver

SUNNY-CP [5] is a parallel portfolio solver that allows one to solve constraint 
satisfaction/optimization problems defined in the MiniZinc language [6].
It implements the SUNNY algorithm described in [1][2][3] and extends its 
sequential version [4].

SUNNY-CP can use any CP solver supporting the MiniZinc language (more precisely,
interpreting the FlatZinc language). In a nutshell, it relies on two steps:

  1. PRE-SOLVING: the (parallel) execution of a (maybe empty) static schedule, 
     and the neighborhood computation for the underlying k-NN algorithm;

  2. SOLVING: the (parallel) cooperative execution of the solvers' schedule 
     returned  by the SUNNY algorithm.

SUNNY-CP won the gold medal in the open track of MiniZinc Challenges 2015, 2016,
and 2017, and the silver medal in 2018 and 2019 [6].

## Contents

+ `bin`     contains the executables of SUNNY-CP
+ `kb`      contains the utilities for the knowledge base of SUNNY-CP
+ `src`     contains the sources of SUNNY-CP
+ `solvers` contains the utilities for the constituent solvers of SUNNY-CP
+ `test`    contains some MiniZinc examples for testing SUNNY-CP
+ `docker`	contains the dockerfile used to generate the image in the dockerhub
+ `tmp`     possibly contains the temporary files produced by SUNNY-CP

## Installation & Usage

You can install SUNNY-CP on your local machine, or use it via [Docker](https://www.docker.com)

### Local installation

To install SUNNY-CP locally, you need to install first:
+ Python (version >= 3)
+ MiniZinc (version >= 2.6.4)
+ `mzn2feat` feature extractor, available at [https://github.com/CP-Unibo/mzn2feat](https://github.com/CP-Unibo/mzn2feat).

Then, run the command `sunny-cp/install.sh`. This script performs pre-checks,
compiles the Python sources and adds the default solvers to the portfolio of 
SUNNY-CP. The default portfolio includes the following MiniZinc solvers:
+ Chuffed
+ COIN-BC
+ Gecode

However, the user can specify its own portfolio, provided that each of its 
solvers is installed in the MiniZinc bundle, that is, it can be run via the 
`minizinc --solver <solver>` command. For more details on how to build a 
user-defined portfolio, please see the README file in the `sunny-cp/solvers` 
folder.

After the installation, you can test SUNNY-CP by running the 
`sunny-cp/test/examples/run_examples` script.

### Docker installation

To install SUNNY-CP via Docker, you need to download the Docker image available 
in Docker Hub with the command:
```
sudo docker pull jacopomauro/sunny-cp
```

To execute SUNNY-CP from command line you can use the command
```
sudo docker run --rm -i -t jacopomauro/sunny-cp
```

You will get shell control inside the docker container and you can trigger
SUNNY-CP by invoking the `sunny-cp` command (`sunny-cp --help` for getting
information on its command line usage). 

Note that SUNNY-CP will run inside the container. MiniZinc files can be
shared from the host computer to the Docker container by using Docker
volumes (see [https://docs.docker.com/storage/volumes/](https://docs.docker.com/storage/volumes/)
for more information). For example, assuming that the MiniZinc model `test.mzn` to
solve is in the folder `/host_dir`, you can run SUNNY-CP by first invoking the 
command 
```
sudo docker run --rm -it -v /host_dir:/cont_dir jacopomauro/sunny-cp
```
and then, after getting the shell, run the command
```
sunny-cp /cont_dir/test.mzn
```

## Features

During the presolving phase, SUNNY-CP possibly extracts a feature vector 
identifying the problem to solve. This is a necessary step for the *k*-nearest 
neighbours algorithm on which the SUNNY approach relies on.

By default, the feature vector is extracted by the `mzn2feat` tool.
However, the user can define its own extractor by implementing a corresponding 
class in `sunny-cp/src/features.py`.

## Knowledge Base

The SUNNY algorithm needs a knowledge base, stored by SUNNY-CP in a folder 
containing all the relevant information for the schedule computation.
By default, the knowledge base of SUNNY-CP is empty. But the user can define its 
own knowledge base. For more details, see the README file in the `sunny-cp/kb` folder.

## Authors

SUNNY-CP is developed by Roberto Amadini (University of Bologna) and 
Jacopo Mauro (University of Southern Denmark). For any question or information, 
please contact us:
+ roberto.amadini *at* unibo.it
+ mauro.jacopo *at* gmail.com

Other contributors:
+ Tong Liu
+ Mario Sabatini
+ Sebastian Kosch


## Acknowledgement

We would like to thank the staff of the former Optimization Research Group of 
NICTA (National ICT of Australia) for granting us the computational resources 
needed for building and testing SUNNY-CP.

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
