'''
Solver is the abstraction of a constituent solver of the portfolio. Each solver
must be an object of class Solver.

RunningSolver is instead a solver running on a given FlatZinc model.
'''


import psutil


class Solver:
    """
    Solver is the abstraction of a solver instance.
    """
    # Id. of the solver, used as argument for the --solver MiniZinc parameter.
    solver_id = ''
    # Id. defining a particular version of the solver.
    version_id = ''
    # String representation of the solver, returned by __str__ method.
    name = ''
    # String of additional options for solving the FlatZinc instance.
    solv_opts = ''
    # String of additional options for the conversion MiniZinc->FlatZinc.
    conv_opts = ''
    # How many threads the solver uses.
    n_threads = -1
    # How the solver translates constraint LHS < RHS into FlatZinc.
    constraint = ''

    # Status of the solving process. It can be either:
    #         'ready': solver is ready to convert a MiniZinc model
    #     'mzn2fzn': solver is converting a MiniZinc model into a FlatZinc
    #    'flatzinc': solver is solving the FlatZinc instance
    # The status is preserved even when a solver process is suspended.
    status = ''

    # Don't stop solver if it has produced a solution in the last wait_time s.
    wait_time = -1

    # Restart solver if its best solution is obsolete and it has not produced a
    # solution in the last restart_time sec.
    restart_time = -1

    # Timeout in seconds of the solving process.
    timeout = -1

    # Time in seconds (since the epoch) when the solving process started.
    start_time = -1

    # Time in seconds (since the epoch) when the solver found last solution.
    solution_time = -1

    # Absolute path of the FlatZinc model on which solver is run.
    fzn_path = ''

    # Flag for printing all the solutions.
    all_opt = ''

    # Flag for ignoring all the search annotations.
    free_opt = ''

    # Dictionary (variable,value) of the best solution found by solver.
    solution = {}

    # Can be either 'sat', 'min', or 'max' for satisfaction, minimization, or
    # maximization problems respectively.
    solve = ''

    # Objective variable of the FlatZinc model.
    obj_var = ''

    # Best objective value found by solver.
    obj_value = None

    # Object of class psutil.Popen referring to the solving process.
    process = None

    # True iff the value of obj_var is annotated with "output_var".
    output_var = True

    # Number of times solver has been restarted.
    num_restarts = -1

    # Maximum number of solver restarts allowed.
    max_restarts = -1

    def __init__(self):
        pass

    def __init__(
        self, solver_info, solve, fzn_path, all_opt, free_opt, wait_time,
        restart_time, timeout, max_restarts, obj_var = ''
    ):
        self.name = solver_info['name']
        self.n_threads = solver_info['n_threads']
        self.conv_opts = solver_info['conv_opts']
        self.solv_opts = solver_info['solv_opts']
        self.solver_id = solver_info['solver_id']
        self.version_id = solver_info['version_id']
        self.constraint = solver_info['constraint']
        
        self.solve = solve
        self.fzn_path = fzn_path
        self.all_opt = all_opt
        self.free_opt = free_opt
        self.wait_time = wait_time
        self.restart_time = restart_time
        self.timeout = timeout
        self.max_restarts = max_restarts
        
        self.status = 'ready'
        self.num_restarts = 0
        if obj_var:
            self.obj_var = obj_var
        if solve == 'min':
            self.obj_value = float('+inf')
        elif solve == 'max':
            self.obj_value = float('-inf')
        
       
    def mem_percent(self):
        """
        Returns the memory usage (in percent) of the solver process.
        """
        m = self.process.memory_percent()
        for p in self.process.children(recursive=True):
            try:
                m += p.memory_percent()
            except psutil.NoSuchProcess:
                pass
        return m

    def mzn2fzn_cmd(self, pb):
        """
        Returns the command for converting a given MiniZinc model to FlatZinc
        by using solver-specific redefinitions.
        """
        return (f'minizinc -c --output-ozn-to-file {pb.ozn_path} --solver ' + 
                f"{self.solver_id} {self.conv_opts} " + 
                f'{pb.mzn_path} {pb.dzn_path} -o {self.fzn_path}').split()

    def flatzinc_cmd(self, pb):
        """
        Returns the command for executing the FlatZinc model.
        """
        return (f"minizinc --solver {self.solver_id} " +
                f"{self.solv_opts} {self.all_opt} {self.free_opt} " +
                f'{self.fzn_path}').split()

    def set_obj_var(self, problem, lb, ub):
        """
        Retrieve and set the name of the obj. variable in the FlatZinc model,
        possibly adding the "output_var" annotation to obj_var declaration.
        """
        lines = []
        with open(self.fzn_path, 'r') as infile:
            for line in reversed(infile.readlines()):
                line = line.strip()
                if not line or line.startswith('%'):
                    continue
                tokens = line.replace('::', ' ').replace(';', '').split()
                if 'solve' in tokens:
                    self.obj_var = tokens[-1].replace(';', '')
                    cons = ''
                    if lb > float('-inf'):
                        cons += self.constraint.replace('RHS', self.obj_var)\
                                               .replace('LHS', str(lb - 1)) + ';\n'
                    if ub < float('+inf'):
                        cons += self.constraint.replace('LHS', self.obj_var)\
                                               .replace('RHS', str(ub + 1)) + ';\n'
                    line = cons + line
                if tokens[0] == 'var' and self.obj_var in tokens and \
                   'output_var' not in tokens and '=' not in tokens:
                    self.output_var = False
                    line = line.replace(';', '') + ' :: output_var;\n'
                lines.append(line + '\n')
            infile.close()
        with open(self.fzn_path, 'w') as outfile:
            outfile.writelines(reversed(lines))

    def inject_bound(self, bound):
        """
        Injects a new bound to the FlatZinc model.
        """
        if self.solve == 'min':
            cons = self.constraint.replace('LHS', self.obj_var) \
                                  .replace('RHS', str(bound))
        elif self.solve == 'max':
            cons = self.constraint.replace('RHS', self.obj_var) \
                                  .replace('LHS', str(bound))
        else:
            return
        lines = []
        with open(self.fzn_path, 'r') as infile:
            add = True
            for line in infile.readlines():
                if add and 'constraint' in line.split(';')[0]:
                    lines.append(cons + ';\n')
                    add = False
                lines.append(line)
        with open(self.fzn_path, 'w') as outfile:
            outfile.writelines(lines)
        self.obj_value = bound
