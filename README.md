# SUNNY-CP 2.2

SUNNY-CP: a Parallel CP Portfolio Solver

sunny-cp [5] is a parallel parallel portfolio solver that allows to solve a
Constraint (Satisfaction/Optimization) Problem defined in the MiniZinc language.
It essentially implements the SUNNY algorithm described in [1][2][3] and extends
its sequential version [4] that attended the MiniZinc Challenge 2014 [6].
sunny-cp is built on top of state-of-the-art constraint solvers, including:
Choco, Chuffed, CPX, G12/LazyFD, G12/FD, G12/Gurobi, G12/CBC, Gecode, HaifaCSP,
JaCoP, iZplus, MinisatID, Mistral, Opturion, OR-Tools, Picat. These solvers are 
not included by default in sunny-cp, except for those already included in the 
MiniZinc bundle (i.e., G12/CBC, G12/LazyFD, G12/FD, and Gecode).
However, sunny-cp provides utilities for adding new solvers to the portfolio and
for customizing their settings (see below).

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


## Installation & Usage by HTTP POST requests 

To install sunny-cp it is possible to use [Docker](https://www.docker.com) available for
the majority of the operating systems. It can then be used by simply sending a 
post request to the server deployed by using docker.

The Docker image is availabe in Docker Hub. To install it please run the
following commands.

```
sudo docker pull jacopomauro/sunny_cp
sudo docker run -d -p <PORT>:9001 --name sunny_cp_container jacopomauro/sunny_cp
```

where `<PORT>` is the port used to use the functionalities of the service.

Assuming that `<MZN>` is the path of the mzn file to solve,
to run the solver on it is possible to invoke it by a multipart post request as follows.

```
curl -F "mzn=@<MZN>" http://localhost:<PORT>/process
```

This will run sunny-cp with the default parameters on the minizinc instance.
If a `<DZN>` file is also needed, sunny-cp can be invoked as follows.

```
curl -F "mzn=@<MZN>" -F "dzn=@<DZN>" http://localhost:<PORT>/process
```

sunny-cp options can be passed by adding the string "option=value" as additional
part of the request.

For instance to solve the `<MZN>` using only the gecode solver (option `-P`)
the post request to perform is the following one.

```
curl -F "-P=gecode" -F "mzn=@<MZN>" http://localhost:<PORT>/process
```

To see the options supported by sunny-cp please run the following command.

```
curl -F "--help=" http://localhost:<PORT>/process
```

To select sunny-cp flags (like `--help` above) it is possible to add the string
"flag=".

To understand what are the solvers installed you can use the following get request.

```
curl http://localhost:<PORT>/solvers
```

Note that the post requests will return the output generate by sunny-cp at the
end of its execution. In case partial solutions are need, it is possible 
to interact with sunny-cp from command line as specified in the remaining part of 
the section.

#### Interacting with SUNNY-CP from command line

To interact with SUNNY-CP, it is possible to run the docker container getting
a direct access to the bash. This can be done by running the following command.

```
sudo docker run --entrypoint="/bin/bash" -i --rm -t jacopomauro/sunny_cp
```

This will give access to the bash and SUNNY-CP can be invoked by running the
`sunny-cp` command. To move the mzn and dzn files within the container
the `scp` command can be used or, alternatively, it is possible also to 
start the container with some shared volume (see
[Docker documentation](https://docs.docker.com/engine/admin/volumes/volumes/)
for more information.)

If they `sunny_cp_container` is already running it is possible to have bash
access to that container by running the following command.

```
sudo docker exec -i -t sunny_cp_container /bin/bash
```

Note that sunny-cp can be also installed on a Linux operating machine. To understand
the dependencies and the installation instructions, we invite the interested
user to consult the commands defined in the Dockerfile in the docker subfolder.

#### Cleaning

To clean up please lunch the following commands:

```
sudo docker stop sunny_cp_container
sudo docker rm sunny_cp_container
sudo docker rmi jacopomauro/sunny_cp
```

## Solvers supported

The default image of SUNNY-CP consists of the solvers included in the
[MiniZinc](http://www.minizinc.org) bundle (2.1.6 version):
* G12/CBC
* G12/LazyFD
* G12/FD
* G12/MPI
* [Gecode](http://www.gecode.org/)
* [Chuffed](https://github.com/geoffchu/chuffed)

Additionally, the default installation comes with the following solvers,
publicly available online:
* [OR-Tools](https://code.google.com/p/or-tools/) (version v6.4.4495)
* [Choco](http://choco-solver.org/) (version 4.0.4)
* [Picat](http://picat-lang.org/) CP (version 2.2)
* [Picat](http://picat-lang.org/) SAT (version 2.2)
* [JaCoP](http://jacop.osolpro.com/) (version 4.4)
* [MinisatID](http://dtai.cs.kuleuven.be/krr/software/minisatid) (version 3.11.0)
* [HaifaCSP](http://strichman.net.technion.ac.il/haifacsp/) (version 1.3.0)

These are the solvers that constitute the default portfolio (when not better specified,
the default portfolio consists of the solvers defined in the sunny-cp/solvers
directory).

Note that the included solvers are treated as black boxes, there is no guarantee
that they are bug free. The user can check
the soundness of a solution with the option `--check-solvers`.

#### Adding a solver

It is possible to add manually a solver in the portfolio and sunny-cp provides
utilities for adding new solvers to the portfolio and for
customizing their settings. If interested, more details
on how to add a solver can be found in the README file in the sunny-cp/solvers folder.

Previous version of SUNNY-CP for instance supported solvers that are currently not included
by default due to compilation problems
or the fact that are not publicly available/free. The old solvers that are not provided
with the current default configuration are:
* [Mistral](http://homepages.laas.fr/ehebrard/mistral.html) (version does not compile)
* [G12/Gurobi](http://www.gurobi.com/) (not free)
* [iZplus](http://www.constraint.org/ja/izc_download.html) (not publicly available)
* [Opturion](http://www.opturion.com) (not free)

We invite the developers interested in adding their solver
to the default image of sunny-cp to contact us.

## Features

During the presolving phase (in parallel with the static schedule execution)
sunny-cp extracts a feature vector of the problem in order to apply the k-NN
algorithm for determining the solvers schedule to be run in the following
solving phase. By default, the feature vector is extracted by the
[mzn2feat tool](https://github.com/CP-Unibo/mzn2feat).
The user can define its own extractor by implementing a corresponding
class in `src/features.py`.


## Knowledge Base

The SUNNY algorithm on which sunny-cp relies needs a knowledge base, that
consists of a folder containing the information relevant for the schedule
computation.
For the time being the default knowlege base of SUNNY-CP is empty.
However, the user has the possibility of defining its own knowledge bases.
For more details, see the README file in sunny-cp/kb folder.

In the sunny-cp/kb/mznc1215 folder it is possible to retrieve the 
knowledge base created in 2015 consisting of 76 CSP
instances and 318 COP instances coming from the MiniZinc challenges 2012--2015.
Moreover, also the knowledge base mznc15 used in the MiniZinc Challenge 2016 is available.

## Testing

Although a full support for automatic testing is not yet implemented, in the
sunny-cp/test/examples folder there is a number of simple MiniZinc models.
When using the tool from command line, the user can test all the models by running
the following command

```
 test/examples$ bash run_examples
```

The run_examples script also produces output.log and errors.log files in the
test/examples folder, where the standard output/error of the tested models are
respectively redirected.

## Acknowledgement

We would like to thank the staff of the Optimization Research Group of NICTA
(National ICT of Australia) for allowing us to use G12/Gurobi, as well as for
granting us the computational resources needed for building and testing sunny-cp.
We also thank all the developers of the constituent solvers without which sunny-cp
could not exists.


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
