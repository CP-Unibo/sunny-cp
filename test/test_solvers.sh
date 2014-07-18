#!/bin/bash

# Script that test the installation of the solvers

# dotlockfile -r 100 $LOCKFILE

FZN="/tmp/$$.fzn"
OZN="/tmp/$$.ozn"
OUT="/tmp/$$.out"

CP_MZN_PATH="$SUNNY_HOME/benchmarks/mario/mario.mzn"
CP_DZN_PATH="$SUNNY_HOME/benchmarks/mario/mario_easy_2.dzn"

# CP_MZN_PATH="$SUNNY_HOME/benchmarks/black-hole/black-hole.mzn"
# CP_DZN_PATH="$SUNNY_HOME/benchmarks/black-hole/6.dzn"

cd $SUNNY_HOME/solvers

# exit after SIGINT
trap "exit" INT

for s in `find . -maxdepth 1 -type d`
do
  if [ -f "$s/fzn-exec" ]; then
    solver=`basename $s`
    echo "################################"
    echo "Found solver $solver"
    
    SOLVER_DIR="$SUNNY_HOME/solvers/$solver"    
    MZNLIB=""
    STDLIB=""
    
    if [ -d "$SOLVER_DIR/mzn-lib" ]; then
      MZNLIB="-I $SOLVER_DIR/mzn-lib"
      echo "mznlib global definiton detected"
    fi
    
    if [ -d "$SOLVER_DIR/std-lib" ]; then
      STDLIB="-I $SOLVER_DIR/std-lib"
      echo "stdlib global definiton detected"
    fi
    
    echo "Compiling the MiniZinc problem into FlatZinc"
    
    mzn2fzn $MZNLIB $STDLIB $CP_MZN_PATH $CP_DZN_PATH -o $FZN --output-ozn-to-file $OZN &> /dev/null
    ret=$?
    if 
      [ $ret -ne 0 ]
    then
      echo "MiniZinc model for $solver not converted (return error $ret)" 1>&2
    else
      echo "Running the solver"
      $solver/fzn-exec -a $FZN > $OUT 2> /dev/null
      ret=$?
      if 
	[ $ret -ne 0 ]
      then
	echo "Error in launching $solver (return error $ret)" 1>&2
      else
	echo "Parsing the output"
	solns2out $OZN $OUT &> /dev/null
	ret=$?
	if 
	  [ $ret -ne 0 ]
	then
	  echo "Error in parsing $solver output (return error $ret)" 1>&2
	else
	  echo "$solver passed the CP test"
	fi
      fi
    fi
  fi
done

if [ -f "$FZN" ]; then
  rm $FZN
fi

if [ -f "$OZN" ]; then
  rm $OZN
fi

if [ -f "$OUT" ]; then
  rm $OUT
fi
# dotlockfile -u $LOCKFILE
