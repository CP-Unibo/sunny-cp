#!/bin/bash

# Script that run the list of problems to test

source $SUNNY_HOME/test/test_env.sh

# exit after SIGINT
trap "exit" INT

MODEL=$1
DATA=$2

MODEL_NAME=`basename $MODEL`
MODEL_NAME=${MODEL_NAME%.mzn}
DATA_NAME=`basename $DATA`
DATA_NAME=${DATA_NAME%.dzn}

ERR="$RESULTS_DIR/$MODEL_NAME-$$.err"
OUT="$RESULTS_DIR/$MODEL_NAME-$$.out"
TMP_FZN="$RESULTS_DIR/$MODEL_NAME-$$.fzn"
TMP_MODEL="$RESULTS_DIR/$MODEL_NAME-$$.mzn"

# if [[ $DATA = "NODATA" ]];
# then
#         DATA=""
# else
#         cp $DATA $TMP_DIR/
#         DATA="--data $DATA"
# fi

CMD="$SUNNY_HOME/bin/sunny-cp -T $TIMEOUT $SOLVER $MODEL $DATA"
echo "`date`: Running $CMD"
ABORTED=""
START_TIME=`date '+%s%N'`

EXTENDED_TIMEOUT=$(($TIMEOUT + 10))

# run sunny-cp with maximum TIMEOUT + 10 seconds
timeout $EXTENDED_TIMEOUT $CMD >$OUT 2>$ERR
ret=$?
if
  [ $ret -eq 124 ]
then
  echo "ERROR: the command '$CMD' took more than $TIMEOUT seconds" 1>&2
  if [ -f "$OUT" ]
  then
      rm $OUT
  fi

  if [ -f "$ERR" ]
  then
      rm $ERR
  fi
elif
  [ $ret -ne 0 ]
then
  echo "ERROR: the command '$CMD' returned with error $ret" 1>&2
  echo "ERROR: please check the output log $OUT and the error log $ERR" 1>&2
else

  END_TIME=`date '+%s%N'`
  RUN_TIME=$((($END_TIME - $START_TIME) / 1000000))
  echo "Run time: $RUN_TIME. Testing" 

  # Check if the output is consistent

  if grep -Fq "=====UNSAT" $OUT
  then
    if grep -Fq "$MODEL_NAME $DATA_NAME" $UNSAT_LIST
    then
	echo "Test Ok"
    else 
	echo "ERROR: Output '$CMD' not consistent: instance not listed as UNSAT" 1>&2
    fi
  else

    if grep -Fq "==========" $OUT
    then
	BEST_SOL=`grep  "$MODEL_NAME $DATA_NAME" $OPT_LIST`
	if [ -n "$BEST_SOL" ]
	then
	  PROVEN_OPT=`grep -F "o__b__j__v__a__r" $OUT | tail -n 1 | awk -F" " '{print $4}'`
	  TYPE_SOL=`echo $BEST_SOL | awk -F" " '{print $1}'`
	  BEST_SOL=`echo $BEST_SOL | awk -F" " '{print $4}'`
	  if [ "$PROVEN_OPT" -eq "$PROVEN_OPT" ] 2> /dev/null; then
	    if [ "$BEST_SOL" -eq "$BEST_SOL" ] 2> /dev/null; then
	      if [ "$TYPE_SOL" = "MIN" ] && [ "$PROVEN_OPT" -lt "$BEST_SOL" ]
	      then
		echo "WARNING: '$CMD' found solution with objective $PROVEN_OPT, but best know solution $BEST_SOL" 1>&2
	      elif
		[ "$TYPE_SOL" = "MAX" ] && [ "$PROVEN_OPT" -gt "$BEST_SOL" ]
	      then
		echo "WARNING: '$CMD' found solution with objective $PROVEN_OPT, but best know solution $BEST_SOL" 1>&2
	      fi
	    else
	      echo "WARNING: when parsing the known best solution file, found non integer value $BEST_SOL for instance $MODEL_NAME $DATA_NAME"  1>&2
	    fi
	  else
	    echo "WARNING: '$CMD' found objective value that is not a number. Expected integer, found $PROVEN_OPT"  1>&2
	  fi
	fi
    fi
    NSOL=`grep -c "\-\-\-\-\-\-\-\-\-\-" $OUT`
    if [ $NSOL -eq 0 ]
    then
	  echo "No solutions found"
    else
	  cp $MODEL $TMP_MODEL
	  solns2dzn -l $OUT >> $TMP_MODEL
	  curdir=$(pwd)
	  cd $RESULTS_DIR
	  # sometimes minizinc gives error while separating the computation is ok 
	  # minizinc -G g12
	  mzn2fzn $TMP_MODEL $DATA -o $TMP_FZN --no-output-ozn 2> /dev/null
	  ret=$?
	  if [ $ret -ne 0 ]
	  then
	    echo "WARNING: '$CMD' + output is not a valid minizinc model. Mizinc conversion returned with error $ret. Ignoring checking correctness solution"  1>&2
	  else	  
	    if flatzinc $TMP_FZN | grep -q "\-\-\-\-\-\-\-\-\-" 2> /dev/null
	    then
		echo "Test Ok"
	    else
		echo "ERROR: Output '$CMD' not consistent: invalid output or incorrect solution detected" 1>&2
	    fi
	  fi
	  cd $curdir
    fi
  fi

  if [ -f "$OUT" ]; then
      rm $OUT
  fi

  if [ -f "$ERR" ]; then
      rm $ERR
  fi
    
  if [ -f "$TMP_MODEL" ]; then
      rm $TMP_MODEL
  fi
  
  if [ -f "$TMP_FZNL" ]; then
      rm $TMP_FZN
  fi

fi

