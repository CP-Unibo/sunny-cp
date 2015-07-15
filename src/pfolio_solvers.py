'''
This module contains an object of class Solver for each installed solver of the 
portfolio. Each object of class Solver might be defined manually, but it is 
however strongly suggested to first generate it automatically by using the
make_pfolio.py script in solvers folder. Then, once the file is created, it 
is possible to customize each object. Note that running make_pfolio.py script 
will replace the current file.
'''

from solver import Solver

g12fd_free = Solver()
g12fd_free.name = 'g12fd_free'
g12fd_free.mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12fd_free/mzn-lib'
g12fd_free.fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12fd_free/fzn-exec'
g12fd_free.constraint = 'constraint int_lin_le([1,-1],[LHS,RHS],-1)'
g12fd_free.all_opt = '-a'
g12fd_free.free_opt  = '--ignore-user-search'

g12cbc = Solver()
g12cbc.name = 'g12cbc'
g12cbc.mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12cbc/mzn-lib'
g12cbc.fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12cbc/fzn-exec'
g12cbc.constraint = 'constraint int_lin_le([1,-1],[LHS,RHS],-1)'
g12cbc.all_opt = '-a'
g12cbc.free_opt  = '--ignore-user-search'

g12lazyfd = Solver()
g12lazyfd.name = 'g12lazyfd'
g12lazyfd.mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12lazyfd/mzn-lib'
g12lazyfd.fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12lazyfd/fzn-exec'
g12lazyfd.constraint = 'constraint int_lin_le([1,-1],[LHS,RHS],-1)'
g12lazyfd.all_opt = '-a'
g12lazyfd.free_opt  = '--ignore-user-search'

g12cpx_free = Solver()
g12cpx_free.name = 'g12cpx_free'
g12cpx_free.mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12cpx_free/mzn-lib'
g12cpx_free.fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12cpx_free/fzn-exec'
g12cpx_free.constraint = 'constraint int_lin_le([1,-1],[LHS,RHS],-1)'
g12cpx_free.all_opt = '-a'
g12cpx_free.free_opt = '-f'

choco = Solver()
choco.name = 'choco'
choco.mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/choco/mzn-lib'
choco.fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/choco/fzn-exec'
choco.constraint = 'constraint int_lin_le([1,-1],[LHS,RHS],-1)'
choco.all_opt = '-a'
choco.free_opt = '-f'

g12gurobi = Solver()
g12gurobi.name = 'g12gurobi'
g12gurobi.mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12gurobi/mzn-lib'
g12gurobi.fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12gurobi/fzn-exec'
g12gurobi.constraint = 'constraint int_lin_le([1,-1],[LHS,RHS],-1)'
g12gurobi.all_opt = '-a'
g12gurobi.free_opt  = '--ignore-user-search'

g12fd = Solver()
g12fd.name = 'g12fd'
g12fd.mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12fd/mzn-lib'
g12fd.fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12fd/fzn-exec'
g12fd.constraint = 'constraint int_lin_le([1,-1],[LHS,RHS],-1)'
g12fd.all_opt = '-a'
g12fd.free_opt  = '--ignore-user-search'

g12lazyfd_free = Solver()
g12lazyfd_free.name = 'g12lazyfd_free'
g12lazyfd_free.mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12lazyfd_free/mzn-lib'
g12lazyfd_free.fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12lazyfd_free/fzn-exec'
g12lazyfd_free.constraint = 'constraint int_lin_le([1,-1],[LHS,RHS],-1)'
g12lazyfd_free.all_opt = '-a'
g12lazyfd_free.free_opt  = '--ignore-user-search'

gecode = Solver()
gecode.name = 'gecode'
gecode.mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/gecode/mzn-lib'
gecode.fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/gecode/fzn-exec'
gecode.constraint = 'constraint int_lin_le([1,-1],[LHS,RHS],-1)'
gecode.all_opt = '-a'
gecode.free_opt = '--free'


minisatid = Solver()
minisatid.name = 'minisatid'
minisatid.mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/minisatid/mzn-lib'
minisatid.fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/minisatid/fzn-exec'
minisatid.constraint = 'constraint int_lin_le([1,-1],[LHS,RHS],-1)'
minisatid.all_opt = '-a'
minisatid.free_opt = ''


izplus_free = Solver()
izplus_free.name = 'izplus_free'
izplus_free.mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/izplus_free/mzn-lib'
izplus_free.fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/izplus_free/fzn-exec'
izplus_free.constraint = 'constraint int_lin_le([1,-1],[LHS,RHS],-1)'
izplus_free.all_opt = '-a'
izplus_free.free_opt = '-f'

gecode_free = Solver()
gecode_free.name = 'gecode_free'
gecode_free.mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/gecode_free/mzn-lib'
gecode_free.fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/gecode_free/fzn-exec'
gecode_free.constraint = 'constraint int_lin_le([1,-1],[LHS,RHS],-1)'
gecode_free.all_opt = '-a'
gecode_free.free_opt = '--free'


chuffed = Solver()
chuffed.name = 'chuffed'
chuffed.mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/chuffed/mzn-lib'
chuffed.fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/chuffed/fzn-exec'
chuffed.constraint = 'constraint int_lin_le([1,-1],[LHS,RHS],-1)'
chuffed.all_opt = '-a'
chuffed.free_opt = '-f'

ortools_free = Solver()
ortools_free.name = 'ortools_free'
ortools_free.mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/ortools_free/mzn-lib'
ortools_free.fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/ortools_free/fzn-exec'
ortools_free.constraint = 'constraint int_lin_le([1,-1],[LHS,RHS],-1)'
ortools_free.all_opt = '-a'
ortools_free.free_opt = '-free'


chuffed_free = Solver()
chuffed_free.name = 'chuffed_free'
chuffed_free.mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/chuffed_free/mzn-lib'
chuffed_free.fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/chuffed_free/fzn-exec'
chuffed_free.constraint = 'constraint int_lin_le([1,-1],[LHS,RHS],-1)'
chuffed_free.all_opt = '-a'
chuffed_free.free_opt = '-f'

choco_free = Solver()
choco_free.name = 'choco_free'
choco_free.mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/choco_free/mzn-lib'
choco_free.fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/choco_free/fzn-exec'
choco_free.constraint = 'constraint int_lin_le([1,-1],[LHS,RHS],-1)'
choco_free.all_opt = '-a'
choco_free.free_opt = '-f'

g12cpx = Solver()
g12cpx.name = 'g12cpx'
g12cpx.mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12cpx/mzn-lib'
g12cpx.fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/g12cpx/fzn-exec'
g12cpx.constraint = 'constraint int_lin_le([1,-1],[LHS,RHS],-1)'
g12cpx.all_opt = '-a'
g12cpx.free_opt = '-f'

izplus = Solver()
izplus.name = 'izplus'
izplus.mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/izplus/mzn-lib'
izplus.fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/izplus/fzn-exec'
izplus.constraint = 'constraint int_lin_le([1,-1],[LHS,RHS],-1)'
izplus.all_opt = '-a'
izplus.free_opt = '-f'

haifacsp = Solver()
haifacsp.name = 'haifacsp'
haifacsp.mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/haifacsp/mzn-lib'
haifacsp.fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/haifacsp/fzn-exec'
haifacsp.constraint = 'constraint int_lin_le([1,-1],[LHS,RHS],-1)'
haifacsp.all_opt = ''
haifacsp.free_opt = ''


ortools = Solver()
ortools.name = 'ortools'
ortools.mznlib = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/ortools/mzn-lib'
ortools.fzn_exec = '/import/atp-linhome/home/1/ramadini/sunny-cp/solvers/ortools/fzn-exec'
ortools.constraint = 'constraint int_lin_le([1,-1],[LHS,RHS],-1)'
ortools.all_opt = '-a'
ortools.free_opt = '-free'


