'''
Solver is the abstraction of a constituent solver of the portfolio. Each solver 
must be a subclass of Solver.
'''

class Solver:
  """
  Solver is the abstraction of a constituent solver of the portfolio.
  """
    
  def mzn2fzn_cmd(self, pb):
    '''
    Returns the command for converting the given MiniZinc model to FlatZinc.
    '''
    fzn = pb.TMP_ID + '.' + self.name + '.fzn'
    ozn = pb.TMP_ID + '.ozn'
    pb.fzns[self.name] = fzn
    pb.ozn = ozn
    cmd = ['mzn2fzn', '-I', self.mznlib, pb.mzn]
    if pb.dzn:
      return cmd + [pb.dzn, '-o', fzn, '--output-ozn-to-file', ozn]
    else:
      return cmd + ['-o', fzn, '--output-ozn-to-file', ozn]
    
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
    
    from shutil import move
    from string import replace
    
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
    move(tmp_fzn, pb.fzns[self.name])