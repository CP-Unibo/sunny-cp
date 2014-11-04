'''
Default settings for sunny-cp parameters.
'''

import os
SUNNY_HOME = os.environ['SUNNY_HOME']

DEF_k_csp = 70
DEF_k_cop = 70

DEF_T_csp = 1800
DEF_T_cop = 1800

DEF_pfolio_csp = [
  'chuffed',  'g12cpx', 'minisatid', 'gecode',
  'g12lazyfd', 'g12fd', 'g12gurobi', 'g12cbc',
  'haifacsp', 'ortools', 'choco', 'izplus'
]
DEF_pfolio_cop = [
  'chuffed',  'g12cpx', 'minisatid', 'gecode',
  'g12lazyfd', 'g12fd', 'g12gurobi', 'g12cbc',
  'haifacsp', 'ortools', 'choco', 'izplus'
]

DEF_backup_csp = 'chuffed'
DEF_backup_cop = 'chuffed'

DEF_kb_csp   = SUNNY_HOME + '/kb/all_T1800/all_T1800_csp'
DEF_kb_cop   = SUNNY_HOME + '/kb/all_T1800/all_T1800_cop'
DEF_lims_csp = SUNNY_HOME + '/kb/all_T1800/all_T1800_lims_csp'
DEF_lims_cop = SUNNY_HOME + '/kb/all_T1800/all_T1800_lims_cop'

DEF_static_csp = []
DEF_static_cop = []

DEF_extractor = 'mzn2feat'

from multiprocessing import cpu_count
DEF_cores = cpu_count()

# If KEEP == True, do not remove temporary files.
DEF_KEEP = False

# Directory where temporary files will put.
DEF_TMP_DIR = SUNNY_HOME + '/tmp'

# Unique identifier of temporary files.
from socket import gethostname
DEF_TMP_ID = DEF_TMP_DIR + '/tmp_' + gethostname() + '_' + str(os.getpid())

# Variable artificially introduced for keeping track of the objective function.
DEF_OBJ_VAR = 'o__b__j__v__a__r'