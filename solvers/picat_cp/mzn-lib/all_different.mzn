include "all_different_int.mzn";
include "all_different_set.mzn";

/** @group globals.alldifferent
  Constrain the array of integers \a x to be all different.
*/
predicate all_different(array[int] of var int: x);

/**  @group globals.alldifferent
  Constrain the array of sets of integers \a x to be all different.
*/
predicate all_different(array[int] of var set of int: x);

% Synonyms for the above.

predicate alldifferent(array[int] of var int: x);

predicate alldifferent(array[int] of var set of int: x);

