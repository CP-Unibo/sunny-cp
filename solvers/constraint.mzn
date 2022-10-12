% Basic MiniZinc model for capturing the solver-specific FlatZinc redefinition 
% of the "LHS < RHS" constraint. This model is processed by make_pfolio.py and 
% will be later used for injecting a new bound in a FlatZinc model.

var int: LHS;
var int: RHS;
constraint LHS < RHS;
solve satisfy;
