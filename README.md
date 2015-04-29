sunny-cp 1.0
============

Sequential CP Portfolio Solver

The CP portfolio solver sunny-cp was developed by Roberto Amadini and Jacopo 
Mauro (University of Bologna / Lab. Focus INRIA).

This framework allows to solve a Constraint (Satisfaction/Optimization) Problem 
defined in MiniZinc language by using a portfolio approach.
It essentially implements the SUNNY algorithm described in [1][2][3].
Most of its constituent solvers are publicly available, except for Chuffed and 
G12/Gurobi which have been kindly granted by NICTA Optimization Research Group.
This is essentially the version of sunny-cp that attended the MiniZinc Challenge 
2014 [4]. A paper describing this tool is available at [5].

CONTENTS
========

  bin		contains the executable files of sunny-cp
  
  kb		contains the knowledge bases of sunny-cp
  
  src		contains the sources of sunny-cp
		
  tmp		is aimed at containing the temporary files produced by sunny-cp.

PREREQUISITES
=============

sunny-cp is tested on a 64-bit machine running Ubuntu 12.04 and not yet portable 
on other platforms. Some of the main requirements are:

+ MiniZinc 1.6
  http://www.minizinc.org/

+ mzn2feat 1.0
  http://www.cs.unibo.it/~amadini/mzn2feat-1.0.tar.bz2

SOLVERS
=======

This package does not contain neither the sources and the binaries of the 
constituent solvers, that should be installed separately.
A part of the solvers already included in MiniZinc 1.6, the other publicly 
available solvers used by the portfolio are:
  
+ Gecode
  http://www.gecode.org/

+ MinisatID
  http://dtai.cs.kuleuven.be/krr/software/minisatid

At the moment, the commands for running the constituent solvers on a given 
CSP/COP have to be set respectively in $SUNNY_HOME/src/exe_csp and 
$SUNNY_HOME/src/exe_csp scripts. Note that the failure (or the lack) of a 
constituent solver does not imply the overall failure of the portfolio: simply, 
that solver will be skipped when selected.
  
INSTALLATION
=============

To properly execute sunny-cp, the environment variable SUNNY_HOME must to be set 
to the directory where the tool was decompressed. If "sunny-dir" is that folder,
then please add the following line to your .bashrc file:

  export SUNNY_HOME="sunny-dir"

Moreover, please add the sunny-cp executables to your PATH:

  export PATH="${PATH}:${SUNNY_HOME}/bin"

Once the variables are set, type the command: 

  sunny-cp --help

for printing the help page.

TESTING
=======

In test/examples there is a number of simple MiniZinc models. You can run them 
individually, e.g.

  test/examples:~$ sunny-cp zebra.mzn

or alternatively you can test all the models of the folder by typing:

  test/examples:~$ ./run_examples 

	
FURTHER INFORMATION
===================

For any question or information, please contact us at:

  amadini at cs.unibo.it

  jmauro  at cs.unibo.it

REFERENCES
==========

  [1] R. Amadini, M. Gabbrielli, and J. Mauro. SUNNY: a Lazy Portfolio Approach 
      for Constraint Solving 2013. In ICLP, 2014.

  [2] R. Amadini, M. Gabbrielli, and J. Mauro. Portfolio Approaches for 
      Constraint Optimization Problems. In LION, 2014.

  [3] R. Amadini, and P.J. Stuckey. Sequential Time Splitting and Bounds 
      Communication for a Portfolio of Optimization Solvers. In CP, 2014.

  [4] MiniZinc Challenge 2014. 
      http://www.minizinc.org/challenge2014/results2014.html
      
  [5] R. Amadini, M. Gabbrielli, and J. Mauro. SUNNY-CP: a Sequential CP 
      Portfolio Solver. In SAC, 2015.