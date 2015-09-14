'''
Default settings for sunny-cp parameters.
'''

from multiprocessing import cpu_count
import os
SUNNY_HOME = os.path.realpath(__file__).split('/')[:-2]
SUNNY_HOME = '/'.join(SUNNY_HOME)

DEF_K = -1

DEF_TOUT = 1200

DEF_PFOLIO = []
pfolio_solvers = open(SUNNY_HOME + '/src/pfolio_solvers.py')
for row in pfolio_solvers:
  if ' = Solver()' in row:
    DEF_PFOLIO.append(row.split(' = ')[0])

DEF_BACKUP = 'chuffed'

DEF_STATIC = []

DEF_KB_CSP   = SUNNY_HOME + '/kb/mznc1215/mznc1215_csp'
DEF_KB_COP   = SUNNY_HOME + '/kb/mznc1215/mznc1215_cop'

DEF_LIMS_CSP = SUNNY_HOME + '/kb/mznc1215/mznc1215_lims_csp'
DEF_LIMS_COP = SUNNY_HOME + '/kb/mznc1215/mznc1215_lims_cop'

DEF_EXTRACTOR = 'mzn2feat'

DEF_CORES = cpu_count()

DEF_TMP_DIR = SUNNY_HOME + '/tmp'

DEF_KEEP = False

DEF_WAIT_TIME = 2

DEF_RESTART_TIME = 5

DEF_MEM_LIMIT = 100

DEF_OPTS = ''

DEF_ALL = False

DEF_FREE = False

DEF_SWITCH = False

DEF_LB = float('-inf')

DEF_UB = float('+inf')

DEF_RESTARTS = float('+inf')

DEF_CHECK = {}
