'''
csv2kb: builds a knowledge base starting from corresponding CSV files.
  
Usage: python csv2kb.py [OPTIONS] <KB_NAME> <FEAT_FILE> <INFO_FILE> 

Options:

  -h, --help  		
    Print this message
    
  -t <timeout>
    Solving timeout (in seconds) used for collecting the knowledge base runtime 
    information in the <INFO_FILE>. By default, T = 1800.
  
  -p <path>
    Creates the folder <KB_NAME> containing the knowledge base at the specified 
    path. The default path is SUNNY_HOME/kb
  
  -f <lb>,<ub>
    Scales all the features of <FEAT_FILE> in the range [lb, ub], with lb < ub.
    By default, lb = -1 and ub = 1.
    
  -s <lb>,<ub>
    Computes the solving score of the COPs in <INFO_FILE> by scaling the partial 
    solutions in the range [lb, ub], where 0 <= lb < lb <= 1. 
    By default, lb = 0.25 and ub = 0.75
    
  -a <lb>,<ub>
    Computes the solving area of the COPs in <INFO_FILE> by scaling the partial 
    solutions in the range [lb, ub], where 0 <= lb < lb <= 1. 
    By default, lb = 0.25 and ub = 0.75
  
  --no-scale
    Not scales the features.
  
  --no-const
    Not removes constant features.
    
  --no-check
    Not performs consistency checks.
'''

import getopt
import traceback
from helper_kb import *

def main(args):

  # Getting arguments.
  try:
    opts, args = getopt.getopt(
      args, 'ht:p:s:a:f:', ['help', 'no-scale', 'no-const']
    )
  except getopt.error, msg:
    print msg
    print >> sys.stderr, 'For help use --help'
    sys.exit(2)
    
  if len(args) != 3:
    for o, a in opts:
      if o in ('-h', '--help'):
        print __doc__
        sys.exit(0)
    print >> sys.stderr, 'Error! Wrong number of arguments.'
    print >> sys.stderr, 'For help use --help'
    sys.exit(2)
  
  kb_name = args[0]
  feat_file = args[1]
  info_file = args[2]
  timeout = 1800
  path = os.environ['SUNNY_HOME'] + '/kb'
  lb_feat = -1
  ub_feat = 1
  lb_score = 0.25
  ub_score = 0.75
  lb_area = 0.25
  ub_area = 0.75
  scale = True
  const = True
  check = True
  
  # Arguments parsing.
  for o, a in opts:
    if o in ('-h', '--help'):
      print __doc__
      return
    elif o == '-t':
      timeout = int(a)
      if timeout <= 0:
        print >> sys.stderr, 'Error! Timeout',timeout,'is non positive.'
        sys.exit(2)
    elif o == '-p':
      path = a
      if not os.path.exists(a):
	print >> sys.stderr, 'Error! Path',path,'does not exists.'
	sys.exit(2)
    elif o == '-f':
      l, u = a.split(',')
      lb_feat = float(l)
      ub_feat = float(u)
      if lb_feat >= ub_feat:
	print >> sys.stderr, 'Error! Bound',l,'not greater than',u
	sys.exit(2)
    elif o == '-s':
      l, u = a.split(',')
      lb_score = float(l)
      ub_score = float(u)
      if not (0 <= lb_score < ub_score <= 1):
	print >> sys.stderr, 'Error! Must be 0 <=',l,'<',u,'<= 1'
	sys.exit(2)
    elif o == '-a':
      l, u = a.split(',')
      lb_area = float(l)
      ub_area = float(u)
      if not (0 <= lb_area < ub_area <= 1):
	print >> sys.stderr, 'Error! Must be 0 <=',l,'<',u,'<= 1'
	sys.exit(2)
    elif o == '--no-scale':
      scale = False
    elif o == '--no-const':
      const = False
    elif o == '--no-check':
      check = False
  
  kb_path = path + '/' + kb_name
  if os.path.exists(kb_path):
    print >> sys.stderr, 'Error! Folder',kb_path,'already exists! Choose ',
    print >> sys.stderr, 'another name or location for the knowledge base!'
    sys.exit(2)
  
  try:
    # Extract runtimes information.
    kb_csp, kb_cop = compute_infos(
      info_file, timeout, lb_score, ub_score, lb_area, ub_area, check
    )
    # Process the features and make the knowledge base.
    make_kb(
      kb_path, kb_name, feat_file, lb_feat, ub_feat, 
      scale, const, kb_csp, kb_cop
    )
  except Exception as e:
    traceback.print_exc()
    #print e
    if os.path.exists(kb_path):
      from shutil import rmtree
      rmtree(kb_path)
    print 'Knowledge base',kb_name,'not created'
    sys.exit(1)
  
  print 'Knowledge base',kb_name,'created in',path

if __name__ == '__main__':
  main(sys.argv[1:])