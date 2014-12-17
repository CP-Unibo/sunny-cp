'''
Problem is the abstraction of a MiniZinc model to be solved by sunny-cp.
'''

import uuid
import shutil
from copy import copy
from string import replace

class Problem:
  '''
  Abstraction of a problem.
  '''
   
  # Absolute path of the MiniZinc model of the problem.
  mzn_path = ''
  
  # Absolute path of the data of the problem.
  dzn_path = ''
  
  # Absolute path of the output specification file.
  ozn_path = ''
  
  # Absolute path of the MiniZinc model that actually contains the output string
  # It may coincide with mzn, be a file included in mzn, or be empty.
  out_path = ''
  
  # Can be either 'sat', 'min', or 'max' for satisfaction, minimization, or 
  # maximization problems respectively.
  solve = ''
  
  # Objective function expression in the MiniZinc model.
  obj_expr = ''
  
  # Best known objective function value for this problem.
  best_bound = None
  
  # Auxiliary variable possibly introduced for tracking the objective function 
  # value (that will be printed on std output).
  aux_var = ''
  
  def isCSP(self):
    """
    Returns True if the problem is a satisfaction problem, False otherwise.
    """
    return self.solve == 'sat'
  
  def isCOP(self):
    """
    Returns True if the problem is an optimization problem, False otherwise.
    """
    return self.solve in ['min', 'max']
  
  def has_bound(self):
    """
    Returns True iff an objective bound is known for this problem.
    """
    return float("-inf") < self.best_bound < float("+inf")
  
  def bound_better_than(self, bound):
    """
    Returns True iff the current best bound is better than the specified bound.
    """
    return self.isCOP() and self.has_bound() and (
      self.solve == 'min' and self.best_bound < bound or \
      self.solve == 'max' and self.best_bound > bound
    )
  
  def bound_worse_than(self, bound):
    """
    Returns True iff the current best bound is worse than the specified bound: 
    this means that the current best bound should be updated.
    """
    return self.isCOP() and bound is not None and (
      self.solve == 'min' and self.best_bound > bound or \
      self.solve == 'max' and self.best_bound < bound
    )
  
  def __init__(self, mzn_path, dzn_path, out_path, solve, obj_expr, aux_var):
    """
    Class Constructor.
    """
    self.mzn_path = mzn_path
    self.dzn_path = dzn_path
    self.out_path = out_path
    assert solve in ['sat', 'min', 'max']
    self.solve = solve
    if solve == 'min':
      self.best_bound = float('+inf')
    else:
      self.best_bound = float('-inf')
    self.obj_expr = obj_expr
    self.aux_var = aux_var
    
  def make_cpy(self, mzn_path, out_path, aux = False):
    """
    Creates a copy of the original MiniZinc model at the specified path and 
    returns the corresponding object. If aux flag is set, it also introduces in 
    the copy the variable aux_var for printing the objective value on stdout.
    """
    cpy = copy(self)
    cpy.mzn_path = mzn_path
    cpy.out_path = out_path
    if not aux:
      shutil.copy(self.mzn_path, mzn_path)
      shutil.copy(self.out_path, out_path)
      return cpy
    var_expr = 'var int: ' + self.aux_var + ' = ' + self.obj_expr + ';\n'
    out_expr = 'output [show(' + self.aux_var + ')] ++ '
    
    # The output item is included in the original model
    if self.mzn_path == self.out_path:
      with open(self.mzn_path, 'r') as infile:
        with open(mzn_path, 'w') as outfile:
          outfile.write(var_expr)
          for line in infile:
            if 'output' in line.split() or 'output[' in line.split():
              line = line.replace('output', out_expr, 1)
            outfile.write(line)
      return cpy
    
    # No output item defined in the original model.
    if not self.out_path:
      with open(self.mzn_path, 'r') as infile:
        with open(mzn_path, 'w') as outfile:
          outfile.write(var_expr)
          outfile.write(out_expr + '[];\n')
          for line in infile:
            outfile.write(line)
      return cpy
   
    # Output item is not included in the original model
    with open(self.mzn_path, 'r') as infile:
      with open(mzn_path, 'w') as outfile:
        for line in infile:
          # Replace mzn_out inclusion with mzn_out_cpy inclusion
          line = replace(
            line, '"' + self.out_path + '"', '"' + out_cpy + '"'
          )
          outfile.write(line)
    with open(self.out_path, 'r') as infile:
      with open(out_path, 'w') as outfile:
        # Replace the output item in mzn_out_cpy
        outfile.write(var_expr)
        for line in infile:
          if 'output' in line.split() or 'output[' in line.split():
            line = replace(line, 'output', out_expr, 1)
          outfile.write(line)
    return cpy
    
  def inject_bound(self, bound):
    """
    Injects a new bound to the MiniZinc model.
    """
    if self.solve == 'min':
      constraint = '\nconstraint ' + self.obj_expr + ' < ' + str(bound) + ';\n'
    elif self.solve == 'max':
      constraint = '\nconstraint ' + self.obj_expr + ' > ' + str(bound) + ';\n'
    else:
      return
    tmp_path = str(uuid.uuid4())
    with open(mzn_path, 'r') as infile:
      with open(tmp_path, 'w') as outfile:
        outfile.write(constraint)
        for line in infile:
          outfile.write(line)
    shutil.move(tmp_path, mzn_path)    