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

+ Gecode solver:
        http://www.gecode.org/
        
+ MinisatID solver:
        http://dtai.cs.kuleuven.be/krr/software/minisatid
	

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
