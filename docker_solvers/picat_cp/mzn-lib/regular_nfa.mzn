/** @group globals.extensional
  The sequence of values in array \a x (which must all be in the range 1..\a S)
  is accepted by the NFA of \a Q states with input 1..\a S and transition
  function \a d (which maps (1..\a Q, 1..\a S) -> set of 1..\a Q)) and initial state \a q0
  (which must be in 1..\a Q) and accepting states \a F (which all must be in
  1..\a Q).
*/
predicate regular_nfa(array[int] of var int: x, int: Q, int: S,
                      array[int,int] of set of int: d, int: q0, set of int: F);
