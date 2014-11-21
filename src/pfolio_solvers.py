'''
This module contains one class for each installed solver of the portfolio.
Each class must be a subclass of Solver class and might be defined manually, but 
it is however strongly suggested to first generate it automatically by using the
make_pfolio.py script in SUNNY_HOME/solvers. Then, once the file is created, it 
is possible to specialize each class. Note that running make_pfolio.py script 
will replace the current file.
'''

from solver import Solver

class g12lazyfd(Solver):
  name = 'g12lazyfd'
  mznlib = '/home/roberto/sunny-cp/solvers/g12lazyfd/mzn-lib'
  fzn_exec = '/home/roberto/sunny-cp/solvers/g12lazyfd/fzn-exec'
  lt_constraint = 'constraint int_lt(llt, rlt)'
  gt_constraint = 'constraint int_lt(rgt, lgt)'

class g12fd(Solver):
  name = 'g12fd'
  mznlib = '/home/roberto/sunny-cp/solvers/g12fd/mzn-lib'
  fzn_exec = '/home/roberto/sunny-cp/solvers/g12fd/fzn-exec'
  lt_constraint = 'constraint int_lt(llt, rlt)'
  gt_constraint = 'constraint int_lt(rgt, lgt)'

class chuffed(Solver):
  name = 'chuffed'
  mznlib = '/home/roberto/sunny-cp/solvers/chuffed/mzn-lib'
  fzn_exec = '/home/roberto/sunny-cp/solvers/chuffed/fzn-exec'
  lt_constraint = 'constraint int_lt(llt, rlt)'
  gt_constraint = 'constraint int_lt(rgt, lgt)'

class g12cbc(Solver):
  name = 'g12cbc'
  mznlib = '/home/roberto/sunny-cp/solvers/g12cbc/mzn-lib'
  fzn_exec = '/home/roberto/sunny-cp/solvers/g12cbc/fzn-exec'
  lt_constraint = 'constraint int_lt(llt, rlt)'
  gt_constraint = 'constraint int_lt(rgt, lgt)'

class g12cpx(Solver):
  name = 'g12cpx'
  mznlib = '/home/roberto/sunny-cp/solvers/g12cpx/mzn-lib'
  fzn_exec = '/home/roberto/sunny-cp/solvers/g12cpx/fzn-exec'
  lt_constraint = 'constraint int_lin_le([1, -1], [llt, rlt], -1)'
  gt_constraint = 'constraint int_lin_le([1, -1], [rgt, lgt], -1)'

