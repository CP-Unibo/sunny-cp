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

psv=`python -c "import psutil ; print psutil.__version__[0]"` 2>/dev/null
if 
  [ -z $psv ]
then
  echo 'Error! psutil package not properly installed'
  echo 'Aborted.'
  exit 1
elif
  [ $psv -lt 2 ]
then
  echo 'Error! psutil package obsolete (need version >= 2.x)'
  echo 'Aborted.'
  exit 1
fi

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
    rm `find . -name *.pyc`
    exit $ret
  fi
  echo 'OK!'
done

echo "--- Everything went well!"
echo "To complete sunny-cp installation you just have to add/modify the" 
echo "environment variables SUNNY_HOME and PATH:"
echo "1. SUNNY_HOME must point to: "$PWD
echo "2. PATH must be extended to include: "$PWD"/bin"