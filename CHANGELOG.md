## sunny-cp CHANGELOG

#### Version 2.3

Major Changes:
* Upgrade MiniZinc version 2.3 (not compatible with lower versions)

Minor bugs and changes:
* Update choco, jacop, yuck version used


#### Version 2.2.1

Major Changes:
* Upgrade MiniZinc version to 2.2.1
* Remove the default solvers g12fd, g12lazyfd, g12mip
* Add new default solver g12osicbc
* New installation procedure based on docker image stored in docker hub
* Possibility to use sunny-cp as a service
* Default KB is empty

Minor bugs and changes:
* Sunny prints timing information for every solution found and at the end of its execution.


####Version 2.2

Major Changes:
* Included Gecode in the default solvers
* New solvers
* New knoledge base
* Changed docker policy: only solvers publicly available are included

Minor bugs and changes:
* Compatibility with mzn2feat 1.2
* fzn-exec are compressed into fzn-exec.tar.gz
* Bug fixing and cosmetic changes.

#### Version 2.1
Major bugs and changes:
* Compatibility with MiniZinc 2.0
* Solution checking (see option --check-solvers) and other user options 
    (-A, -R, -l, -u, --max-restarts, --switch-search)
* Installing with Docker
* New default knoledge base, including MiniZinc Challenge 2012--2015 instances

Minor bugs and changes:
* Modified bounds injection according to the new conventions of mzn2feat 2.0
* Modified the default values for -k, -P and -T options.
* Avoid to create a copy of MiniZinc model
* Avoid to set SUNNY_HOME environment variable
* Bug fixing and cosmetic changes.



