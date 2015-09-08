%-----------------------------------------------------------------------------%
% A table constraint: table(x, t) represents the constraint x in t where we
% consider each row in t to be a tuple and t as a set of tuples.
%-----------------------------------------------------------------------------%

predicate table_int(array[int] of var int: x, array[int, int] of int: t) =
    assert (index_set_2of2(t) == index_set(x),
        "The second dimension of the table must equal the number of variables "
            ++ "in the first argument",
        let { int: l = min(index_set(x)),
              int: u = max(index_set(x)),
              int: lt = min(index_set_1of2(t)),
              int: ut = max(index_set_1of2(t)),
              int: size = (u-l+1)*(ut-lt+1) }
        in
        hcsp_table_int(x, array1d(1..size, t))
    );

%-----------------------------------------------------------------------------%

% The implementation of the table_int constraint in HCSP.
% This should not be called directly, instead the definition above should
% be used.
predicate hcsp_table_int(array[int] of var int: x, array[int] of var int: t);

%-----------------------------------------------------------------------------%
