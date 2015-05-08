'''
Default settings for sunny-cp parameters.
'''

from multiprocessing import cpu_count
import os
SUNNY_HOME = os.environ['SUNNY_HOME']

DEF_K_CSP = 70
DEF_K_COP = 70

DEF_TOUT_CSP = 1800
DEF_TOUT_COP = 1800

DEF_PFOLIO_CSP = [
  'chuffed','g12cpx','haifacsp','izplus','g12lazyfd','minisatid',
  'g12fd','choco','gecode','ortools','g12gurobi','g12cbc'
]
DEF_PFOLIO_COP = [
  'chuffed','g12cpx','haifacsp','izplus','g12lazyfd','minisatid',
  'g12fd','choco','gecode','ortools','g12gurobi','g12cbc'
]

DEF_BACKUP_CSP = 'chuffed'
DEF_BACKUP_COP = 'chuffed'

DEF_KB_CSP   = SUNNY_HOME + '/kb/all_T1800/all_T1800_csp'
DEF_KB_COP   = SUNNY_HOME + '/kb/all_T1800/all_T1800_cop'
DEF_LIMS_CSP = SUNNY_HOME + '/kb/all_T1800/all_T1800_lims_csp'
DEF_LIMS_COP = SUNNY_HOME + '/kb/all_T1800/all_T1800_lims_cop'

DEF_STATIC_CSP = []
DEF_STATIC_COP = []

DEF_EXTRACTOR = 'mzn2feat'

DEF_CORES = cpu_count()

DEF_TMP_DIR = SUNNY_HOME + '/tmp'

DEF_KEEP = False

DEF_WAIT_TIME = 2

DEF_RESTART_TIME = 5

DEF_MEM_LIMIT = 100

DEF_OPT_CSP = ''
DEF_OPT_COP = ''

DEF_ALL = False

DEF_FREE = False

DEF_SWITCH = False