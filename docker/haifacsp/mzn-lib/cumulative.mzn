%-----------------------------------------------------------------------------%
% Requires that a set of tasks given by start times 's', durations 'd', and
% resource requirements 'r', never require more than a global resource bound
% 'b' at any one time.
% Assumptions:
% - forall i, d[i] >= 0 and r[i] >= 0
%-----------------------------------------------------------------------------%

predicate cumulative(array[int] of var int: s,
                     array[int] of var int: d,
                     array[int] of var int: r, var int: b) =
    assert(index_set(s) == index_set(d) /\ index_set(s) == index_set(r),
        "cumulative: the 3 array arguments must have identical index sets",
        assert(lb_array(d) >= 0 /\ lb_array(r) >= 0,
            "cumulative: durations and resource usages must be non-negative",
    cumulative_decomp(s, d, r, b)));
            
% TODO: Replace with:
%	xcsp_cumulative(s, d, r, b)));
% Once hcsp supports cumulative constraint.

%-----------------------------------------------------------------------------%

% The implementation of the cumulative constraint in the XCSP "solver".
% This should not be called directly, instead the definition above should
% be used.
predicate xcsp_cumulative(array[int] of var int: s,
		     array[int] of var int: d,
		     array[int] of var int: r, var int: b);

%-----------------------------------------------------------------------------%

predicate cumulative_decomp(array[int] of var int: s,
                     array[int] of var int: d,
                     array[int] of var int: r, var int: b) =
            let { 
               set of int: tasks = 
                  {i | i in index_set(s) where ub(r[i]) > 0 /\ ub(d[i]) > 0 },
               set of int: times =
                  min([ lb(s[i]) | i in tasks ]) ..
                  max([ ub(s[i]) + ub(d[i]) | i in tasks ]) 
                } 
            in
               forall( t in times ) (
                  b >= sum( i in tasks ) (
                     bool2int( s[i] <= t /\ t < s[i] + d[i] ) * r[i]
                  )
               );
