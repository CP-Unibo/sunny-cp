"""
Facilities for generating all the subsets of a given set of elements.
The following code draws inspiration from:
http://visualstudiomagazine.com/articles/2012/08/01/biginteger-data-type.aspx
"""

def binom(n, k):
  """ 
  Computes the binomial coefficient "n choose k" 
  """
  if n < 0 or k < 0:
    raise Exception("Error: Negative argument in binomial coefficient!")
  if n < k:
    return 0
  if n == k: 
    return 1
  if k == 0:
    return 1
  if k < n - k:
    delta = n - k 
    iMax = k
  else:
    delta = k 
    iMax = n - k
  ans = delta + 1
  for i in range(2, iMax + 1):
    ans = (ans * (delta + i)) / i
  return ans

def largestV(a, b, x):
  """ 
  Helper function for 
  get_subset
  """
  v = a - 1
  while (binom(v, b) > x):
    v -= 1
  return v

def get_subset(h, k, elements):
  """ 
  Returns the (h+1)-th element, w.r.t. the lexicographic ordering,
  among all the subsets of elements having cardinality k.
  """
  n = len(elements)
  maxM = binom(n, k) - 1
  ans = [0] * k
  a = n
  b = k
  # x is the "dual" of h.
  x = maxM - h 
  for i in range(0, k):
    ans[i] = largestV(a, b, x)    
    x = x - binom(ans[i], b)
    a = ans[i]
    b = b - 1
  for i in range(0, k):
    ans[i] = elements[(n - 1) - ans[i]];
  return ans

'''
# Testing.
from time import clock
elements = [
  'S_1', 'S_2', 'S_3', 'S_4', 'S_5', 'S_6', 
  'S_7', 'S_8', 'S_9', 'S_10', 'S_11', 'S_12'
]
n = len(elements)
start = clock()
i = 0
for k in range(2, n):
  for h in range(0, binom(n, k)):
    s = get_subset(h, k, elements)
    print s
    i += 1
elapsed = (clock() - start)
print "Computed", i, "subsets of", elements, "in", elapsed, "seconds"
'''