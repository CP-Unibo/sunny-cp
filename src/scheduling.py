'''
Module for computing and parallelizing the solvers schedule of SUNNY algorithm.
'''

import csv
from math import sqrt
from combinations import *
from multiprocessing import cpu_count

def sunny(pb, pfolio, backup, feat_vector, k, timeout, kb, size = cpu_count()):
  '''
  Returns the sequential schedule computed by SUNNY algorithm.
  '''
  reader = csv.reader(open(kb, 'r'), delimiter = '|')
  infos = {}
  feat_vectors = {}
  for row in reader:
    inst = row[0]
    feat_vectors[inst] = eval(row[1])
    infos[inst] = eval(row[2])
  neighbours = find_neighbours(feat_vector, feat_vectors, k)
  
  if pb.isCSP():
    return sunny_csp(neighbours, infos, k, timeout, pfolio, backup, size)
  else:
    return sunny_cop(neighbours, infos, k, timeout, pfolio, backup, size)

def find_neighbours(fv, feat_vectors, k):
  """
  Returns the k instances of feat_vectors closer to fv.
  """
  distances = []
  for (inst, vect) in feat_vectors.items():
    distance = compare_instances(fv, vect)
    distances.append((distance, inst))
  distances.sort(key = lambda x : x[0])
  return [i for (d, i) in distances[:k]]  
  
def compare_instances(fv1, fv2):
  """
  Computes the Euclidean distance between two instances.
  """
  distance = 0.0
  for i in range(0, len(fv1)):
    d = fv1[i] - fv2[i]
    distance += d * d
  return sqrt(distance)

def sunny_csp(neighbours, infos, k, timeout, pfolio, backup, size):
  """
  Given the neighborhood of a given CSP and the runtime infos, returns the 
  corresponding SUNNY schedule.
  """
  solved = {}
  times  = {}
  for solver in pfolio:
    solved[solver] = set([])
    times[solver]  = 0.0
  for inst in neighbours:
    for solver in pfolio:
      time = infos[inst][solver]['time']
      if time < timeout:
        solved[solver].add(inst)
      times[solver] += time
  max_solved = 0
  min_time = 1000000
  best_pfolio = []
  m = len(pfolio)
  # Select the best sub-portfolio. size is the minimum cardinality.
  for i in range(size, m + 1):
    for j in range(0, binom(m, i)):
      solved_instances = set([])
      solving_time = 0
      # get the (j + 1)-th subset of cardinality i
      sub_pfolio = get_subset(j, i, pfolio)
      for solver in sub_pfolio:
        solved_instances.update(solved[solver])
        solving_time += times[solver]
      num_solved = len(solved_instances)
      if num_solved >  max_solved or \
        (num_solved == max_solved and solving_time < min_time):
          min_time = solving_time
          max_solved = num_solved
          best_pfolio = sub_pfolio
  # n is the number of instances solved by each solver plus the instances 
  # that no solver can solver.
  n = sum([len(solved[s]) for s in best_pfolio]) + (k - max_solved)
  schedule = {}
  # Compute the schedule and sort it by number of solved instances.
  for solver in best_pfolio:
    ns = len(solved[solver])
    if ns == 0 or round(timeout / n * ns) == 0:
      continue
    schedule[solver] = timeout / n * ns
  tot_time = sum(schedule.values())
  # Allocate to the backup solver the (eventual) remaining time.
  if round(tot_time) < timeout:
    if backup in schedule.keys():
      schedule[backup] += timeout - tot_time
    else:
      schedule[backup]  = timeout - tot_time
  sorted_schedule = sorted(
    schedule.items(), 
    key = lambda x: times[x[0]]
  )
  assert(round(sum(t for (s, t) in sorted_schedule)) <= timeout)
  return sorted_schedule

def sunny_cop(neighbours, infos, k, timeout, pfolio, backup, size):
  """
  Given the neighborhood of a given COP and the runtime infos, returns the 
  corresponding SUNNY schedule.
  """
  scores = {}
  times  = {}
  areas  = {}
  
  for solver in pfolio:
    scores[solver] = []
    times[solver] = 0.0
    areas[solver] = 0.0
  for inst in neighbours:
    for solver in pfolio:
      scores[solver].append(infos[inst][solver]['score']) 
      times[solver] += infos[inst][solver]['time']
      areas[solver] += infos[inst][solver]['area']
  max_score = 0
  min_time = 1000000000
  min_area = 1000000000
  best_pfolio = []
  # Select the best sub-portfolio.
  m = len(pfolio)
  for i in range(size, m + 1):
    for j in range(0, binom(m, i)):
      score = 0
      time = 0
      area = 0
      # get the (j + 1)-th subset of cardinality i
      sub_pfolio = get_subset(j, i, pfolio)
      port_scores = dict([
        (s, l) for s, l in scores.items() if s in sub_pfolio
      ])
      for h in range(0, k):
	score += max([inst[h] for inst in port_scores.values()])
      time = sum([times[solver] for solver in sub_pfolio])
      area = sum([areas[solver] for solver in sub_pfolio])
      if score >  max_score or \
        (score == max_score and time < min_time) or \
        (score == max_score and time == min_time and area < min_area):
          min_time  = time
          min_area  = area
          max_score = score
          best_pfolio = sub_pfolio
  # n is the number of instances solved by each solver plus the instances 
  # that no solver can solver.
  n = sum([sum(scores[s]) for s in best_pfolio]) + (k - max_score)
  schedule = {}
  # compute the schedule and sort it by number of solved instances.
  for solver in best_pfolio:
    ns = sum(scores[solver])
    if ns == 0 or round(timeout / n * ns) == 0:
      continue
    schedule[solver] = timeout / n * ns
  tot_time = sum(schedule.values())
  if round(tot_time) < timeout:
    if backup in schedule.keys():
      schedule[backup] += timeout - tot_time
    else:
      schedule[backup]  = timeout - tot_time
  sorted_schedule = sorted(
    [(s, t) for (s, t) in schedule.items()],
    key = lambda x: times[x[0]]
  )
  return sorted_schedule

def parallelize(static_sched, dynamic_sched, cores, timeout):
  '''
  Returns a parallel schedule of the solvers.
  '''
  par_schedule = []
  for i in range(0, cores - 1):
    if not dynamic_sched:
      break
    par_schedule.append((dynamic_sched.pop(0)[0], timeout))
  
  last_time = timeout
  while static_sched:
    #if dynamic_sched and static_sched[-1][0] == dynamic_sched[0][0]:
      #new_time = static_sched[-1][1] + dynamic_sched[0][1]
      #static_sched[-1] = (static_sched[-1][0], new_time)
      #dynamic_sched.pop(0)
    #while static_sched:
      (s, t) = static_sched.pop(0)
      par_schedule.append((s, t))
      last_time -= t
      
  dyn_time = sum(t for (s, t) in dynamic_sched)
  if last_time and dyn_time:
    while dynamic_sched:
      (s, t) = dynamic_sched.pop(0)
      new_time = t * last_time / dyn_time
      par_schedule.append((s, new_time))
  
  assert not static_sched and not dynamic_sched
  return par_schedule