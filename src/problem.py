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
  
  # Absolute path of the output specification file.
  ozn = ''
  
  # Can be either 'sat', 'min', or 'max' for satisfaction, minimization, or 
  # maximization problems respectively.
  solve = ''
  
  # Objective function expression in the MiniZinc model.
  obj_expr = ''
  
  # Objective variable in the FlatZinc model.
  obj_var = ''
  
  # Best known objective function value for this problem.
  best_bound = None
  
  # Absolute path of the MiniZinc model that actually contains the output string
  # It may coincide with mzn, be a file included in mzn, or be empty.
  mzn_out = ''
  
  # Auxiliary variable artificially introduced in mzn_cpy for keeping track of 
  # the objective function value (printed in std output).
  AUX_VAR = 'o__b__j__v__a__r'
  
  # Absolute path of a copy of the original model mzn. This copy is got from 
  # the original MiniZinc model by adding the AUX_VAR output variable.
  mzn_cpy = ''
  
  # Absolute path of a copy of the model out_mzn containing the output item. 
  # This copy is got from out_mzn by adding the AUX_VAR output variable.
  mzn_out_cpy = ''
  
  # Identifier of the folder where temporary files generated from this problem 
  # (e.g., copies of MiniZinc model or FlatZinc models) are put.
  tmp_dir = ''
  
  # Unique identifier for temporary files.
  TMP_ID = ''
  
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
  
  def has_bound(self):
    """
    Returns True iff the best known bound is defined.
    """
    return float("-inf") < self.best_bound < float("+inf")
  
  def bound_better_than(self, bound):
    """
    Returns True iff the current best bound is better than bound.
    """
    return self.isCOP() and self.best_bound is not None and (
      self.solve == 'min' and self.best_bound < bound or \
      self.solve == 'max' and self.best_bound > bound
    )
  
  def bound_worse_than(self, bound):
    """
    Returns True iff the current best bound is worse than bound: this means that
    the current best bound should be updated.
    """
    return self.isCOP() and bound is not None and (
      self.solve == 'min' and self.best_bound > bound or \
      self.solve == 'max' and self.best_bound < bound
    )
  
  def __init__(self, mzn, dzn, solve, obj_expr, mzn_out, tmp_dir, keep):
    """
    Constructor.
    """
    self.mzn = mzn
    self.dzn = dzn
    assert solve in ['sat', 'min', 'max']
    self.solve   = solve
    if solve == 'min':
      self.best_bound = float('+inf')
    else:
      self.best_bound = float('-inf')
    self.obj_expr = obj_expr
    self.mzn_out = mzn_out
    self.tmp_dir = tmp_dir
    self.keep    = keep
    from socket import gethostname
    from os import getpid
    self.TMP_ID  = tmp_dir + '/tmp_' + gethostname() + '_' + str(getpid())
    self.ozn = self.TMP_ID + '.ozn'
    
  def make_mzn_cpy(self):
    """
    Copies the original MiniZinc model mzn to mzn_cpy, and eventually copies the 
    model mzn_out to mzn_out_cpy.
    """
    self.mzn_cpy = self.TMP_ID + '.mzn'
    self.mzn_out_cpy = self.TMP_ID + '.out'
    import shutil
    shutil.copyfile(self.mzn, self.mzn_cpy)
    var_expr = 'var int: ' + self.AUX_VAR + ' = ' + self.obj_expr + ';\n'
    out_expr = 'output [show(' + self.AUX_VAR + ')] ++ '
    
    # The output item is included in the original model
    if self.mzn == self.mzn_out:
      with open(self.mzn, 'r') as infile:
	with open(self.mzn_cpy, 'w') as outfile:
	  outfile.write(var_expr)
	  for line in infile:
	    if 'output' in line.split() or 'output[' in line.split():
	      line = line.replace('output', out_expr, 1)
	    outfile.write(line)
      return
    
    # No output item defined in the original model.
    if not self.mzn_out:
      with open(self.mzn_cpy, 'a') as outfile:
        outfile.write(var_expr)
        outfile.write(out_expr + '[]')
        return
   
    # Output item is not included in the original model
    with open(self.mzn, 'r') as infile:
      with open(self.mzn_cpy, 'w') as outfile:
	for line in infile:
	  # Replace mzn_out inclusion with mzn_out_cpy inclusion
	  line = replace(
	    line, '"' + self.mzn_out + '"', '"' + self.mzn_out_cpy + '"'
	  )
          outfile.write(line)
    with open(self.mzn_cpy, 'r') as infile:
      with open(self.mzn_out_cpy, 'w') as outfile:
	# Replace the output item in mzn_out_cpy
        outfile.write(var_expr)
	for line in infile:
	  if 'output' in line.split() or 'output[' in line.split():
	    line = replace(line, 'output', out_expr, 1)
	  outfile.write(line)
	  
  def inject_bound_mzn(self, bound):
    """
    Injects a new bound to the copy of the MiniZinc model.
    """
    if self.solve == 'min':
      constraint = '\nconstraint ' + self.obj_expr + ' < ' + str(bound) + ';\n'
    else:
      constraint = '\nconstraint ' + self.obj_expr + ' > ' + str(bound) + ';\n'
    tmp_mzn = self.TMP_ID + '.bound'
    with open(self.mzn, 'r') as infile:
      with open(tmp_mzn, 'w') as outfile:
	tmp_mzn.write(constraint)
	for line in infile:
	  tmp_mzn.write(line)
    shutil.move(tmp_mzn, mzn_cpy)
  
  def inject_bound_fzn(self, solver, bound):
    '''
    Injects a new bound to the FlatZinc model.
    '''
    if self.solve == 'min':
      lt = solver.lt_constraint
      new_bound = lt.replace('llt', pb.obj_var).replace('rlt', str(bound))
    else:
      gt = solver.gt_constraint
      new_bound = gt.replace('lgt', pb.obj_var).replace('rgt', str(bound))
    
    tmp_fzn = self.fzns[solver.name] + '.bound'
    with open(self.fzns[solver.name], 'r') as infile:
      with open(tmp_fzn, 'w') as outfile:
	add = True
	for line in infile:
	  if add and 'constraint' in line.split():
	    outfile.write(bound_const)
	    add = False
	  outfile.write(line)
    shutil.move(tmp_fzn, self.fzns[solver.name])