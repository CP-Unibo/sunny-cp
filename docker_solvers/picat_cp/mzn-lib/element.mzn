%-----------------------------------------------------------------------------%
% Requires that 'y' is the ith element of the array 'x'.
%-----------------------------------------------------------------------------%

include "element_bool.mzn";
include "element_float.mzn";
include "element_int.mzn";
include "element_set.mzn";

predicate element(var int: i, array[int] of var bool: x, var bool: y);

predicate element(var int: i, array[int] of var float: x, var float: y);

predicate element(var int: i, array[int] of var int: x, var int: y);

predicate element(var int: i, array[int] of var set of int: x,
        var set of int: y);
