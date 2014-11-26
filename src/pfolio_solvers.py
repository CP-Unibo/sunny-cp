'''
This module contains one class for each installed solver of the portfolio.
Each class must be a subclass of Solver class and might be defined manually, but 
it is however strongly suggested to first generate it automatically by using the
make_pfolio.py script in SUNNY_HOME/solvers. Then, once the file is created, it 
is possible to specialize each class. Note that running make_pfolio.py script 
will replace the current file.
'''

from solver import Solver

class g12cbc(Solver):
  name = 'g12cbc'
  mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12cbc/mzn-lib'
  fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12cbc/fzn-exec'
  lt_constraint = 'constraint int_lt(llt, rlt)'
  gt_constraint = 'constraint int_lt(rgt, lgt)'

class g12lazyfd(Solver):
  name = 'g12lazyfd'
  mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12lazyfd/mzn-lib'
  fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12lazyfd/fzn-exec'
  lt_constraint = 'constraint int_lt(llt, rlt)'
  gt_constraint = 'constraint int_lt(rgt, lgt)'

class choco(Solver):
  name = 'choco'
  mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/choco/mzn-lib'
  fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/choco/fzn-exec'
  lt_constraint = 'constraint int_lt(llt, rlt)'
  gt_constraint = 'constraint int_lt(rgt, lgt)'

class g12gurobi(Solver):
  name = 'g12gurobi'
  mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12gurobi/mzn-lib'
  fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12gurobi/fzn-exec'
  lt_constraint = 'constraint int_lt(llt, rlt)'
  gt_constraint = 'constraint int_lt(rgt, lgt)'

class g12fd(Solver):
  name = 'g12fd'
  mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12fd/mzn-lib'
  fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12fd/fzn-exec'
  lt_constraint = 'constraint int_lt(llt, rlt)'
  gt_constraint = 'constraint int_lt(rgt, lgt)'

class gecode(Solver):
  name = 'gecode'
  mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/gecode/mzn-lib'
  fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/gecode/fzn-exec'
  lt_constraint = 'constraint int_lt(llt, rlt)'
  gt_constraint = 'constraint int_lt(rgt, lgt)'

class minisatid(Solver):
  name = 'minisatid'
  mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/minisatid/mzn-lib'
  fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/minisatid/fzn-exec'
  lt_constraint = 'constraint int_lt(llt, rlt)'
  gt_constraint = 'constraint int_lt(rgt, lgt)'

class chuffed(Solver):
  name = 'chuffed'
  mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/chuffed/mzn-lib'
  fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/chuffed/fzn-exec'
  lt_constraint = 'constraint int_lt(llt, rlt)'
  gt_constraint = 'constraint int_lt(rgt, lgt)'

class g12cpx(Solver):
  name = 'g12cpx'
  mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12cpx/mzn-lib'
  fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12cpx/fzn-exec'
  lt_constraint = 'constraint int_lin_le([1, -1], [llt, rlt], -1)'
  gt_constraint = 'constraint int_lin_le([1, -1], [rgt, lgt], -1)'

class izplus(Solver):
  name = 'izplus'
  mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/izplus/mzn-lib'
  fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/izplus/fzn-exec'
  lt_constraint = 'constraint int_lt(llt, rlt)'
  gt_constraint = 'constraint int_lt(rgt, lgt)'

class haifacsp(Solver):
  name = 'haifacsp'
  mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/haifacsp/mzn-lib'
  fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/haifacsp/fzn-exec'
  lt_constraint = 'constraint int_lt(llt, rlt)'
  gt_constraint = 'constraint int_lt(rgt, lgt)'

class ortools(Solver):
  name = 'ortools'
  mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/ortools/mzn-lib'
  fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/ortools/fzn-exec'
  lt_constraint = 'constraint int_lt(llt, rlt)'
  gt_constraint = 'constraint int_lt(rgt, lgt)'

