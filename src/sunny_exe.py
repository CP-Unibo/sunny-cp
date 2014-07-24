"""
Module for executing the scheduled solvers on a given CP problem.
"""
from string import replace
from subprocess import Popen, PIPE, call
import subprocess as sp
import sys
import os
import shutil
import tempfile
import time


# Path of the bash files containing the solvers instructions for solving a 
# given CSP/COP and for checking if a solution is valid
EXE_COP = os.environ['SUNNY_HOME'] + '/src/exe_cop'
EXE_GET_SOL = os.environ['SUNNY_HOME'] + '/src/get_solution'
EXE_PRINT_SOL = os.environ['SUNNY_HOME'] + '/src/output_script'
# If SAT is True, the problem has at least a solution (for COPs).
SAT = False
# PID is the process ID of the running command.
PID = None
# Variable artificially introduced for keeping track of the objective function.
OBJ_VAR = 'o__b__j__v__a__r'

class SearchCompleted(Exception):
  """
  Exception raised when the search is completed.
  """
  pass

def get_pid():
  """
  Returns the PID of the running command.
  """
  global PID
  return PID

def exe_schedule(schedule, mzn, dzn, obj, obj_var, obj_bound, tmp_id, out_mzn):
  """
  Executes the scheduled solvers according to the specified order.
  """
  # Initialize the name of temporary files.
  global SAT
  if dzn == '':
    dzn = 'NODATA'
  tmp_fzn = tmp_id + '.fzn'
  tmp_ozn = tmp_id + '.ozn'
  tmp_out = tmp_id + '.out'
  tmp_sol = tmp_id + '.sol'
  if obj_var:
    tmp_mzn = tmp_id + '.mzn'
    tmp_inc = tmp_id + '.inc'
    if not os.path.exists(tmp_mzn):
      update_mzn(mzn, tmp_mzn, out_mzn, tmp_inc, obj_var)
  
  # Time not used by the previous solver due to a failure.
  additional_time = 0 
  
  # Execute solver s for t seconds.
  for (s, t) in schedule:
    t = t + additional_time
    additional_time = 0
    if obj_var:
      if obj_bound:
	# A partial solution is found: the model must be updated accordingly.
	SAT = True
	add_constraint(tmp_mzn, obj, obj_var, obj_bound, tmp_id)
      time1 = time.time()
      obj_bound = exe_solver_cop(
        s, t, tmp_mzn, dzn, tmp_fzn, tmp_ozn, tmp_out, tmp_sol
      )
      time2 = time.time()
      if (time2 - time1) < t:
	additional_time = t - (time2 - time1)
    else:
      time1 = time.time()
      exe_solver_csp(s, t, mzn, dzn, tmp_fzn, tmp_ozn, tmp_out,tmp_sol)
      time2 = time.time()
      if (time2 - time1) < t:
	additional_time = t - (time2 - time1)
  return obj_bound
  
def update_mzn(mzn, tmp_mzn, out_mzn, tmp_inc, obj_var):
  """
  Updates the original MiniZinc model(s) for formatting the output string. 
  The original model mzn is left unaltered.
  """
  global OBJ_VAR
  shutil.copyfile(mzn, tmp_mzn)
  out_expr = \
    'output [ "% ' + OBJ_VAR + ' = ", show(' + OBJ_VAR + '), "\\n" ] ++ '
  if mzn == out_mzn:
    with open(mzn, 'r') as infile:
      with open(tmp_mzn, 'w') as outfile:
        outfile.write('var int: ' + OBJ_VAR + ' = ' + obj_var + ';\n')
	for line in infile:
	  if 'output' in line.split() or 'output[' in line.split():
	    line = line.replace('output', out_expr, 1)
	  outfile.write(line)
  else:
    # output string is omitted in mzn or included in another file.
    if not out_mzn:
      with open(tmp_mzn, 'a') as outfile:
        outfile.write('var int: ' + OBJ_VAR + ' = ' + obj_var + ';\n')
        outfile.write('output [show(' + OBJ_VAR + '), "\\n" ]')
      return
    with open(mzn, 'r') as infile:
      with open(tmp_mzn, 'w') as outfile:
	for line in infile:
	  line = replace(line, '"' + out_mzn + '"', '"' + tmp_inc + '"')
          outfile.write(line)
    with open(out_mzn, 'r') as infile:
      with open(tmp_inc, 'w') as outfile:
        outfile.write('var int: ' + OBJ_VAR + ' = ' + obj_var + ';\n')
	for line in infile:
	  if 'output' in line.split() or 'output[' in line.split():
	    line = replace(line, 'output', out_expr, 1)
	  outfile.write(line)  

def add_constraint(tmp_mzn, obj, obj_var, obj_bound, tmp_id):
  """
  Add the bound constraint to tmp_mzn.
  """
  tmp_name = tmp_id + '.con'
  tmp_con = open(tmp_name, 'w')
  with open(tmp_mzn, 'r') as mznfile:
    if obj == 'min':
      con = '\nconstraint ' + obj_var + ' < ' + obj_bound + ';\n'
      print '% Adding constraint',obj_var + ' < ' + obj_bound
    else:
      con = '\nconstraint ' + obj_var + ' > ' + obj_bound + ';\n'
      print '% Adding constraint',obj_var + ' > ' + obj_bound
    tmp_con.write(con)
    for line in mznfile:
      tmp_con.write(line)
  shutil.move(tmp_name, tmp_mzn)
  
def print_solution(out,sol,ozn):
  assert(os.path.exists(out))
  
  proc = Popen(['bash', '-c', EXE_GET_SOL + " " + out + " " + sol])
  proc.wait()
  rv = proc.returncode
  if rv != 0:
    print \
      "% Impossible to found last solution: solns2dzn -l returned with value " + \
      str(rv)
    return False
  proc = Popen(
    ['bash', '-c', EXE_PRINT_SOL + ' ' + ozn + ' ' + sol + ' ' + out]
  )
  proc.wait()
  rv = proc.returncode
  if rv != 0:
    print "% Impossible to print solution: solns2out returned with value " + str(rv)
    return False
  output = open(out, 'r').readlines()
  for line in output:
    line = replace(line, '\n', '')
    print line
  return True

def get_objective_value(out):
  output = open(out, 'r').readlines()
  for line in output:
    if OBJ_VAR in line:
      line = replace(line, '\n', '')
      return replace(line.split(' = ')[1], ';', '')

def exe_solver_cop(solver, timeout, mzn, dzn, fzn, ozn, out,tmp_sol):
  """
  Executes a single solver on a COP for a given time limit. If the solver is not 
  able to complete the solving process, the function returns the best objective 
  value found so far (returns None is no value is found).
  """
  global EXE_COP, PID, OBJ_VAR, SAT
  timeout = int(round(timeout))
  # Exploit the bash timeout.
  cmd = 'timeout ' + str(timeout) + ' unbuffer bash ' + EXE_COP + ' ' + solver   + ' ' \
      + mzn + ' ' + dzn + ' ' + fzn + ' ' + ozn + ' ' + out + " COP"
  print '% Executing ' + solver + ' for ' + str(timeout) + ' seconds.'
  
  obj_bound = None
  sol_file = open(out, 'w')
  
  proc = Popen(cmd.split(),stdout=PIPE)
     
  # Poll process for new output until finished
  while True:
    line = proc.stdout.readline()
    if line == '' and proc.poll() != None:
      break
    else:
        if '==========' in line:
	  print '% Search completed by ' + solver
	  print replace(line, '\n', '')
	  raise SearchCompleted
	elif '=====UNSATISFIABLE=====' in line:     
	  if SAT:
	    print '% Search completed by ' + solver
	    print '=========='
	  else:
	    print '% Search completed by ' + solver
	    print replace(line, '\n', '')
	  raise SearchCompleted
	elif '----------' in line:
	  sol_file.write(line)
	  sol_file.close()
	  if print_solution(out,tmp_sol,ozn):
	    SAT = True
	    sol_file = open(out, 'w')
	elif OBJ_VAR in line:
	  sol_file.write(line)
	  obj_bound = replace(replace(line.split(' = ')[1], ';', ''),'\n', '')
	  print '% New bound found: ' + obj_bound
	else:
	  sol_file.write(line)
  
  sol_file.close()
  proc.communicate()[0]
  rv = proc.returncode
  
  print "% The execution of solver " + solver + " finished with return value " + str(rv)
  print '% Search not yet completed.'
  return obj_bound

def exe_solver_csp(solver, timeout, mzn, dzn, fzn, ozn, out, tmp_sol):
  """
  Executes a single solver on a CSP for a given time limit.
  """
  global EXE_CSP, PID
  timeout = int(round(timeout))
  cmd = 'timeout ' + str(timeout) + ' unbuffer bash ' + EXE_COP + ' ' + solver   + ' ' \
      + mzn + ' ' + dzn + ' ' + fzn + ' ' + ozn + ' ' + out + " CSP"
  print '% Executing ' + solver + ' for ' + str(timeout) + ' seconds.' 
  proc = Popen(cmd.split())
  PID = proc.pid
  proc.communicate()
  rv = proc.returncode
  print "% The execution of solver " + solver + " finished with return value " + str(rv)
  # Read the output from the end to the begin, assuming the monotonicity of the 
  # printed solutions.
  reversed_output = []
  if os.path.exists(out):
    reversed_output = reversed(open(out, 'r').readlines())
  for line in reversed_output:
    line = replace(replace(line, '\n', ''), ';', '')
    # FIXME: =====UNBOUNDED===== ignored.
    if line in ['=====UNSATISFIABLE=====']:
      print line
      print '% Search completed by ' + solver
      raise SearchCompleted
    elif line in ['==========']:
      if print_solution(out,tmp_sol,ozn):
	print line
	print '% Search completed by ' + solver
	raise SearchCompleted
    elif line in ['----------']:
      if print_solution(out,tmp_sol,ozn):
	print '% Search completed by ' + solver
	raise SearchCompleted
  print '% Search not yet completed.'
  return None
