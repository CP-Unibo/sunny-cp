'''
Solver is the abstraction of a constituent solver of the portfolio. Each solver 
must be a subclass of Solver.

RunningSolver is instead a solver running on a given FlatZinc model.
'''

import uuid
import psutil
from shutil import move
from string import replace

class Solver:
  """
  Solver is the abstraction of a constituent solver of the portfolio.
  """
  
  # Solver name. It must be an unique identifier.
  name = ''
  # Absolute path of the folder containing solver-specific redefinitions.
  mznlib = ''
  # Absolute path of the command used for executing a FlatZinc model.
  fzn_exec = ''
  # Solver representation of a MiniZinc constraint "llt < rlt".
  lt_constraint = ''
  # Solver representation of a MiniZinc constraint "lgt < rgt".
  gt_constraint = ''
  
class RunningSolver:
  """
  RunningSolver is a solver running on a given FlatZinc model.
  """
  
  # Object of class Solver, identifying the running solver.
  solver = None
  
  # Status of the solving process. It can be either:
  #     'ready': solver is ready to execute the mzn2fzn conversion
  #   'mzn2fzn': solver is running mzn2fzn converter
  #  'flatzinc': solver is running the FlatZinc interpreter
  status = ''
  
  # Don't stop solver if it has produced a solution in the last wait_time sec.
  wait_time = -1
  
  # Restart solver if its best solution is obsolete and it has not produced a 
  # solution in the last restart_time sec.
  restart_time = -1
  
  # Timeout in seconds of the solving process.
  timeout = -1
  
  # Time in seconds (since the epoch) when the solving process started.
  start_time = -1
  
  # Time in seconds (since the epoch) when the solver found its last solution.
  solution_time = -1
  
  # Absolute path of the FlatZinc model on which solver is run.
  fzn_path = ''
  
  # String of the options used by the FlatZinc interpreter of the solver.
  fzn_options = ''
  
  # Array of the best solution currently found by solver, where each element 
  # corresponds to a line <VARIABLE> = <VALUE> printed by solver on std output.
  solution = []
  
  # Can be either 'sat', 'min', or 'max' for satisfaction, minimization, or 
  # maximization problems respectively.
  solve = ''
  
  # Objective variable of the FlatZinc model.
  obj_var = ''
  
  # Best objective value found by solver.
  obj_value = None
  
  # Object of class psutil.Popen referring to the solving process.
  process = None
  
  def __init__(
    self, solver, solve, fzn_path, options, wait_time, restart_time, timeout
  ):
    self.status       = 'ready'
    self.solver       = solver
    self.solve        = solve
    if solve == 'min':
      self.obj_value = float('+inf')
    elif solve == 'max':
      self.obj_value = float('-inf')
    self.fzn_path     = fzn_path
    self.fzn_options  = options
    self.wait_time    = wait_time
    self.restart_time = restart_time
    self.timeout      = timeout
  
  def name(self):
    return self.solver.name
  
  def mem_percent(self):
    m = self.process.memory_percent()
    for p in self.process.children(recursive = True):
      try:
        m += p.memory_percent()
      except psutil.NoSuchProcess:
	pass
    return m
  
  def mzn2fzn_cmd(self, pb):
    '''
    Returns the command for converting a given MiniZinc model to FlatZinc by 
    using solver-specific redefinitions.
    '''
    cmd = 'mzn2fzn -I ' + self.solver.mznlib + ' ' + pb.mzn_path + ' '     + \
           pb.dzn_path + ' -o ' + self.fzn_path + ' --output-ozn-to-file ' + \
           pb.ozn_path
    return cmd.split()
    
  def flatzinc_cmd(self, pb):
    '''
    Returns the command for executing the FlatZinc model.
    '''
    cmd = self.solver.fzn_exec + ' ' + self.fzn_options + ' ' + self.fzn_path
    return cmd.split()
  
  def set_obj_var(self):
    with open(self.fzn_path, 'r') as infile:
      for line in reversed(infile.readlines()):
        tokens = line.split()
        if 'solve' in tokens:
          self.obj_var = tokens[-1].replace(';', '')
          break
  
  def inject_bound(self, bound):
    '''
    Injects a new bound to the FlatZinc model.
    '''
    if self.solve == 'min':
      lt = self.solver.lt_constraint
      constraint = lt.replace('llt', self.obj_var).replace('rlt', str(bound))
    elif self.solve == 'max':
      gt = self.solver.gt_constraint
      constraint = gt.replace('lgt', self.obj_var).replace('rgt', str(bound))
    else:
      return
    tmp_path = str(uuid.uuid4())
    with open(self.fzn_path, 'r') as infile:
      with open(tmp_path, 'w') as outfile:
        add = True
        for line in infile:
          if add and 'constraint' in line.split():
            outfile.write(constraint + ';\n')
            add = False
          outfile.write(line)
    move(tmp_path, self.fzn_path)
    self.obj_value = bound
