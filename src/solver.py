'''
Solver is the abstraction of a constituent solver of the portfolio. Each solver
must be an object of class Solver.

RunningSolver is instead a solver running on a given FlatZinc model.
'''

import psutil

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
  # Solver-specific FlatZinc translation of the MiniZinc constraint "LHS < RHS".
  constraint = ''
  # Solver-specific option for printing all the solutions (for CSPs only) or all
  # the sub-optimal solutions (for COPs only).
  all_opt = ''
  # Solver-specific option for free search (i.e., to ignore search annotations).
  free_opt = ''

class RunningSolver:
  """
  RunningSolver is the abstraction of a constituent solver running on a given
  FlatZinc model.
  """

  # Object of class Solver, identifying the running solver.
  solver = None

  # Status of the solving process. It can be either:
  #     'ready': solver is ready to execute the mzn2fzn conversion
  #   'mzn2fzn': solver is running mzn2fzn converter
  #  'flatzinc': solver is running the FlatZinc interpreter
  # Note that the status is preserved even when a solver process is suspended.
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

  # Dictionary (variable, value) of the best solution currently found by solver.
  solution = {}

  # Can be either 'sat', 'min', or 'max' for satisfaction, minimization, or
  # maximization problems respectively.
  solve = ''

  # Objective variable of the FlatZinc model.
  obj_var = ''

  # Best objective value found by solver.
  obj_value = None

  # Object of class psutil.Popen referring to the solving process.
  process = None

  # output_var is True iff the value of obj_var is annotated with "output_var".
  output_var = True

  # Is switch is set, the search is switched from fixed search to free search
  # (and viceversa) when solver is restarted. Of course, this holds just if the
  # solver allows both free and fixed search.
  switch_search = False

  # Number of times solver has been restarted.
  num_restarts = -1

  # Maximum number of solver restarts allowed.
  max_restarts = -1

  def __init__(self):
    pass

  def __init__(
    self, solver, solve, fzn_path, options, wait_time, restart_time, timeout,
    switch, max_restarts
  ):
    self.status       = 'ready'
    self.solver       = solver
    self.solve        = solve
    self.fzn_path     = fzn_path
    self.fzn_options  = options
    self.wait_time    = wait_time
    self.restart_time = restart_time
    self.timeout      = timeout
    self.num_restarts  = 0
    self.max_restarts = max_restarts
    if solve == 'min':
      self.obj_value = float('+inf')
    elif solve == 'max':
      self.obj_value = float('-inf')
    if self.solver.free_opt:
      self.switch_search = switch
 

  def name(self):
    """
    Returns the name of the running solver.
    """
    return self.solver.name

  def mem_percent(self):
    """
    Returns the memory usage (in percent) of the solver process.
    """
    m = self.process.memory_percent()
    for p in self.process.children(recursive = True):
      try:
        m += p.memory_percent()
      except psutil.NoSuchProcess:
        pass
    return m

  def mzn2fzn_cmd(self, pb):
    """
    Returns the command for converting a given MiniZinc model to FlatZinc by
    using solver-specific redefinitions.
    """
    cmd = 'mzn2fzn --output-ozn-to-file ' + pb.ozn_path + ' -I '     \
        + self.solver.mznlib + ' ' + pb.mzn_path + ' ' + pb.dzn_path \
        + ' -o ' + self.fzn_path
    return cmd.split()

  def flatzinc_cmd(self, pb):
    """
    Returns the command for executing the FlatZinc model.
    """
    cmd = self.solver.fzn_exec + ' ' + self.fzn_options + ' ' + self.fzn_path
    return cmd.split()

  def set_obj_var(self, problem, lb, ub):
    """
    Retrieve and set the name of the objective variable in the FlatZinc model,
    possibly adding the "output_var" annotation to obj_var declaration.
    """
    lines = []
    with open(self.fzn_path, 'r') as infile:
      for line in reversed(infile.readlines()):
        tokens = line.replace('::', ' ').replace(';', '').split()
        if 'solve' in tokens:
          self.obj_var = tokens[-1].replace(';', '')
          cons = ''
          if lb > float('-inf'):
            cons += self.solver.constraint.replace(
              'RHS', self.obj_var).replace('LHS', str(lb - 1)) + ';\n'
          if ub < float('+inf'):
            cons += self.solver.constraint.replace(
              'LHS', self.obj_var).replace('RHS', str(ub + 1)) + ';\n'
          line = cons + line
        if tokens[0] == 'var' and self.obj_var in tokens \
        and 'output_var' not in tokens and '=' not in tokens:
          self.output_var = False
          line = line.replace(';', '') + ' :: output_var;\n'
        lines.append(line)
      infile.close()
    with open(self.fzn_path, 'w') as outfile:
      outfile.writelines(reversed(lines))

  def inject_bound(self, bound):
    """
    Injects a new bound to the FlatZinc model.
    """
    if self.solve == 'min':
      cons = self.solver.constraint.replace(
        'LHS', self.obj_var).replace('RHS', str(bound))
    elif self.solve == 'max':
      cons = self.solver.constraint.replace(
        'RHS', self.obj_var).replace('LHS', str(bound))
    else:
      return
    lines = []
    with open(self.fzn_path, 'r') as infile:
      add = True
      for line in infile.readlines():
        if add and 'constraint' in line.split():
          lines.append(cons + ';\n')
          add = False
        lines.append(line)
    with open(self.fzn_path, 'w') as outfile:
      outfile.writelines(lines)
    self.obj_value = bound
