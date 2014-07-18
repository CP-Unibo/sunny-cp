#!/bin/bash

# Script that generates the list of problems to test

source $SUNNY_HOME/test/test_env.sh

# exit after SIGINT
trap "exit" INT

for p in `ls $PROB_DIR` 
  do
    cd $PROB_DIR/$p
      MOD=`ls *.mzn`
      for i in `find . -maxdepth 1 -type f -name '*.dzn' | sort`
        do
          echo "$PROB_DIR/$p/$MOD $PROB_DIR/$p/`basename $i`"
        done
done
