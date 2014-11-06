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
    
  name = ''
  mznlib = ''
  fzn_exec = ''
  lt_constraint = ''
  gt_constraint = ''  
    
  def mzn2fzn_cmd(self, pb):
    '''
    Returns the command for converting the given MiniZinc model to FlatZinc.
    '''
    
    fzn = pb.TMP_ID + '.' + self.name + '.fzn'
    ozn = pb.TMP_ID + '.ozn'
    cmd_pref = 'mzn2fzn -I ' + self.mznlib + ' '
    cmd_suff = ' -o ' + fzn + ' --output-ozn-to-file ' + ozn
    
    # If the problem is a CSP, no copy of the MiniZinc model is needed.
    if pb.isCSP():
      return (cmd_pref + pb.mzn + ' ' + pb.dzn + cmd_suff).split()
    
    # The MiniZinc model has already been copied into mzn_cpy.
    if pb.mzn_cpy:
      return (cmd_pref + pb.mzn_cpy + ' ' + pb.dzn + cmd_suff).split()
    
    pb.mzn_cpy = pb.TMP_ID + '.mzn'
    pb.mzn_out_cpy = pb.TMP_ID + '.out'
    shutil.copyfile(pb.mzn, pb.mzn_cpy)
    var_expr = 'var int: ' + pb.OBJ_VAR + ' = ' + pb.obj_mzn + ';\n'
    out_expr = 'output [show(' + pb.OBJ_VAR + ')] ++ '
    
    # No output item defined in the original model.
    if not pb.mzn_out:
      with open(pb.mzn_cpy, 'a') as outfile:
        outfile.write(var_expr)
        outfile.write(out_expr + '[]')
      return (cmd_pref + pb.mzn_cpy + ' ' + pb.dzn + cmd_suff).split()
    
    # The output item is included in the original model
    if pb.mzn == pb.mzn_out:
      with open(pb.mzn, 'r') as infile:
	with open(pb.mzn_cpy, 'w') as outfile:
	  outfile.write(var_expr)
	  for line in infile:
	    if 'output' in line.split() or 'output[' in line.split():
	      line = line.replace('output', out_expr, 1)
	    outfile.write(line)
      return (cmd_pref + pb.mzn_cpy + ' ' + pb.dzn + cmd_suff).split()
   
    # Output item is not included in the original model
    with open(pb.mzn, 'r') as infile:
      with open(pb.mzn_cpy, 'w') as outfile:
	for line in infile:
	  # Replace pb.mzn_out inclusion with pb.mzn_out_cpy inclusion
	  line = replace(
	    line, '"' + pb.mzn_out + '"', '"' + pb.mzn_out_cpy + '"'
	  )
          outfile.write(line)
    with open(pb.mzn_cpy, 'r') as infile:
      with open(pb.mzn_out_cpy, 'w') as outfile:
	# Replace the output item in mzn_out_cpy
        outfile.write(var_expr)
	for line in infile:
	  if 'output' in line.split() or 'output[' in line.split():
	    line = replace(line, 'output', out_expr, 1)
	  outfile.write(line)
    return (cmd_pref + pb.mzn_cpy + ' ' + pb.dzn + cmd_suff).split()
    
  def flatzinc_cmd(self, pb):
    '''
    Returns the command for executing the given FlatZinc model.
    '''
    if pb.isCSP():
      return [self.fzn_exec, pb.fzns[self.name]]
    else:
      return [self.fzn_exec, '-a', pb.fzns[self.name]]
    
  def inject_bound(self, pb, bound):
    '''
    Inject a new bound to the problem.
    '''
    if pb.solve == 'min':
      lt = self.lt_constraint
      new_bound = lt.replace('llt', pb.fzn_var).replace('rlt', str(bound))
    else:
      gt = self.gt_constraint
      new_bound = gt.replace('lgt', pb.fzn_var).replace('rgt', str(bound))
    
    tmp_fzn = pb.fzns[self.name] + '.bound'
    with open(pb.fzns[self.name]) as infile:
      with open('tmp.fzn', 'w') as outfile:
	add = True
	for line in infile:
	  if add and 'constraint' in line.split():
	    outfile.write(bound_const)
	    add = False
	  outfile.write(line)
    shutil.move(tmp_fzn, pb.fzns[self.name])