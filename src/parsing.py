'''
sunny-cp: a parallel CP portfolio solver. 

sunny-cp tool allows to solve a Constraint (Satisfaction / Optimization) Problem 
defined in MiniZinc language by using the SUNNY portfolio approach.
sunny-cp is a parallel portfolio solver built on top of 12 constituent solvers:

  Choco, Chuffed, CPX, G12/LazyFD, G12/FD, G12/Gurobi, 
  G12/CBC, Gecode, HaifaCSP, iZplus, MinisatID, OR-Tools

In a nutshell, sunny-cp relies on two sequential steps:

  1. PRE-SOLVING: consists in the parallel execution of a static schedule and 
                  the feature extraction;
                  
  2. SOLVING: consists in the parallel execution of a number of predicted 
              solvers, selected by means of SUNNY algorithm.
              (possibly) selected by means of SUNNY algorithm


Usage: sunny-cp [OPTIONS] <MODEL.mzn> [DATA.dzn] 

Portfolio Options
=================
  -T <TIMEOUT>
    Timeout (in seconds) of SUNNY algorithm, used at runtime for predicting the 
    schedule of solvers to be run. Actually, T will be subtracted by C seconds 
    where C is the time taken by the pre-solving phase (i.e., static schedule 
    and feature extraction). Note that T IS NOT the timeout of the whole solving
    process: indeed, sunny-cp is an "anytime process", which is run indefinitely 
    until a solution is reached. So, the timeout of the whole solving process 
    has to be set externally by the user. The default value is T = 1800.
  -k <SIZE>
    Neighborhood size of SUNNY underlying k-NN algorithm. The default value of 
    k is 70, while the distance metric is the Euclidean one
  -P <PORTFOLIO>
    Specifies the portfolio through a comma-separated list of solvers of the 
    form s_1,s_2,...,s_m. Note that such solvers must be a not empty subset of 
    the default portfolio. The specified ordering of solvers matters: indeed, 
    in case of failure of the scheduled solvers, the other solvers will be 
    executed according to such ordering. This option can be used to select a 
    particular sub-portfolio or even to change the default ordering of the 
    solvers, which is by default: 
      chuffed,g12cpx,haifacsp,izplus,g12lazyfd,minisatid,
      g12fd,choco,gecode,ortools,g12gurobi,g12cbc
  -b <SOLVER>
    Set the backup solver of the portfolio. It must belong to the specified 
    portfolio. The default backup solver is chuffed
  --g12
    Use just the solvers of G12 platform, by using g12cpx as the backup solver. 
    This is equivalent to set -P g12cpx,g12cbc,g12lazyfd,g12fd and -b g12cpx
  -K <PATH>
    Absolute path of the folder which contains the knowledge base. The default 
    knowledge base is in SUNNY_HOME/kb/all_T1800. For more details, see the 
    README file in SUNNY_HOME/kb folder
  -s <SCHEDULE>
    Specifies a static schedule to be run before executing the SUNNY algorithm. 
    The schedule must be passed in the form: 
      s_1,t_1,s_2,t_2,...,s_m,t_m
    where each s_i belongs to the specified portfolio, and t_i is the timeout 
    (in seconds) for s_i. Note that in general when a timeout t_i expires the 
    solver s_i is not killed, but just suspended (and then resumed if s_i has to 
    run again later). The static schedule is empty by default.
  -e <EXTRACTOR>
    Feature extractor used by sunny-cp. By default is "mzn2feat", but it can be 
    changed by defining a corresponding class in SUNNY_HOME/src/features.py
  -p <CORES>
    The number of cores to use in the solving process. By default, is the number 
    of CPUs in the system
  -m <MEM_PERCENTAGE>
    Sets the maximum memory limit (in percentage) for sunny-cp solving process. 
    By default, this value is set to 100%, since the memory check can be pretty 
    resource consuming: it is suggested to set a value lower than 100 only if 
    you are sure that the solving process can be very memory consuming.

Solvers Options
===============
  --fzn-options "<OPTIONS>"
    Allows to run each selected solver on its specific FlatZinc model by using 
    the options specified in <OPTIONS> string. No checks are performed on that 
    string. By default, the options string is empty for CSPs, while is "-a" for 
    COPs. Note that this option should allow to print all the solutions of the 
    problem, according to the MiniZinc Challenge rules.
  --fzn-options-<SOLVER_NAME> "<OPTIONS>"
    Runs the solver <SOLVER_NAME> with the options specified in <OPTIONS>
  --wait-time <TIME>
    Don't stop a running solver if it has produced a solution in the last <TIME> 
    seconds. By default, <TIME> is 2 seconds. Also the constant +inf is allowed
  --wait-time-<SOLVER> <TIME>
    Don't stop <SOLVER> if it has produced a solution in the last <TIME> seconds  
  --restart-time <TIME>
    Restart a constituent solver if its best solution is obsolete and it has not 
    produced a solution in the last <TIME> seconds. 
    By default, <TIME> is 5 seconds. Also the constant +inf is allowed.
  --restart-time-<SOLVER> <TIME>
    Restart <SOLVER> if its best solution is obsolete and it has not produced a 
    solution in the last <TIME> seconds
    
Helper Options
==============
  -h, --help
    Print this message
  -x <AUX_VAR>
    Specifies the name of the auxiliary variable used for tracking the objective 
    function value (for COPs). Note that such variable must not appear in the 
    MiniZinc model to be solved. The default variable name is o__b__j__v__a__r    
  -d <PATH> 
    Absolute path of the folder in which the temporary files created by the 
    solver will be put. The default directory is SUNNY_HOME/tmp, and by default 
    such files are deleted after sunny-cp execution      
  --keep
    Do not erase the temporary files created by the solver and stored in the 
    specified directory (useful for debugging). This option is unset by default    
  --csp-<OPTION> <VALUE>
    Allows to set the specific option only if the input problem is a CSP. Note 
    that the '-' character of <OPTION> must be omitted. For example, --csp-T 900 
    set the T parameter to 900 only if the problem is a CSP, while such option 
    is ignored if the problem is a COP.
  --cop-<OPTION> <VALUE>
    Allows to set the specific option only if the input problem is a COP. Note 
    that the '-' character of <OPTION> must be omitted. For example, --cop-T 900 
    set the T parameter to 900 only if the problem is a COP, while such option 
    is ignored if the problem is a COP.
  -a, -f
    For compatibility with MiniZinc Challenge rules. Note that these options are 
    deprecated, since are always ignored: if needed, use --fzn-options.
'''

import sys
import getopt
from string   import replace
from defaults import *
from features import *
from problem  import *
  
def parse_arguments(args):
  """
  Parse the options specified by the user and returns the corresponding 
  arguments properly set.
  """
  
  # Get the arguments and parse the input model to get auxiliary information. 
  mzn, dzn, opts = get_args(args)
  k, timeout, pfolio, backup, kb, lims, \
  static, solve, obj_expr, mzn_out = parse_model(mzn)
  # Initialize variables with the default values.
  extractor = eval(DEF_EXTRACTOR)
  cores = DEF_CORES
  tmp_dir = DEF_TMP_DIR
  keep = DEF_KEEP
  wait_time = DEF_WAIT_TIME
  restart_time = DEF_RESTART_TIME
  aux_var = DEF_AUX_VAR
  mem_limit = DEF_MEM_LIMIT
  if solve == 'sat':
    solver_options = dict((s, {
      'options': DEF_OPTIONS_CSP, 
      'wait_time': DEF_WAIT_TIME, 
      'restart_time': DEF_RESTART_TIME,
      }) for s in DEF_PFOLIO_CSP
    )
  else:
    solver_options = dict((s, {
      'options': DEF_OPTIONS_COP, 
      'wait_time': DEF_WAIT_TIME, 
      'restart_time': DEF_RESTART_TIME,
      }) for s in DEF_PFOLIO_COP
    )
  
  # Arguments parsing.
  for o, a in opts:
    if o in ('-h', '--help'):
      print __doc__
      sys.exit(0)
    elif o == '-p':
      n = int(a)
      if n < 1:
        print >> sys.stderr, 'Warning: -p parameter set to 1.'
        cores = 1
      elif n > cores:
        print >> sys.stderr, 'Warning: -p parameter set to',cores
      else:
        cores = n
    elif o == '-e':
      extractor = eval(a)
    elif o == '-k':
      k = int(a)
      if k < 0:
        print >> sys.stderr, 'Error! Negative value ' + a + ' for k value.'
        print >> sys.stderr, 'For help use --help'
        sys.exit(2)
    elif o == '-T':
      timeout= int(a)
      if timeout<= 0:
        print >> sys.stderr, 'Error! Non-positive value ' + a + ' for timeout.'
        print >> sys.stderr, 'For help use --help'
        sys.exit(2)
    elif o == '-P':
      p = a.split(',')
      if not p:
        print >> sys.stderr, 'Error! The portfolio ' + a + ' is not valid.'
        print >> sys.stderr, 'For help use --help'
        sys.exit(2)
      if not set(p) <= set(pfolio):
        print >> sys.stderr, 'Error! The portfolio',a,'is not a subset of', \
          str(pfolio)
        print >> sys.stderr, 'For help use --help'
        sys.exit(2)
      pfolio = p
    elif o == '-b':
      backup = a
    elif o == '-K':
      if not os.path.exists(a):
        print >> sys.stderr, 'Error! Directory ' + a + ' not exists.'
        print >> sys.stderr, 'For help use --help'
        sys.exit(2)
      name = [token for token in a.split('/') if token][-1]
      if a[-1] != '/':
        path = a + '/'
      else:
        path = a
      if solve in ['min', 'max']:
        pb = 'cop'
      else:
        pb = 'csp'
      kb = path + 'kb_' + pb + '_' + name
      lims = path + 'lims_' + pb + '_' + name
      if not os.path.exists(kb):
        print >> sys.stderr, 'Error! File ' + kb + ' not exists.'
        print >> sys.stderr, 'For help use --help'
        sys.exit(2)
      if not os.path.exists(lims):
        print >> sys.stderr, 'Error! File ' + kb + ' not exists.'
        print >> sys.stderr, 'For help use --help'
        sys.exit(2)
    elif o == '-s':
      s = a.split(',')
      for i in range(0, len(s) / 2):
	solver = s[2 * i]
	time = int(s[2 * i + 1])
	if time < 0:
	  print >> sys.stderr, 'Error! Not acceptable negative time'
          print >> sys.stderr, 'For help use --help'
          sys.exit(2)
        static.append((solver, time))
    elif o == '-d':
      if not os.path.exists(a):
        print >> sys.stderr, 'Error! Directory ' + a + ' not exists.'
        print >> sys.stderr, 'For help use --help'
        sys.exit(2)
      name = [token for token in a.split('/') if token][-1]
      if a[-1] == '/':
        tmp_dir = a[0 : -1]
      else:
        tmp_dir = a
    elif o == '-m':
      mem_limit = float(a)
    elif o.startswith('--fzn-options'):
      if len(o) > 13:
        solver = o[14:]
        solver_options[solver]['options'] = a
      else:
        for item in solver_options.values():  
          item['options'] = a
    elif o.startswith('--wait-time'):
      wait_time = float(a)
      if wait_time < 0:
        print >> sys.stderr, 'Error! Not acceptable negative time'
        print >> sys.stderr, 'For help use --help'
        sys.exit(2)
      if len(o) > 11:
        solver = o[12:]
        solver_options[solver]['wait_time'] = wait_time
      else:
        for item in solver_options.values():  
          item['wait_time'] = wait_time
    elif o.startswith('--restart-time'):
      rest_time = float(a)
      if rest_time < 0:
        print >> sys.stderr, 'Error! Not acceptable negative time'
        print >> sys.stderr, 'For help use --help'
        sys.exit(2)
      if len(o) > 14:
        solver = o[15:]
        solver_options[solver]['restart_time'] = rest_time
      else:
        for item in solver_options.values():  
          item['restart_time'] = rest_time
    elif o == '-x':
      aux_var = a
    elif o == '--keep':
      keep = True
    elif o == '--g12':
      pfolio = ['g12cpx', 'g12lazyfd', 'g12fd', 'g12cbc']
      backup = 'g12cpx'
    elif o.startswith('--csp-') and solve == 'sat' or \
         o.startswith('--cop-') and solve != 'sat':
           if len(o) == 7:
             opts.append(['-' + o[6], a])
           else:
             opts.append(['--' + o[6:], a])
           
  # Additional checks.
  if backup not in pfolio:
    print >> sys.stderr, \
    'Error! Backup solver ' + backup + ' is not in ' + str(pfolio)
    print >> sys.stderr, 'For help use --help'
    sys.exit(2)
  if not (set(s for (s, t) in static) <= set(pfolio)):
    print >> sys.stderr, \
    'Error! Static schedule is not a subset of ' + str(pfolio)
    print >> sys.stderr, 'For help use --help'
    sys.exit(2)
  st = 0
  for (s, _) in static:
    if s not in pfolio:
      print >> sys.stderr, 'Error! Solver ' + s + ' is not in ' + str(pfolio)
      print >> sys.stderr, 'For help use --help'
      sys.exit(2)
    
  problem = Problem(mzn, dzn, mzn_out, solve, obj_expr, aux_var)
  return problem, k, timeout, pfolio, backup, kb, lims, static, extractor, \
    cores, solver_options, tmp_dir, mem_limit, keep

def get_args(args):
  """
  Get the input arguments.
  """
  dzn = ''
  try:
    options = ['T', 'k', 'P', 'b', 'K', 's', 'd', 'p', 'e', 'x', 'a', 'f', 'm']
    long_options = ['fzn-options', 'wait-time', 'restart-time', 'max-memory']
    long_options += [o + '-' + s for o in long_options for s in DEF_PFOLIO_CSP]
    csp_opts = ['csp-' + o + '=' for o in options + long_options]
    cop_opts = ['cop-' + o + '=' for o in options + long_options]
    long_options = [o + '=' for o in long_options]
    long_options += ['help', 'keep', 'g12'] + csp_opts + cop_opts
    opts, args = getopt.getopt(
      args, 'hafT:k:P:b:K:s:d:p:e:x:m:', long_options
    )
  except getopt.error, msg:
    print msg
    print >> sys.stderr, 'For help use --help'
    sys.exit(2)
  
  if len(args) == 0:
    for o, a in opts:
      if o in ('-h', '--help'):
        print __doc__
        sys.exit(0)
    print >> sys.stderr, 'Error! No arguments given.'
    print >> sys.stderr, 'For help use --help'
    sys.exit(2)
  mzn = args[0]
  if not mzn.endswith('.mzn'):
    print >> sys.stderr, 'Error! MiniZinc input model must have .mzn extension.'
    print >> sys.stderr, 'For help use --help'
    sys.exit(2)
  if len(args) > 1:
    dzn = args[1]
    if not dzn.endswith('.dzn'):
      print >> sys.stderr, \
      'Error! MiniZinc input data must have .dzn extension.'
      print >> sys.stderr, 'For help use --help'
      sys.exit(2)
  return mzn, dzn, opts

def parse_model(mzn):
  """
  Parse the input model to get auxiliary information (i.e., solve and output 
  items).
  """
  # Set default arguments.
  k = DEF_K_CSP
  timeout= DEF_TOUT_CSP
  pfolio = DEF_PFOLIO_CSP
  backup = DEF_BACKUP_CSP
  kb = DEF_KB_CSP
  lims = DEF_LIMS_CSP
  static = DEF_STATIC_CSP
  solve = 'sat'
  solve_item = False
  output_item = False
  include_list = [mzn]
  mzn_out = None
  static = []
  obj_expr = ''
  mzn_dir = os.path.dirname(mzn)
  
  # Possibly extract solve and output items (for COPs).
  while include_list and not (solve_item and output_item):
    model = include_list.pop()
    if os.path.exists(model):
      lines = open(model, 'r').read().split(';')
    elif os.path.exists(mzn_dir + '/' + model):
      model = mzn_dir + '/' + model
      lines = open(model, 'r').read().split(';')
    else:
      continue
    for line in lines:
      include = False
      new_line = ''
      ignore = False
      for l in line:
        # Ignore comments.
        if ignore or l == '%':
          ignore = True
          if l == '\n':
            ignore = False
        else:
          new_line += l
      tokens = new_line.split()
      i = 0
      for token in tokens:
        if token == 'include' or token == 'include"':
          include = True
        # Looking for included models.
        if include and token[-1] == '"' or token[-1] == '";':
          include = \
            replace(replace(replace(token, 'include"', ''),'"', ''), "'", '')
          include_list.append(include)
          include = False
        elif token.endswith('satisfy'):
          include_list = []
          break
        elif token in ['minimize', 'maximize']:
          solve_item = True
          k = DEF_K_COP
          timeout= DEF_TOUT_COP
          pfolio = DEF_PFOLIO_COP
          backup = DEF_BACKUP_COP
          kb = DEF_KB_COP
          lims = DEF_LIMS_COP
          static = DEF_STATIC_COP
          if token == 'minimize':
            solve = 'min'
          else:
            solve = 'max'
          obj_expr = ''
          for j in range(i + 1, len(tokens)):
            obj_expr += tokens[j] + ' '
          if output_item:
            include_list = []
            break
        elif token in ['output', 'output[']:
          mzn_out = model
          output_item = True
          if solve_item:
            include_list = []
            break
        i += 1
  return k, timeout, pfolio, backup, kb, lims, static, solve, obj_expr, mzn_out