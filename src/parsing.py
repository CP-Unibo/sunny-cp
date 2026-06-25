'''
SUNNY-CP is a parallel portfolio solver that allows one to solve constraint
satisfaction/optimization problems defined in the MiniZinc language.
By default, solutions are printed in MiniZinc-formatted output.

USAGE: sunny-cp [OPTIONS] <MODEL.mzn> [DATA.dzn]

Internally, SUNNY-CP solves FlatZinc instances. The low-level solver
    sunny-cp-fzn emits raw FlatZinc solution streams. The sunny-cp wrapper runs:

        sunny-cp-fzn --mzn-output ... | solns2out

    where solns2out translates FlatZinc solutions back to MiniZinc output using
    solver-specific .ozn files.

    Use --fzn-output to print the raw FlatZinc solution stream instead.

WARNING: the order in [OPTIONS] matters! For instance, by typing the command:
         sunny-cp -p 1 -p 2 <MODEL.mzn> [DATA.dzn] the option -p will be set to
         value 2, since option -p 1 will be overwritten by -p 2.
   

Portfolio Options
=================
  -T <TIMEOUT>
    Timeout (in seconds) of SUNNY algorithm, used at runtime for predicting the
    schedule of solvers to be run. Actually, T will be subtracted by C seconds
    where C is the time taken by the pre-solving phase. Note that T IS NOT the
    timeout of the whole solving process: sunny-cp is an "anytime process", run
    indefinitely until a solution is reached. So, the timeout of sunny-cp has
    to be set externally by the user. The default value is T = 1200 sec., the
    same timeout of MiniZinc Challenge 2015. Also the constant +inf is allowed.
  -k <SIZE>
    Neighborhood size of SUNNY underlying k-NN algorithm. The default value of
    k is the square root of the knowledge base size.
  -P <PORTFOLIO>
    Specifies the portfolio through a comma-separated list of solvers of the
    form s_1,s_2,...,s_m. The specified ordering matters: indeed, if all the
    scheduled solvers fails, the other solvers will be run to such ordering.
    By default, the portfolio includes all the installed solvers.
  -A <SOLVERS>
    Adds to the default portfolio (or to the one specified with -P option) the
    solvers in <SOLVERS>, which is a list of the form s_1,...,s_m.
  -R <SOLVERS>
    Removes from the default portfolio (or from the portfolio specified with -P
    option) the solvers in <SOLVERS>, which is a list of the form s_1,...,s_m.
  -b <SOLVER>
    Set the backup solver of the portfolio. If the backup solver is not in the
    specified portfolio, the first solver of the portfolio is selected. The
    default backup solver is chuffed.
  -K <PATH>
    Absolute path of the folder which contains the knowledge base. For more
    details, see the README file in kb folder
  -s <SCHEDULE>
    Specifies a static schedule to be run before executing the SUNNY algorithm.
    It must in the form  s_1,t_1,s_2,t_2,...,s_m,t_m  where t_i is the time
    limit (in seconds) allocated to solver s_i. Note that in general when a
    timeout t_i expires the solver s_i is not killed, but just suspended (and
    then resumed if s_i has to run again later). The static schedule is empty
    by default. Also the constant +inf is allowed for the times t_i.
  -e <EXTRACTOR>
    Feature extractor used by sunny-cp. By default is "mzn2feat", but it can be
    changed by defining a corresponding class in src/features.py.
  -a
    Prints to standard output all the solutions of the problem (for CSPs only).
    or all the sub-optimal solutions (for COPs only).
  -f
    Imposes the free search to all the running solvers, i.e., any search
    annotation will be ignored.
  -p <CORES>
    The number of cores to use in the solving process. By default, it is the
    number of CPUs in the system
  -m <MEM_PERCENTAGE>
    Sets the maximum memory limit (in percentage) for sunny-cp solving process.
    By default, this value is set to 100%, since the memory check can be pretty
    resource consuming: it is suggested to set a value lower than 100 only if
    you are sure that the solving process can be very memory consuming.
  -l <BOUND>
    Sets a lower bound for the problem to be solved (for COPs only). This is
    equivalent of adding the constraint f(x) >= <BOUND> where f(x) is the
    objective function of the problem.
  -u <BOUND>
    Sets an upper bound for the problem to be solved (for COPs only). This is
    equivalent of adding the constraint f(x) <= <BOUND> where f(x) is the
    objective function of the problem.

Solvers Options
===============
  --check-solvers <UNT_1>,<TRU_1>,...,<UNT_k>,<TRU_k>
    Checks the outcome of k "untrusted" solvers UNT_i by means of k "trusted"
    solvers TRU_i for i = 1, ..., k. In particular:
    - if the outcome of UNT_i is =====UNBOUNDED===== or ====UNSATISFIABLE=====
      then the outcome is ignored and nothing is printed;
    - if UNT_i produces a solution, sunny-cp exploits its FlatZinc output for
      checking such solution by using TRU_i. If an inconsistency is detected,
      UNT_i is killed. Otherwise, the solution is printed;
    - If UNT_i proves the optimality, then the optimal solution is checked as
      described above. However, line ========== is never printed (even when the
      solution is sound);
    - In all the other cases (including failures of TRU_i) we assume that UNT_i
      gives a correct answer, and thus the corresponding solution is printed.
    Note that checked solutions can be partial, since the variable assignments
    considered in the solution check are all and only those printed by UNT_i
    on standard output. So, the solution check also depends on the output
    annotations defined by the user in the MiniZinc model. This option clearly
    introduces an overhead in the solving process, especially if UNT_i produces
    a lot of sub-optimal solutions or TRU_i is not performant.
    *** NOTE ***: This option, unset by default, only works with MiniZinc 2.x.
    While UNT_i must be different from TRU_i, it is however possible to have
    UNT_i = UNT_j or TRU_i = TRU_j for some distinct indexes i,j in {1, ..., k}
  --wait-time <TIME>
    Don't stop a running solver if it produced a solution in the last <TIME>
    seconds. By default, <TIME> is 2 seconds. Also the constant +inf is allowed
  --wait-time-<SOLVER> <TIME>
    Don't stop <SOLVER> if it produced a solution in the last <TIME> seconds
  --restart-time <TIME>
    Restart a constituent solver if its best solution is obsolete and it did
    not produced any solution in the last <TIME> seconds.
    By default, <TIME> is 5 seconds. Also the constant +inf is allowed.
  --restart-time-<SOLVER> <TIME>
    Restart <SOLVER> if its best solution is obsolete and it did not produced a
    solution in the last <TIME> seconds
  --max-restarts <MAX>
    Sets the maximum number of times a solver can be restarted. After <MAX>
    restarts, the solver is killed rather than being restarted for the
    (<MAX> + 1)-th time.
    By default, <MAX> = +inf
  --max-restarts-<SOLVER>
    As above, with the difference that the option is set only for <SOLVER_NAME>
    and not for all the solvers of the portfolio.
  --kill-idle
    Kills a solver instead of restarting it again if it has produced no solution
    and has already been restarted at least once. Unset by default.
  --mzn-output
    Annotate the raw FlatZinc solution stream with solver-specific .ozn files
    so that it can be translated by solns2out.

Helper Options
==============
  -h, --help
    Print this message
  -d <PATH>
    Absolute path of the folder in which the temporary files created by the
    solver will be put. The default directory is tmp, and by default such files
    are deleted after sunny-cp execution
  --keep
    Do not erase the temporary files created by the solver and stored in the
    specified directory (useful for debugging). This option is unset by default
  --csp-<OPTION> <VALUE>
    Allows to set the specific option only if the input problem is a CSP. Note
    that the '-' character of <OPTION> must be omitted. E.g., --csp-T 900 sets
    the T parameter to 900 only if the problem is a CSP, while such option
    is ignored if the problem is a COP.
  --cop-<OPTION> <VALUE>
    Allows to set the specific option only if the input problem is a COP. Note
    that the '-' character of <OPTION> must be omitted. E.g., --cop-T 900 sets
    the T parameter to 900 only if the problem is a COP, while such option
    is ignored if the problem is a COP.
'''

import os
import sys
import getopt
from socket import gethostname
from defaults import *
from features import *
from problem import *
from pfolio_solvers import *

def parse_arguments(args):
    """
    Parse the options specified by the user and returns the corresponding
    arguments properly set.
    """

    # Get the arguments and parse the input model to get solve information.
    n = os.cpu_count()    
    mzn, dzn, opts = get_args(args)
    pfolio = DEF_PFOLIO
    solve = get_solve(mzn)

    # Initialize variables with the default values.
    k = DEF_K
    check = DEF_CHECK
    timeout = DEF_TOUT
    backup = DEF_BACKUP
    static = DEF_STATIC
    extractor = DEF_EXTRACTOR
    cores = DEF_CORES
    tmp_dir = DEF_TMP_DIR
    keep = DEF_KEEP
    verbose = DEF_VERBOSE
    mem_limit = DEF_MEM_LIMIT
    all_opt = DEF_ALL
    free_opt = DEF_FREE
    kill_idle = DEF_KILL_IDLE
    lb = DEF_LB
    ub = DEF_UB
    mzn_output = DEF_MZN_OUTPUT
    solver_options = dict((s, {
        'wait_time': DEF_WAIT_TIME,
        'restart_time': DEF_RESTART_TIME,
        'max_restarts': DEF_RESTARTS
    }) for s in ALL_SOLVERS)
    if solve == 'sat':
        kb = DEF_KB_CSP
        lims = DEF_LIMS_CSP
    else:
        kb = DEF_KB_COP
        lims = DEF_LIMS_COP

    # Arguments parsing.
    for o, a in opts:
        if o in ('-h', '--help'):
            print(__doc__)
            sys.exit(0)
        elif o == '-P':
            pfolio = a.split(',')
            if not pfolio:
                print('Error! Empty portfolio ', file=sys.stderr)
                print('For help use --help', file=sys.stderr)
                sys.exit(2)
        elif o == '-A':
            solvers = a.split(',')
            pfolio += [s for s in solvers if s not in pfolio]
        elif o == '-R':
            solvers = a.split(',')
            pfolio = [s for s in pfolio if s not in solvers]
        elif o == '-p':
            n = int(a)
            if n < 1:
                print('Warning: -p parameter set to 1.', file=sys.stderr)
                cores = 1
            else:
                cores = n
        elif o == '-e':
            extractor = a
        elif o == '-k':
            k = int(a)
            if k < 0:
                print('Error! Negative value ' + a +
                      ' for k value.\nFor help use --help', file=sys.stderr)
                sys.exit(2)
        elif o == '-T':
            timeout = float(a)
            if timeout <= 0:
                print('Error! Non-positive value ' + a +
                      ' for timeout.\nFor help use --help', file=sys.stderr)
                sys.exit(2)
        elif o == '-b':
            backup = a
        elif o == '-K':
            if not os.path.exists(a):
                print('Error! Directory ' + a +
                      ' not exists.\nFor help use --help', file=sys.stderr)
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
            kb = path + name + '_' + pb
            lims = path + name + '_lims_' + pb
            if not os.path.exists(kb):
                print('Error! File ' + kb + ' not exists.', file=sys.stderr)
                print('For help use --help', file=sys.stderr)
                sys.exit(2)
            if not os.path.exists(lims):
                print('Error! File ' + lims + ' not exists.', file=sys.stderr)
                print('For help use --help', file=sys.stderr)
                sys.exit(2)
        elif o == '-s':
            s = a.split(',')
            for i in range(0, len(s) // 2):
                solver = s[2 * i]
                time = float(s[2 * i + 1])
                if time < 0:
                    print('Error! Not acceptable negative time',
                          file=sys.stderr)
                    print('For help use --help', file=sys.stderr)
                    sys.exit(2)
                static.append((solver, time))
        elif o == '-d':
            if not os.path.exists(a):
                print('Error! Directory ' + a + ' not exists.',
                      file=sys.stderr)
                print('For help use --help', file=sys.stderr)
                sys.exit(2)
            name = [token for token in a.split('/') if token][-1]
            if a[-1] == '/':
                tmp_dir = a[0:-1]
            else:
                tmp_dir = a
        elif o == '-m':
            mem_limit = float(a)
        elif o == '-a':
            all_opt = True
        elif o == '-f':
            free_opt = True
        elif o == '--kill-idle':
            kill_idle = True
        elif o == '-l' and solve != 'sat':
            lb = int(a)
        elif o == '-u' and solve != 'sat':
            ub = int(a)
        elif o.startswith('--wait-time'):
            wait_time = float(a)
            if wait_time < 0:
                print('Error! Not acceptable negative time', file=sys.stderr)
                print('For help use --help', file=sys.stderr)
                sys.exit(2)
            if len(o) > 11:
                solver = o[12:]
                solver_options[solver]['wait_time'] = wait_time
            else:
                for item in list(solver_options.values()):
                    item['wait_time'] = wait_time
        elif o.startswith('--restart-time'):
            rest_time = float(a)
            if rest_time < 0:
                print('Error! Not acceptable negative time', file=sys.stderr)
                print('For help use --help', file=sys.stderr)
                sys.exit(2)
            if len(o) > 14:
                solver = o[15:]
                solver_options[solver]['restart_time'] = rest_time
            else:
                for item in list(solver_options.values()):
                    item['restart_time'] = rest_time
        elif o.startswith('--max-restarts'):
            if len(o) > 14:
                solver = o[15:]
                solver_options[solver]['max_restarts'] = int(a)
            else:
                for item in list(solver_options.values()):
                    item['max_restarts'] = int(a)
        elif o == '--mzn-output':
            mzn_output = True
        elif o == '--keep':
            keep = True
        if o in ('-v', '--verbose'):
            verbose = True
        elif o == '--check-solvers':
            s = a.split(',')
            for i in range(0, len(s) // 2):
                unt = s[2 * i]
                tru = s[2 * i + 1]
                if unt == tru:
                    print('Error! A solver is either trusted or untrusted!',
                          file=sys.stderr)
                    print('For help use --help', file=sys.stderr)
                    sys.exit(2)
                check[unt] = tru
        elif o.startswith('--csp-') and solve == 'sat' \
          or o.startswith('--cop-') and solve != 'sat':
            if len(o) == 7:
                opts.append(['-' + o[6], a])
            else:
                opts.append(['--' + o[6:], a])
    
    problem = Problem(mzn, dzn, solve)
    tmp_id = tmp_dir + '/' + gethostname() + '_' + str(os.getpid())
    return problem, k, timeout, pfolio, backup, kb, lims, static, extractor, \
        cores, solver_options, tmp_id, mem_limit, keep, all_opt, free_opt, \
        lb, ub, check, kill_idle, verbose, mzn_output


def get_args(args):
    """
    Get the input arguments.
    """
    dzn = ''
    try:
        options = [
            'P', 'R', 'A', 'T', 'k', 'b', 'K', 's', 'd', 'p', 'e', 'm', 'l',
            'u'
        ]
        long_options = [
            'fzn-options', 'wait-time', 'restart-time', 'max-restarts'
        ]
        long_options += [
            o + '-' + s for o in long_options for s in ALL_SOLVERS
        ]
        long_options += ['check-solvers']
        csp_opts = ['csp-' + o + '=' for o in options + long_options] + \
            ['csp-a'] + ['csp-f']
        cop_opts = ['cop-' + o + '=' for o in options + long_options] + \
            ['cop-a'] + ['cop-f']
        long_options = [o + '=' for o in long_options]
        long_noval = ['help', 'keep', 'mzn', 'kill-idle', 'verbose', 'mzn-output']
        long_noval += ['csp-' + o for o in long_noval]
        long_noval += ['cop-' + o for o in long_noval]
        long_options += long_noval + csp_opts + cop_opts
        opts, args = getopt.getopt(
            args, 'hvafT:k:b:K:s:d:p:e:x:m:l:u:P:R:A:', long_options
        )
    except getopt.error as msg:
        print(msg)
        print('For help use --help', file=sys.stderr)
        sys.exit(2)

    if len(args) == 0:
        for o, a in opts:
            if o in ('-h', '--help'):
                print(__doc__)
                sys.exit(0)
        print('Error! No arguments given.', file=sys.stderr)
        print('For help use --help', file=sys.stderr)
        sys.exit(2)
    mzn = args[0]
    if not mzn.endswith('.mzn'):
        print('Error! MiniZinc input model must have .mzn extension.\n'
              'For help use --help', file=sys.stderr)
        sys.exit(2)
    if len(args) > 1:
        dzn = args[1]
    return mzn, dzn, opts


def get_solve(mzn):
    """
    Return 'sat', 'min', or 'max' for satisfaction, minimization, or
    maximization problems respectively.
    """
    solve = 'sat'
    include_list = [mzn]
    mzn_dir = os.path.dirname(mzn)

    # Loop for extracting the solve item.
    while include_list:
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
            for c in line:
                # Ignore comments.
                if ignore or c == '%':
                    ignore = True
                    if c == '\n':
                        ignore = False
                else:
                    new_line += c
            tokens = new_line.split()
            for token in tokens:
                if token == 'include' or token == 'include"':
                    include = True
                # Looking for included models.
                if include and token[-1] == '"' or token[-1] == '";':
                    include = token.replace('include"', '').replace('"', '') \
                        .replace("'", '')
                    include_list.append(include)
                    include = False
                elif token.endswith('satisfy'):
                    include_list = []
                    break
                elif token in ['minimize', 'maximize']:
                    solve = 'min' if token == 'minimize' else 'max'
                    include_list = []
                    break
    return solve
