'''
This module contains an object of class Solver for each installed solver of the 
portfolio. Each object of class Solver might be defined manually, but it is 
however strongly suggested to first generate it automatically by using the
make_pfolio.py script in solvers folder. Then, once the file is created, it 
is possible to customize each object. Note that running make_pfolio.py script 
will replace the current file.
'''

from solver import Solver

g12fd = Solver()
g12fd.name = 'g12fd'
g12fd.mznlib = '/home/roberto/sunny-cp/solvers/g12fd/mzn-lib'
g12fd.fzn_exec = '/home/roberto/sunny-cp/solvers/g12fd/fzn-exec'
g12fd.constraint = 'constraint int_lin_le([1,-1],[LHS,RHS],-1)'
g12fd.all_opt = '-a'
g12fd.free_opt  = '--ignore-user-search'


opturion = Solver()
opturion.name = 'opturion'
opturion.mznlib = '/home/roberto/sunny-cp/solvers/opturion/mzn-lib'
opturion.fzn_exec = '/home/roberto/sunny-cp/solvers/opturion/fzn-exec'
opturion.constraint = 'constraint int_lin_le([1,-1],[LHS,RHS],-1)'
opturion.all_opt = '-a'
opturion.free_opt  = '-f'


mistral = Solver()
mistral.name = 'mistral'
mistral.mznlib = '/home/roberto/sunny-cp/solvers/mistral/mzn-lib'
mistral.fzn_exec = '/home/roberto/sunny-cp/solvers/mistral/fzn-exec'
mistral.constraint = 'constraint int_lin_le([1,-1],[LHS,RHS],-1)'
mistral.all_opt = '-a'
mistral.free_opt  = ''


g12lazyfd = Solver()
g12lazyfd.name = 'g12lazyfd'
g12lazyfd.mznlib = '/home/roberto/sunny-cp/solvers/g12lazyfd/mzn-lib'
g12lazyfd.fzn_exec = '/home/roberto/sunny-cp/solvers/g12lazyfd/fzn-exec'
g12lazyfd.constraint = 'constraint int_lin_le([1,-1],[LHS,RHS],-1)'
g12lazyfd.all_opt = '-a'
g12lazyfd.free_opt  = '--ignore-user-search'

izplus = Solver()
izplus.name = 'izplus'
izplus.mznlib = '/home/roberto/sunny-cp/solvers/izplus/mzn-lib'
izplus.fzn_exec = '/home/roberto/sunny-cp/solvers/izplus/fzn-exec'
izplus.constraint = 'constraint int_lin_le([1,-1],[LHS,RHS],-1)'
izplus.all_opt = '-a'
izplus.free_opt  = '-f'


gecode = Solver()
gecode.name = 'gecode'
gecode.mznlib = '/home/roberto/sunny-cp/solvers/gecode/mzn-lib'
gecode.fzn_exec = '/home/roberto/sunny-cp/solvers/gecode/fzn-exec'
gecode.constraint = 'constraint int_lin_le([1,-1],[LHS,RHS],-1)'
gecode.all_opt = '-a'
gecode.free_opt  = '-f'


g12mip = Solver()
g12mip.name = 'g12mip'
g12mip.mznlib = '/home/roberto/sunny-cp/solvers/g12mip/mzn-lib'
g12mip.fzn_exec = '/home/roberto/sunny-cp/solvers/g12mip/fzn-exec'
g12mip.constraint = 'constraint int_lin_le([1,-1],[LHS,RHS],-1)'
g12mip.all_opt = '-a'
g12mip.free_opt  = '--ignore-user-search'


chuffed = Solver()
chuffed.name = 'chuffed'
chuffed.mznlib = '/home/roberto/sunny-cp/solvers/chuffed/mzn-lib'
chuffed.fzn_exec = '/home/roberto/sunny-cp/solvers/chuffed/fzn-exec'
chuffed.constraint = 'constraint int_lin_le([1,-1],[LHS,RHS],-1)'
chuffed.all_opt = '-a'
chuffed.free_opt  = '-f'


