What is a SUNNY-CP Knowledge Base
=================================

A SUNNY-CP knowledge base consists in a folder named <KB> containing (at least) 
two CSV files separated by "|", namely: `<KB>_csp` and `<KB>_cop`.
These are two "symmetric" files encoding the knowledge bases for CSPs and COPs 
respectively. Each of them has records of the form:
```
  inst|feat|info
```
where:
+ `inst`: is an unique identifier of the problem instance
+ `feat`: is the feature vector `f_1, ..., f_n` of inst. All features must be 
numeric, inf or NaN values are not allowed
+ `info`: is a dictionary of the form `{s_1: I_1, ..., s_m: I_m}` where:
  + `s_1, ..., s_m`: are the solvers of the portfolio
  + `I_1, ..., I_m`: are the relevant information for solver `s_i` on 
    instance `inst`. Each `I_j` is a dictionary containing:
    solver answer, solving time, score, and area (note that 
    score and area make sense only for COPs, see [2][3]).

In addition, if you want to scale the features in a reduced range `[a, b]` and/or 
remove the constant features, it is possible to define a second pair of files: 
`<KB>_lims_csp` and `<KB>_lims_cop`. These are are Python dictionaries of 
the form:
```
  {1: [min_1, max_1], ..., n: [min_n, max_n]}
```
where `min_i` and `max_i` are respectively the minimum and the maximum value of 
the i-th feature over all the training instances of the corresponding knowledge 
base. The purpose of these files is to ease the task of scaling/removing 
features for a new incoming instance, by avoiding to recompute for every new 
problem the minimum and the maximum value for each feature of the dataset.


Building a Knowledge Base
=========================

A new knowledge base can be manually built according to the above standards, or 
automatically set up starting from corresponding CSV files.
Let us suppose you want to build a new knowledge base `<KB>`. All you need is two 
CSV files, namely:

+  `<FEAT_FILE>`: a CSV file separated by "|" containing records of the form `inst|[f_1, ..., f_n]` 
    where `inst` is the unique identifier of the problem instance and `[f_1, ..., f_n]` is its feature vector. All the features must be numeric, inf or NaN values are not allowed
               
+  `<INFO_FILE>`: a CSV file separated by "|" containing records of the form:
    ```inst|solver|goal|answer|time|val|values``` where:
    + `inst`: is the unique identifier of the problem instance
    + `solver`: is the unique identifier of the solver 
    + `goal`: is either "sat" for satisfaction problems, "min" for minimization problems, or "max" for maximization problems
    + `info`: is `solver` answer on `inst`. It can be either:
      + *sat*: if `solver` finds at least a solution for inst
      + *uns*: if `solver` proves that inst has no solution
      + *unk*: if `solver` does not give any answer for inst
      + *opt*: if `solver` finds an optimal solution for inst and proves its optimality (only for COPs)
               
    + `time`: is the time needed by solver to solve `inst`. The following invariant must hold:
    ```info = unk \/ (goal != sat /\ info = sat) <===> time = T```  where T is the solving timeout.
    + `val`: is the best known objective value (i.e., the value of the objective function of inst) found by solver within the timeout T. The following invariant must hold: ```goal = sat \/ info = unk \/ info = uns <==> val = nan```
    + `values`: is a dictionary of the form `{t_1: v_1, ..., t_k: v_k}` mapping the anytime performance of `solver` on `inst`. In particular `v_i` is the objective value found by `solver` at time `t_i` (in seconds). Note that the following invariant must hold: ```t_i < T AND v_k = val AND (values = {} <==> val = nan)``` where T is the solving timeout and i = 1, ..., k.
  The `values` dictionary is used by SUNNY for computing the solving area. 
  Since it may be difficult to retrieve such values -and since area is just 
  used in the COP schedule computation for breaking ties- it is possible to 
  meet the above invariant even when the anytime performance of a solver is not 
  known by setting the values dictionary to `{time: val}`.

Once you have `<FEAT_FILE>` and `<INFO_FILE>`, just use the `csv2kb.py` script 
in the `sunny-cp/kb/util` folder to create a new knowledge base `<KB>`:
```
csv2kb.py [OPTIONS] <KB> <FEAT_FILE> <INFO_FILE>
```
This allow you to create a folder named `<KB>` containing the corresponding 
knowledge base, i.e., a pair of files `<KB>_csp` and `<KB>_cop` (and possibly a 
pair `<KB>_lims_csp` and `<KB>_lims_cop` if features are scaled or removed). 
By default a knowledge base is created in the folder `kb/<KB>` by using a timeout 
of T = 1800 seconds, removing the constant features and scaling the feature 
values in the range [-1,1]. The solving score and area are computed by scaling 
the partial solutions in the range [0.25,0.75]. For more information about the 
SUNNY algorithm and the score/area metrics we refer the interested reader to 
[1][2][3].


Customizing a Knowledge Base
============================

The user can change the default settings. For more details, type:
```
  python csv2kb.py --help
```
E.g., you may try the simple example provided in the `util` folder:
```
  python csv2kb.py -p . -f 0,1 kb_example example.feat example.info
```
that builds a knowledge base named `kb_example` starting from `example.feat` and 
`example.info` files by using 3 problems, 5 solvers and 10 features that will be 
scaled in the range [0,1].

The default SUNNY-CP knowledge base is empty, however old knowledge bases can 
be found in `mznc1215` and `mznc15` folders as references.


References
==========

  [1] R. Amadini, M. Gabbrielli, and J. Mauro. SUNNY: a Lazy Portfolio Approach 
      for Constraint Solving 2013. In ICLP, 2014.

  [2] R. Amadini, M. Gabbrielli, and J. Mauro. Portfolio Approaches for 
      Constraint Optimization Problems. In LION, 2014.

  [3] R. Amadini, and P.J. Stuckey. Sequential Time Splitting and Bounds 
      Communication for a Portfolio of Optimization Solvers. In CP, 2014.
