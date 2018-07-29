'''
Problem is the abstraction of a MiniZinc model to be solved by sunny-cp.
'''

class Problem:
  """
  Abstraction of a MiniZinc Model.
  """

  # Absolute path of the MiniZinc model of the problem.
  mzn_path = ''

  # Absolute path of the data of the problem.
  dzn_path = ''

  # Absolute path of the output file.
  ozn_path = ''

  # Can be either 'sat', 'min', or 'max' for satisfaction, minimization, or
  # maximization problems respectively.
  solve = ''

  # Best known objective function value for this problem.
  best_bound = None

  # Name of the solver that found the best bound for this problem.
  best_solver = ''

  def isCSP(self):
    """
    Returns True if the problem is a satisfaction problem, False otherwise.
    """
    return self.solve == 'sat'

  def isCOP(self):
    """
    Returns True if the problem is an optimization problem, False otherwise.
    """
    return self.solve in ['min', 'max']

  def has_bound(self):
    """
    Returns True iff an objective bound is known for this problem.
    """
    return float("-inf") < self.best_bound < float("+inf")

  def bound_better_than(self, bound):
    """
    Returns True iff the current best bound is better than the specified bound.
    """
    return self.isCOP() and self.has_bound() and (
      self.solve == 'min' and self.best_bound < bound or \
      self.solve == 'max' and self.best_bound > bound
    )

  def bound_worse_than(self, bound):
    """
    Returns True iff the current best bound is worse than the specified bound:
    this means that the current best bound should be updated.
    """
    return self.isCOP() and bound is not None and (
      self.solve == 'min' and self.best_bound > bound or \
      self.solve == 'max' and self.best_bound < bound
    )

  def __init__(self, mzn_path, dzn_path, ozn_path, solve):
    """
    Class Constructor.
    """
    self.mzn_path = mzn_path
    self.dzn_path = dzn_path
    self.ozn_path = ozn_path
    assert solve in ['sat', 'min', 'max']
    self.solve = solve
    if solve == 'min':
      self.best_bound = float('+inf')
    else:
      self.best_bound = float('-inf')
