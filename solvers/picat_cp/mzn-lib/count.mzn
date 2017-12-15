%-----------------------------------------------------------------------------%
% Constrains 'c' to be the number of occurrences of 'y' in 'x'. 
%-----------------------------------------------------------------------------%

predicate count(array[int] of var int: x, var int: y, var int: c);

predicate count_reif(array[int] of var int: x, var int: y, var int: c,
                     var bool: b);
%-----------------------------------------------------------------------------%

