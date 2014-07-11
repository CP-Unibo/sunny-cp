"""
Module for computing the static schedule of COPs.
"""

import sys
import csv
from gurobipy import *

def main(args):
  path = os.environ['SUNNY_HOME'] + '/kb/all/schedules' 
  reader = csv.reader(open(path, 'r'), delimiter = '|')
  y = []
  C = 180
  times = range(1, C + 1)
  solvers = {
    'chuffed':   0, 'g12cpx': 0, 'g12fd'    : 0, 
    'g12lazyfd': 0, 'gecode': 0, 'minisatid': 0
  }
  y = {}
  x = {}
  l = {}
  nabla = {}
  y_to_name = {}
  x_to_name = {}
  model_name = 'whole_dataset'
  print 'Building model ' + model_name + '...'
  model = Model(model_name)
  #model.setParam('OutputFlag', False)
  n = 0
  not_solved = {}
  
  print 'Adding Variables...'
  for s in solvers:
    x[s] = {}
    for t in times:
      x_name = 'x_' + s + '_' + str(t)
      x[s][t] = model.addVar(vtype = GRB.BINARY, name = x_name)
      x_to_name[x_name] = (s, t)
  for row in reader:
    n += 1
    p = row[0]
    y_name = 'y_' + str(n)
    y[p] = model.addVar(vtype = GRB.BINARY, name = y_name)
    y_to_name[y_name] = p
    l[p] = int(row[1]) - 1
    schedule = row[2].split()[0 : -2]
    base = []
    for i in range(0, l[p]):
      base.append((schedule[2 * i], float(schedule[2 * i + 1])))
    nabla[p] = [x[s][t_i] for (s, t) in base for t_i in range(int(t), C + 1)]
    not_solved[p] = schedule
  print 'Updating the Model...'
  model.update()
  
  print 'Adding Constraints and Objective Function...'
  for (p, y_p) in y.items():
    lp_yp = LinExpr(l[p], y_p)
    model.addConstr(y_p + quicksum(nabla[p]) >= 1)
  x_term = [LinExpr(t, x[s][t]) for s in solvers for t in times]
  model.addConstr(quicksum(x_term) <= C)
  obj = [LinExpr(C + 1, y_p) for y_p in y.values()]
  obj.extend(x_term)
  model.setObjective(quicksum(obj), GRB.MINIMIZE)
  model.optimize()

  solutions = model.getVars()
  tot_time = 0.0
  not_solv = 0.0
  schedule = []
  for sol in solutions:
    if round(sol.x) == 1:
      if sol.varName[0] == 'x':
	(s, t) = x_to_name[sol.varName]
	print '--- Solver',s,'has to be run for',t,'seconds'
	schedule.append((s, t))
	tot_time += t
      else:
	inst = y_to_name[sol.varName]
	#print inst, not_solved[inst]
	not_solv += 1
  print 'Total time allocated:',tot_time
  print 'Instances not covered:',not_solv,'/',n,'(',not_solv/n*100,'%)'
  model.write('model.lp')
  print 'Resulting Schedule:',sorted(schedule, key = lambda x : x[1])
  
if __name__ == '__main__':
    main(sys.argv[1:])
