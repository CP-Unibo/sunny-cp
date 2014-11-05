'''
Problem is the abstraction of an input problem to be solved by sunny-cp
'''

class Problem:
  '''
  Abstraction of a problem.
  '''
   
  # Absolute path of the MiniZinc model of the problem.
  mzn = ''
  
  # Absolute path of the data of the problem.
  dzn = ''
  
  # A dictionary that associates to each solver name the absolute path of the 
  # corresponding FlatZinc model.
  fzns = {}
  
  # Absolute path of the output specifications of the problem.
  ozn = ''
  
  # Can be either 'sat', 'min', or 'max' for satisfaction, minimization, or 
  # maximization problems respectively.
  solve = ''
  
  # Objective function expression (in the MiniZinc model).
  obj_mzn = ''
  
  # Objective function variable (in the FlatZinc model).
  obj_fzn = ''
  
  # Absolute path of the MiniZinc model that actually contains the output string
  mzn_out = ''
  
  # Auxiliary variable artificially introduced in mzn_copy for keeping track of 
  # the objective function value (printed in std output).
  OBJ_VAR = 'o__b__j__v__a__r'
  
  # Absolute path of the copy of the original MiniZinc model. This copy is got 
  # from the original model by adding the OBJ_VAR output variable.
  mzn_copy = None
  
  # Identifier of the folder where temporary files (i.e., mzn_copy, the FlatZinc
  # models in fzns and ozn) are possibly put.
  tmp_dir = None
  
  # Unique identifier for temporary files.
  TMP_ID = None
  
  # If keep, do not remove temporary files.
  keep = None
  
  
  def isCSP(self):
    """
    Returns True iff the problem is a satisfaction problem.
    """
    return self.solve == 'sat'
  
  def isCOP(self):
    """
    Returns True iff the problem is an optimization problem.
    """
    return self.solve != 'sat'
  
  def better(self, x, y):
    """
    Returns True iff the objective value x is better than the objective value y 
    for this problem
    """
    if self.isCSP():
      return False
    return self.solve == 'min' and x < y or self.solve == 'max' and x > y
  
  def __init__(self, mzn, dzn, solve, obj_mzn, mzn_out, tmp_dir, keep):
    """
    Constructor.
    """
    self.mzn = mzn
    self.dzn = dzn
    assert solve in ['sat', 'min', 'max']
    self.solve   = solve
    self.obj_mzn = obj_mzn
    self.mzn_out = mzn_out
    self.tmp_dir = tmp_dir
    self.keep    = keep
    from socket import gethostname
    from os import getpid
    self.TMP_ID  = tmp_dir + '/tmp_' + gethostname() + '_' + str(getpid())