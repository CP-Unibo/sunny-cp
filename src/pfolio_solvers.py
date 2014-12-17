'''
This module contains one class for each installed solver of the portfolio.
Each class is an object of class Solver and might be defined manually, but it is 
however strongly suggested to first generate it automatically by using the
make_pfolio.py script in SUNNY_HOME/solvers. Then, once the file is created, it 
is possible to customize each object. Note that running make_pfolio.py script 
will replace the current file.
'''

from solver import Solver

g12cbc = Solver()
g12cbc.name = 'g12cbc'
g12cbc.mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12cbc/mzn-lib'
g12cbc.fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12cbc/fzn-exec'
g12cbc.lt_constraint = 'constraint int_lt(llt, rlt)'
g12cbc.gt_constraint = 'constraint int_lt(rgt, lgt)'

g12lazyfd = Solver()
g12lazyfd.name = 'g12lazyfd'
g12lazyfd.mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12lazyfd/mzn-lib'
g12lazyfd.fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12lazyfd/fzn-exec'
g12lazyfd.lt_constraint = 'constraint int_lt(llt, rlt)'
g12lazyfd.gt_constraint = 'constraint int_lt(rgt, lgt)'

choco = Solver()
choco.name = 'choco'
choco.mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/choco/mzn-lib'
choco.fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/choco/fzn-exec'
choco.lt_constraint = 'constraint int_lt(llt, rlt)'
choco.gt_constraint = 'constraint int_lt(rgt, lgt)'

g12gurobi = Solver()
g12gurobi.name = 'g12gurobi'
g12gurobi.mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12gurobi/mzn-lib'
g12gurobi.fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12gurobi/fzn-exec'
g12gurobi.lt_constraint = 'constraint int_lt(llt, rlt)'
g12gurobi.gt_constraint = 'constraint int_lt(rgt, lgt)'

g12fd = Solver()
g12fd.name = 'g12fd'
g12fd.mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12fd/mzn-lib'
g12fd.fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12fd/fzn-exec'
g12fd.lt_constraint = 'constraint int_lt(llt, rlt)'
g12fd.gt_constraint = 'constraint int_lt(rgt, lgt)'

gecode = Solver()
gecode.name = 'gecode'
gecode.mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/gecode/mzn-lib'
gecode.fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/gecode/fzn-exec'
gecode.lt_constraint = 'constraint int_lt(llt, rlt)'
gecode.gt_constraint = 'constraint int_lt(rgt, lgt)'

minisatid = Solver()
minisatid.name = 'minisatid'
minisatid.mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/minisatid/mzn-lib'
minisatid.fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/minisatid/fzn-exec'
minisatid.lt_constraint = 'constraint int_lt(llt, rlt)'
minisatid.gt_constraint = 'constraint int_lt(rgt, lgt)'

chuffed = Solver()
chuffed.name = 'chuffed'
chuffed.mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/chuffed/mzn-lib'
chuffed.fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/chuffed/fzn-exec'
chuffed.lt_constraint = 'constraint int_lt(llt, rlt)'
chuffed.gt_constraint = 'constraint int_lt(rgt, lgt)'

g12cpx = Solver()
g12cpx.name = 'g12cpx'
g12cpx.mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12cpx/mzn-lib'
g12cpx.fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12cpx/fzn-exec'
g12cpx.lt_constraint = 'constraint int_lin_le([1, -1], [llt, rlt], -1)'
g12cpx.gt_constraint = 'constraint int_lin_le([1, -1], [rgt, lgt], -1)'

izplus = Solver()
izplus.name = 'izplus'
izplus.mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/izplus/mzn-lib'
izplus.fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/izplus/fzn-exec'
izplus.lt_constraint = 'constraint int_lt(llt, rlt)'
izplus.gt_constraint = 'constraint int_lt(rgt, lgt)'

haifacsp = Solver()
haifacsp.name = 'haifacsp'
haifacsp.mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/haifacsp/mzn-lib'
haifacsp.fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/haifacsp/fzn-exec'
haifacsp.lt_constraint = 'constraint int_lt(llt, rlt)'
haifacsp.gt_constraint = 'constraint int_lt(rgt, lgt)'

ortools = Solver()
ortools.name = 'ortools'
ortools.mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/ortools/mzn-lib'
ortools.fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/ortools/fzn-exec'
ortools.lt_constraint = 'constraint int_lt(llt, rlt)'
ortools.gt_constraint = 'constraint int_lt(rgt, lgt)'

