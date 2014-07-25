import os
from socket import gethostname

# SUNNY_HOME environment variable must be set.
SUNNY_HOME = os.environ['SUNNY_HOME']

# If KEEP == True, do not remove temporary files.
KEEP = False
# Directory where temporary files will put.
TMP_DIR = SUNNY_HOME + '/tmp'
# Unique identifier of temporary files.
TMP_ID = TMP_DIR + '/tmp_' + gethostname() + '_' + str(os.getpid())
# Variable artificially introduced for keeping track of the objective function.

# type of output_type.
# possible values: minizinc | flatzinc
OUTPUT_TYPE = "minizinc"

# Variable artificially introduced for keeping track of the objective function.
OBJ_VAR = 'o__b__j__v__a__r'

# PID is the process ID of the running command.
PID = None

# Path of the bash files containing the solvers instructions for solving a 
# given CSP/COP and for checking if a solution is valid
EXE_COP = os.environ['SUNNY_HOME'] + '/src/exe_cop'

# If SAT is True, the problem has at least a solution (for COPs).
SAT = False

