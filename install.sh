#!/bin/sh
# Minimal installation file for sunny-cp.

echo -n 'Testing Python installation...'
which python 1>/dev/null
ret=$?
if 
  [ $ret -ne 0 ]
then
  echo 'Error! Python not properly installed'
  echo 'Aborted.'
  exit $ret
fi
echo 'OK!'

echo -n 'Testing MiniZinc installation...'
which minizinc 1>/dev/null
ret=$?
if 
  [ $ret -ne 0 ]
then
  echo 'Error! MiniZinc not properly installed'
  echo 'Aborted.'
  exit $ret
fi
echo 'OK!'

echo -n 'Testing mzn2feat installation...'
which minizinc 1>/dev/null
ret=$?
if 
  [ $ret -ne 0 ]
then
  echo 'Error! mzn2feat not properly installed'
  echo 'Please decompress mzn2feat-1.0.tar.bz2 and install the mzn2feat tool.'
  echo 'Aborted.'
  exit $ret
fi
echo 'OK!'

echo 'Checking solvers installation...'
python solvers/make_pfolio.py

echo 'Compiling python sources...'
for f in `find . -name *.py` ./bin/sunny-cp
do
  echo -n 'Compiling '$f'...'
  python $f --help 1>/dev/null
  ret=$?
  if 
    [ $ret -ne 0 ]
  then
    echo 'Error! '$f' not successfully compiled!'
    echo 'Aborted.'
    exit $ret
  fi
  echo 'OK!'
done

echo "\n--- Everything went well!\n"
echo -n "To complete sunny-cp installation just add/modify the "
echo "environment variables SUNNY_HOME and PATH:\n"
echo "  SUNNY_HOME must point to: "$PWD
echo "\n  PATH must be extended to include: "$PWD"/bin\n"