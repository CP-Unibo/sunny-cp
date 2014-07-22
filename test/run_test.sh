#!/bin/bash

# Script that run the list of problems to test

source $SUNNY_HOME/test/test_env.sh

# exit after SIGINT
trap "exit" INT

if [ ! -d "$SUNNY_HOME/tmp" ]; then
  mkdir $SUNNY_HOME/tmp
fi

if [ ! -d "$RESULTS_DIR" ]; then
  mkdir $RESULTS_DIR
fi

while [[ -s $LISTFILE ]];
do 

        if [[ -s $LISTFILE ]];
        then
                LINE=`head -n 1 $LISTFILE`
                sed -i -e "1d" $LISTFILE
                $SUNNY_HOME/test/run_one_test.sh $LINE
        fi
done