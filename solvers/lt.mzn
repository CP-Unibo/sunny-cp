% Basic MiniZinc model for capturing the redefinition of "x < y" constraint.
%
% mzn2fzn --no-output-ozn --output-to-stdout -I SOLVER/mzn-lib lt.mzn

var int: left_var;
var int: right_var;
constraint left_var < right_var;
solve satisfy;
