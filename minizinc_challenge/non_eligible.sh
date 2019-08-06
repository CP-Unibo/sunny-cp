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
 #-p 8 -- should be given in input
 --cop-a -f -T 1200 \
 -P picat,izplus,choco,ortools,gecode,jacop,yuck,chuffed \
 -s picat,10,izplus,10,choco,10,ortools,10,gecode,10,jacop,10,yuck,10,chuffed,10 \
 $PARAM | solns2out $TMP.ozn
 #--check-solvers mistral,gecode,opturion,gecode "$@"
rm ${TMP}