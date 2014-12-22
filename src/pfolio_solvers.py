'''
This module contains one class for each installed solver of the portfolio.
Each class is an object of class Solver and might be defined manually, but it is 
however strongly suggested to first generate it automatically by using the
make_pfolio.py script in SUNNY_HOME/solvers. Then, once the file is created, it 
is possible to customize each object. Note that running make_pfolio.py script 
will replace the current file.
'''

from solver import Solver

g12lazyfd = Solver()
g12lazyfd.name = 'g12lazyfd'
g12lazyfd.mznlib = '/home/roberto/sunny-cp/solvers/g12lazyfd/mzn-lib'
g12lazyfd.fzn_exec = '/home/roberto/sunny-cp/solvers/g12lazyfd/fzn-exec'
g12lazyfd.lt_constraint = 'constraint int_lt(llt, rlt)'
g12lazyfd.gt_constraint = 'constraint int_lt(rgt, lgt)'

g12fd = Solver()
g12fd.name = 'g12fd'
g12fd.mznlib = '/home/roberto/sunny-cp/solvers/g12fd/mzn-lib'
g12fd.fzn_exec = '/home/roberto/sunny-cp/solvers/g12fd/fzn-exec'
g12fd.lt_constraint = 'constraint int_lt(llt, rlt)'
g12fd.gt_constraint = 'constraint int_lt(rgt, lgt)'

chuffed = Solver()
chuffed.name = 'chuffed'
chuffed.mznlib = '/home/roberto/sunny-cp/solvers/chuffed/mzn-lib'
chuffed.fzn_exec = '/home/roberto/sunny-cp/solvers/chuffed/fzn-exec'
chuffed.lt_constraint = 'constraint int_lt(llt, rlt)'
chuffed.gt_constraint = 'constraint int_lt(rgt, lgt)'

g12cbc = Solver()
g12cbc.name = 'g12cbc'
g12cbc.mznlib = '/home/roberto/sunny-cp/solvers/g12cbc/mzn-lib'
g12cbc.fzn_exec = '/home/roberto/sunny-cp/solvers/g12cbc/fzn-exec'
g12cbc.lt_constraint = 'constraint int_lt(llt, rlt)'
g12cbc.gt_constraint = 'constraint int_lt(rgt, lgt)'

g12cpx = Solver()
g12cpx.name = 'g12cpx'
g12cpx.mznlib = '/home/roberto/sunny-cp/solvers/g12cpx/mzn-lib'
g12cpx.fzn_exec = '/home/roberto/sunny-cp/solvers/g12cpx/fzn-exec'
g12cpx.lt_constraint = 'constraint int_lin_le([1, -1], [llt, rlt], -1)'
g12cpx.gt_constraint = 'constraint int_lin_le([1, -1], [rgt, lgt], -1)'

g12gurobi = Solver()
g12gurobi.name = 'g12gurobi'
g12gurobi.mznlib = '/home/roberto/sunny-cp/solvers/g12gurobi/mzn-lib'
g12gurobi.fzn_exec = '/home/roberto/sunny-cp/solvers/g12gurobi/fzn-exec'
g12gurobi.lt_constraint = 'constraint int_lt(llt, rlt)'
g12gurobi.gt_constraint = 'constraint int_lt(rgt, lgt)'

minisatid = Solver()
minisatid.name = 'minisatid'
minisatid.mznlib = '/home/roberto/sunny-cp/solvers/minisatid/mzn-lib'
minisatid.fzn_exec = '/home/roberto/sunny-cp/solvers/minisatid/fzn-exec'
minisatid.lt_constraint = 'constraint int_lt(llt, rlt)'
minisatid.gt_constraint = 'constraint int_lt(rgt, lgt)'

