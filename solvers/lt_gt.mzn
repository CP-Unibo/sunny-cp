% Basic MiniZinc model for capturing the solver-specific redefinitions of 
% "x < y" and "x > y" constraints.
%
% mzn2fzn --no-output-ozn --output-to-stdout -I SOLVER/mzn-lib lt_gt.mzn

var int: llt;
var int: rlt;
var int: lgt;
var int: rgt;
constraint llt < rlt;
constraint lgt > rgt;
solve satisfy;
