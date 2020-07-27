#!/bin/bash
#----------------------------------------------------------#
# Script for running eligible SUNNY-CP
#------------------------------------------#

TMP=$(mktemp)
PARAM=""
MZN=""
DZN=""
while (( "$#" ))
do
    case $1 in
    -p)
        shift
        PARAM="$PARAM -p $1"
        ;;
    -a)
        # ignore -a. Set by default if a problem is an optimization one
        ;;
    -f)
        # ignore -f. Set by default
        ;;
    -G)
        # ignore -G option
        ;;
    *.mzn)
        MZN=$1
        PARAM="$PARAM $1"
        ;;
    *.dzn)
        DZN=$1
        PARAM="$PARAM $1"
        ;;
    *)
        PARAM="$PARAM $1"
        ;;
    esac
    shift
done

# generate ozn file to later parse output
minizinc --compile -G gecode $MZN $DZN -O $TMP.ozn --fzn $TMP.fzn

# run sunny-cp
sunny-cp \
 -p 8 --cop-a -f -T 1200 \
 -P picat,izplus,sicstus,ortools,gecode,cplex,jacop,yuck \
 -s picat,10,izplus,10,sicstus,10,ortools,10,gecode,10,jacop,10,yuck,10,cplex,10 \
# --check-solvers haifacsp,gecode \
 $PARAM | solns2out $TMP.ozn

rm ${TMP}
