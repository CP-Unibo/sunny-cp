'''
This module contains an object of class Solver for each installed solver of the 
portfolio. Each object of class Solver might be defined manually, but it is 
however strongly suggested to first generate it automatically by using the
make_pfolio.py script in solvers folder. Then, once the file is created, it 
is possible to customize each object. Note that running make_pfolio.py script 
will replace the current file.
'''

from solver import Solver

chuffed = Solver()
chuffed.name = 'chuffed'
chuffed.mznlib = '/home/roberto/sunny-cp/solvers/chuffed/mzn-lib'
chuffed.fzn_exec = '/home/roberto/sunny-cp/solvers/chuffed/fzn-exec'
chuffed.constraint = 'constraint int_lin_le([1,-1],[LHS,RHS],-1)'
chuffed.all_opt = '-a'
chuffed.free_opt = '-f'

g12fd = Solver()
g12fd.name = 'g12fd'
g12fd.mznlib = '/home/roberto/sunny-cp/solvers/g12fd/mzn-lib'
g12fd.fzn_exec = '/home/roberto/sunny-cp/solvers/g12fd/fzn-exec'
g12fd.constraint = 'constraint int_lin_le([1,-1],[LHS,RHS],-1)'
g12fd.all_opt = '-a'
g12fd.free_opt  = '--ignore-user-search'

minisatid = Solver()
minisatid.name = 'minisatid'
minisatid.mznlib = '/home/roberto/sunny-cp/solvers/minisatid/mzn-lib'
minisatid.fzn_exec = '/home/roberto/sunny-cp/solvers/minisatid/fzn-exec'
minisatid.constraint = 'constraint int_lin_le([1,-1],[LHS,RHS],-1)'
minisatid.all_opt = '-a'
minisatid.free_opt = ''

g12lazyfd = Solver()
g12lazyfd.name = 'g12lazyfd'
g12lazyfd.mznlib = '/home/roberto/sunny-cp/solvers/g12lazyfd/mzn-lib'
g12lazyfd.fzn_exec = '/home/roberto/sunny-cp/solvers/g12lazyfd/fzn-exec'
g12lazyfd.constraint = 'constraint int_lin_le([1,-1],[LHS,RHS],-1)'
g12lazyfd.all_opt = '-a'
g12lazyfd.free_opt  = '--ignore-user-search'

g12cpx = Solver()
g12cpx.name = 'g12cpx'
g12cpx.mznlib = '/home/roberto/sunny-cp/solvers/g12cpx/mzn-lib'
g12cpx.fzn_exec = '/home/roberto/sunny-cp/solvers/g12cpx/fzn-exec'
g12cpx.constraint = 'constraint int_lin_le([1,-1],[LHS,RHS],-1)'
g12cpx.all_opt = '-a'
g12cpx.free_opt = '-f'

g12cbc = Solver()
g12cbc.name = 'g12cbc'
g12cbc.mznlib = '/home/roberto/sunny-cp/solvers/g12cbc/mzn-lib'
g12cbc.fzn_exec = '/home/roberto/sunny-cp/solvers/g12cbc/fzn-exec'
g12cbc.constraint = 'constraint int_lin_le([1,-1],[LHS,RHS],-1)'
g12cbc.all_opt = '-a'
g12cbc.free_opt  = '--ignore-user-search'

