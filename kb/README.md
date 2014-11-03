WHAT IS A KNOWLEDGE BASE
========================

A knowledge base essentially consists in a folder named <KB> containing (at 
least) two CSV files separated by "|", namely: <KB>_csp and <KB>_cop.
These two "symmetric" files that encode the knowledge bases for CSPs and COPs 
respectively. In particular, each of them has records of the form:

  inst|feat|info

where:

  - inst: is an unique identifier of the problem instance
  - feat: is the feature vector [f_1, ...f_n] of inst. All features must be 
          numeric (e.g., inf or NaN values are not allowed)
  - info: is a dictionary of the form {s_1: I_1, ..., s_m: I_m} where:
      s_1, ..., s_m: are the solvers of the portfolio
      I_1, ..., I_m: are the relevant informations of the solver s_i on the 
                     instance inst. Each I_j is a dictionary containing the 
                     solver answer, solving time, score, and area (note that 
                     score and area make sense only for COPs, see [2][3]).

In addition, if you want to scale the features in a reduced range [a, b] and/or 
remove the constant features, it is possible to define a second pair of files: 
<KB>_lims_csp and <KB>_lims_cop. These are are instead python dictionaries of 
the form:

  {1: [min_1, max_1], ..., n: [min_n, max_n]}

where min_i and max_i are respectively the minimum and the maximum value of the 
i-th feature over all the training instances of the corresponding knowledge 
base. The purpose of these files is to ease the task of scaling/removing 
features for a new incoming instance, by avoiding to recompute for every new 
problem the minimum and the maximum value for each feature of the dataset.


BUILDING A KNOWLEDGE BASE
=========================

A new knowledge base can be manually built according to the above standards, or 
automatically set up starting from corresponding CSV files.
Let us suppose you want to build a new knowledge base <KB>. All you need is two 
CSV files, namely:

  <FEAT_FILE>: a CSV file separated by "|" containing records of the form:
                
                 inst|[f_1, ..., f_n] 
                 
               where inst is an unique identifier of the problem instance and 
               [f_1, ..., f_n] is its feature vector. All the features must be 
               numeric (e.g., inf or NaN values are not allowed)
               
  <INFO_FILE>: a CSV file separated by "|" containing records of the form:
               
                 inst|solver|goal|answer|time|val|values 
               
               where:
               
               - inst: is the unique identifier of the problem instance
               
               - solver: is the unique identifier of the solver 
               
               - goal: is either "sat" for satisfaction problems, "min" for 
                       minimization problems, or "max" for maximization problems
                       
               - info: is the solver answer on inst. It can be either:
                   (i)   sat: if solver finds at least a solution for inst
                   (ii)  uns: if solver proves that inst has no solution
                   (iii) unk: if solver does not give any answer for inst
                   (iv)  opt: if solver finds an optimal solution for inst and 
                              proves its optimality (only for COPs)
               
               - time: is the time needed by solver to solve inst. Note that the 
                       following invariant must hold:
                       
                        info = unk \/ (goal != sat /\ info = sat) <==> time = T
                         
                       where T is the solving timeout.
               
               - val: is the best known objective value (i.e., the value of the 
                      objective function of inst) found by solver within the 
                      timeout T. Note that the following invariant must hold: 
                      
                        goal = sat \/ info = unk \/ info = uns <==> val = nan
               
               - values: is a dictionary of the form {t_1: v_1, ..., t_k: v_k} 
                         mapping the anytime performance of solver on inst. 
                         In particular v_i is the objective value found by 
                         solver at the time t_i (in seconds). 
                         Note that the following invariant must hold:
                         
                          t_i < T AND v_k = val AND (values = {} <==> val = nan)
                         
                         where T is the solving timeout and i = 1, ..., k.
                         
                         
  The "values" dictionary is used by SUNNY for computing the solving area. 
  Since it may be difficult to retrieve such values --- and since area is just 
  used in the COP schedule computation for breaking ties --- it is possible to 
  meet the above invariants even when the anytime performance of a solver is not 
  available by setting: values = {time: val}.

Once you have <FEAT_FILE> and <INFO_FILE>, just use the csv2kb.py script (in the 
folder SUNNY_HOME/kb/util) for creating a new knowledge base <KB>:

  csv2kb.py [OPTIONS] <KB> <FEAT_FILE> <INFO_FILE>

This allow you to create a folder named <KB> containing the corresponding 
knowledge base, i.e., a pair of files <KB>_csp and <KB>_cop (and eventually a 
pair <KB>_lims_csp and <KB>_lims_cop if features are scaled or removed). 
By default a knowledge base is created in the folder SUNNY_HOME/kb/<KB> by using 
a timeout of T = 1800 seconds, removing the constant features and scaling the 
feature values in the range [-1, 1]. The solving score and area are computed by 
scaling the partial solutions in the range [0.25, 0.75]. For more informations 
about the SUNNY algorithm and the score/area metrics we defer the interested 
reader to [1][2][3].


CUSTOMIZING A KNOWLEDGE BASE
============================

The user can change the default settings. For more details, type:

  csv2kb.py --help

You can try the simple example provided in the util folder:

  python csv2kb.py -p . -f 0,1 kb_example example.feat example.info

that builds a knowledge base named "kb_example" starting from example.feat and 
example.feat files by using 3 problems, 5 solvers and 10 features that will be 
scaled in the range [0, 1].

The default sunny-cp knowledge base is in kb/all_T1800. It consists of 5527 CSP 
instances and 4988 COP instances. It have been computed by considering the 
default solvers of sunny-cp (12 solvers), the default timeout (1800 seconds), 
the non-constant features extracted by mzn2feat tool (normalized in [-1, 1]), 
and the default settings for area and score. The original <FEAT_FILE> and 
<INFO_FILE> used for creating all_T1800 are compressed in all.feat.tar.bz2 and 
all_T1800.info.tar.bz2. From such files, it is possible via csv2kb.py script to 
rebuild the default knowledge bases or to create new ones (e.g., by setting a 
new timeout or new bounds).


REFERENCES
==========

  [1] R. Amadini, M. Gabbrielli, and J. Mauro. SUNNY: a Lazy Portfolio Approach 
      for Constraint Solving 2013. In ICLP, 2014.

  [2] R. Amadini, M. Gabbrielli, and J. Mauro. Portfolio Approaches for 
      Constraint Optimization Problems. In LION, 2014.

  [3] R. Amadini, and P.J. Stuckey. Sequential Time Splitting and Bounds 
      Communication for a Portfolio of Optimization Solvers. In CP, 2014.