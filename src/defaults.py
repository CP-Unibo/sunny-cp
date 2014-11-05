'''
Default settings for sunny-cp parameters.
'''

import os
SUNNY_HOME = os.environ['SUNNY_HOME']

DEF_K_CSP = 70
DEF_K_COP = 70

DEF_T_CSP = 1800
DEF_T_COP = 1800

# FIXME: Change this ordering.
DEF_PFOLIO_CSP = [
  'chuffed',  'g12cpx', 'minisatid', 'gecode',
  'g12lazyfd', 'g12fd', 'g12gurobi', 'g12cbc',
  'haifacsp', 'ortools', 'choco', 'izplus'
]
DEF_PFOLIO_COP = [
  'chuffed',  'g12cpx', 'minisatid', 'gecode',
  'g12lazyfd', 'g12fd', 'g12gurobi', 'g12cbc',
  'haifacsp', 'ortools', 'choco', 'izplus'
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

from multiprocessing import cpu_count
DEF_CORES = cpu_count()

DEF_TMP_DIR = SUNNY_HOME + '/tmp'

DEF_KEEP = False