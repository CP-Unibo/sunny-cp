sunny-cp
========

CP portfolio based solver

The CP portfolio solver sunny-cp was developed by Roberto Amadini and Jacopo 
Mauro (University of Bologna / Lab. Focus INRIA).

This framework allows to solve a Constraint (Satisfaction/Optimization) Problem 
defined in MiniZinc language by using a portfolio approach.
It essentially implements the SUNNY algorithm described in [1]--[3].
Most of its constituent solvers are publicly available, except for Chuffed and 
G12/Gurobi which have been kindly provided by NICTA Optimization Research Group.

CONTENTS
========

  bin		contains the executable file sunny-cp
		
  src		contains the sources of sunny-cp
		
  kb		contains the knowledge base(s) of sunny-cp
		
  tmp		is aimed at containing the temporary files produced by sunny-cp.

  
PREREQUISITES
=============

sunny-cp is tested on a 64-bit machine running Ubuntu 12.04 and not yet portable 
on other platforms. Moreover, this package does not contain neither the sources 
and the binaries of the constituent solvers that should be installed separately.
Some of the main requirements are:

+ MiniZinc 1.6 suite:
  http://www.minizinc.org/

+ mzn2feat-1.0 feature extractor:
  http://www.cs.unibo.it/~amadini/mzn2feat-1.0.tar.bz2
  
Note that the commands of these two tools (e.g., mzn2fzn, flatzinc, mzn2feat)   
should be include in the PATH system variable.
        
The external solvers used in the portfolio, i.e., those that are not included 
in the MiniZinc suite,  have to be installed in the 'solvers' directory.
Following the rule convention used in the MiniZinc challenge, to install a 
solver XXX you have to:
* Install required packages for XXX.
* Install XXX in the directory 'solvers/XXX'.
* A FlatZinc executable named 'fzn-exec' is expected in the 'solvers/XXX' 
  directory
* The directory 'solvers/mzn-lib' must contains the solver MiniZinc
  globals/redefinition file.
  
  
INSTALL
=============

To be properly launched sunny-cp requires the setting of the variable 
SUNNY_HOME to the directory containing the program

If <install-dir> is the directory containing the code please add the following 
line to ~/.bashrc

export SUNNY_HOME="<install-dir>"
	

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
      Communication for a Portfolio of Optimization SolversIn CP, 2014.
