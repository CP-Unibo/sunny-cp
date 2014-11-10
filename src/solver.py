'''
Solver is the abstraction of a constituent solver of the portfolio. Each solver 
must be a subclass of Solver.
'''

import shutil
from string import replace

class Solver:
  """
  Solver is the abstraction of a constituent solver of the portfolio.
  """
  
  # Solver name.
  name = ''
  # Absolute path of the folder containing solver-specific redefinitions.
  mznlib = ''
  # Absolute path of the command used for executing a FlatZinc model.
  fzn_exec = ''
  # Solver representation of a MiniZinc constraint llt < rlt.
  lt_constraint = ''
  # Solver representation of a MiniZinc constraint lgt < rgt.
  gt_constraint = ''
  
  def mzn2fzn_cmd(self, pb, fzn):
    '''
    Returns the command for converting the given MiniZinc model to FlatZinc.
    '''
    pref = 'mzn2fzn -I ' + self.mznlib + ' '
    suff = ' ' + pb.dzn + ' -o ' + fzn + ' --output-ozn-to-file ' + pb.ozn
    # If the problem is a CSP, no copy of the MiniZinc model is needed.
    if pb.isCSP():
      return (pref + pb.mzn + suff).split()
    else:
      return (pref + pb.mzn_cpy + suff).split()
    
  def flatzinc_cmd(self, pb):
    '''
    Returns the command for executing the given FlatZinc model.
    '''
    if pb.isCSP():
      return [self.fzn_exec, pb.fzns[self.name]]
    else:
      return [self.fzn_exec, '-a', pb.fzns[self.name]]