%-----------------------------------------------------------------------------%
% FlatZinc built-in redefinitions for XCSP
%-----------------------------------------------------------------------------%

include "table.mzn";

%-----------------------------------------------------------------------------%
% Set membership
%
% Interval set: turned into two inequalities
% General case: turned into a 1D table
%
% For example, given
%
%   var 1..4: x;
%
% then
%
%   constraint x in {2,4};
%
% becomes
%
%   constraint table([x], [2, 4]);

predicate set_in(var int: x, set of int: s) =
    if s = min(s)..max(s) then
        min(s) <= x /\ x <= max(s)
    else
        table([x], array2d(1..card(s), 1..1, set2array(s)))
    endif;


%-----------------------------------------------------------------------------%
% Reified set membership
%
% Interval set: turned into two reified inequalities
% General case: turned into a 2D table
%
%
% For example, given
%
%   var 1..4: x;
%   var bool: b;
%
% then
%
%   constraint x in {2,4} <-> b;
%
% becomes
%
%   constraint table([x, bool2int(b)],
%                  [| 1, 0 |
%                     2, 1 |
%                     3, 0 |
%                     4, 1 |]);

predicate set_in_reif(var int: x, set of int: s, var bool: b) =
    if s = min(s)..max(s) then
        (min(s) <= x /\ x <= max(s)) <-> b
    else
        table([x,bool2int(b)], array2d(1..card(dom(x)), 1..2,
            [ if p = 0 then e else bool2int(e in s) endif
              | e in dom(x), p in 0..1 ] ))
    endif;

%-----------------------------------------------------------------------------%
%-----------------------------------------------------------------------------%
