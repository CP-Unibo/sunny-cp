'''
Module for creating a Solver object for each constituent solver of the 
portfolio by automatically generating the SUNNY_HOME/src/pfolio_solvers.py file,
according to the conventions specified in the README file of this folder.
'''

import os
import sys
import psutil
from subprocess import PIPE

pfolio_path = os.environ['SUNNY_HOME'] + '/src/pfolio_solvers.py'
pfolio_file = open(pfolio_path, 'w')

preamble = "'''\nThis module contains an object of class Solver for each " \
  "installed solver of the \nportfolio. Each object of class Solver might be" \
  " defined manually, but it is \nhowever strongly suggested to first generate"\
  " it automatically by using the\nmake_pfolio.py script in SUNNY_HOME/solvers"\
  ". Then, once the file is created, it \nis possible to customize each object"\
  ". Note that running make_pfolio.py script \nwill replace the current file." \
  "\n'''\n\nfrom solver import Solver\n\n"
pfolio_file.write(preamble)

solvers_path = os.environ['SUNNY_HOME'] + '/solvers/'
solvers = os.walk(solvers_path).next()[1]
for solver in solvers:
  print 'Adding solver',solver
  pfolio_file.write(solver + ' = Solver()\n')
  pfolio_file.write(solver + ".name = '" + solver + "'\n")
  pfolio_file.write(
    solver + ".mznlib = '" + solvers_path + solver + "/mzn-lib'\n"
  )
  pfolio_file.write(
    solver + ".fzn_exec = '" + solvers_path + solver + "/fzn-exec'\n"
  )
  cmd = 'mzn2fzn -I ' + solvers_path + solver + '/mzn-lib ' + solvers_path \
      + 'constraint.mzn --output-to-stdout --no-output-ozn'
  proc = psutil.Popen(cmd.split(), stdout = PIPE, stderr = PIPE)
  out, err = proc.communicate()
  if proc.returncode != 0:
    print err
    print 'Error! Solver',solver,'not installed'
    continue
  for line in out.split(';\n'):
    intro = 'X_INTRODUCED_0 = '
    idx = line.find(intro)
    if idx >= 0:
      val = line[idx + len(intro):]
      continue
    if 'constraint' in line:
      line = line.replace('X_INTRODUCED_0', val)
      constraint = solver + ".constraint = '" + line + "'\n"
      pfolio_file.write(solver + ".constraint = '" + line + "'\n")
      break
  opts = open(solvers_path + solver + '/opts', 'r')
  for line in opts:
    pfolio_file.write(solver + '.' + line)
  pfolio_file.write('\n\n')
