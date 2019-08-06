#!/bin/bash
#----------------------------------------------------------#
# Script for running SUNNY-CP in the challenge with only freely available solvers
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
# -p 8 -- should be given in input. We assume p = 8
sunny-cp \
 --cop-a -f -T 1200 \
 -P picat,choco,ortools,gecode,jacop,yuck \
 -s picat,10,choco,10,ortools,10,gecode,10,jacop,10,yuck,10 \
 $PARAM | solns2out $TMP.ozn
 #--check-solvers mistral,gecode,opturion,gecode "$@"
rm ${TMP}