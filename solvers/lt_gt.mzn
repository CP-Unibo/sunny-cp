% Basic MiniZinc model for capturing the solver-specific redefinitions of 
% "llt < rlt" and "lgt > rgt" constraints.
%
% mzn2fzn --no-output-ozn --output-to-stdout -I <SOLVER>/mzn-lib lt_gt.mzn

% FIXME: Change.
%var int: LHS;
%var int: RHS;
%constraint LHS < RHS;
%solve satisfy;
var int: llt;
var int: rlt;
var int: lgt;
var int: rgt;
constraint llt < rlt;
constraint lgt > rgt;
solve satisfy;
