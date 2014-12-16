'''
Module for creating a Solver subclass for each constituent solver of the 
portfolio, according to the input/output conventions specified in the README 
file of this folder.
'''

import os
import sys
from string import replace
from subprocess import Popen, PIPE

pfolio_path = os.environ['SUNNY_HOME'] + '/src/pfolio_solvers.py'
pfolio_file = open(pfolio_path, 'w')

preamble = "'''\nThis module contains one class for each installed solver of " \
  "the portfolio.\nEach class is an object of class Solver and might be" \
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
  cmd = 'mzn2fzn -I ' + solvers_path + solver + '/mzn-lib ' + solvers_path + \
        'lt_gt.mzn --output-to-stdout --no-output-ozn'
  proc = Popen(cmd.split(), stdout = PIPE, stderr = PIPE)
  out, err = proc.communicate()
  if proc.returncode != 0:
    print err
    print 'Error! Solver',solver,'not installed'
    continue
    #pfolio_file.close()
    #os.remove(pfolio_path)
    #sys.exit(proc.returncode)
  for line in out.split(';\n'):
    if 'constraint ' in line:
      if 'llt' in line:
        pfolio_file.write(solver + ".lt_constraint = '" + line + "'\n")
      elif 'lgt' in line:
        pfolio_file.write(solver + ".gt_constraint = '" + line + "'\n")
  pfolio_file.write('\n')
