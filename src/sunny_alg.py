"""
Module for computing the solvers schedule of SUNNY algorithm on a given problem,
differentiating between CSPs and COPs.
"""

import json
import csv
from math import sqrt, isnan
from combinations import *

def get_schedule(feat_vector, k, T, pfolio, backup, kb, lims, obj, static = []):
  """
  Returns the schedule of solvers computed by SUNNY algorithm.
  """
  with open(lims, 'r') as infile:
    l = json.load(infile)
  feat_norm = normalize_features(feat_vector, l)
  
  reader = csv.reader(open(kb, 'r'), delimiter = '|')
  feat_vectors = {}
  infos = {}
  for row in reader:
    inst = row[0]
    feat_vectors[inst] = eval(row[1])
    infos[inst] = eval(row[2])
  neighbours = find_neighbours(feat_norm, feat_vectors, k)
  
  if obj == 'sat':
    return csp_schedule(neighbours, infos, k, T, pfolio, backup)
  else:
    return cop_schedule(neighbours, infos, k, T, pfolio, backup, static)

def normalize_features(feat_vector, lims, lb = -1, ub = 1, def_value = -1):
  """
  Given a features vector, it returns a normalized one in which constant 
  features are removed and features values are scaled in [lb, ub] by 
  exploiting the information already computed in lims dictionary.
  """
  norm_vector = []
  for i in range(0, len(feat_vector)):
    j = str(i)
    if lims[j]:
      val = float(feat_vector[i])
      if isnan(val):
        val = def_value
      min_val = float(lims[j][0])
      max_val = float(lims[j][1])
      if val <= min_val:
        norm_val = lb
      elif val >= max_val:
        norm_val = ub
      else:
        x = (val - min_val) / (max_val - min_val)
        norm_val = (ub - lb) * x + lb
        assert lb <= norm_val <= ub
      norm_vector.append(norm_val)
  return norm_vector

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
  
def csp_schedule(neighborhood, infos, k, T, pfolio, backup):
  """
  Given the neighborhood of a given CSP and the runtime infos, returns the 
  corresponding SUNNY schedule.
  """
  solved = {}
  times  = {}
  for solver in pfolio:
    solved[solver] = set([])
    times[solver]  = 0.0
  for inst in neighborhood:
    for solver in pfolio:
      time = infos[inst][solver]['time']
      if time < T:
        solved[solver].add(inst)
      times[solver] += time
  max_solved = 0
  min_time = 1000000
  best_pfolio = []
  m = len(pfolio)
  # Select the best sub-portfolio.
  for i in range(0, m + 1):
    for j in range(0, binom(m, i)):
      solved_instances = set([])
      solving_time = 0
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
    if ns == 0 or round(T / n * ns) == 0:
      continue
    schedule[solver] = T / n * ns
  tot_time = sum(schedule.values())
  # Allocate to the backup solver the (eventual) remaining time.
  if round(tot_time) < T:
    if backup in schedule.keys():
      schedule[backup] += T - tot_time
    else:
      schedule[backup]  = T - tot_time
  sorted_schedule = sorted(
    schedule.items(), 
    key = lambda x: times[x[0]]
  )
  assert(round(sum(t for (s,t) in sorted_schedule)) <= T)
  return sorted_schedule
  
def cop_schedule(neighborhood, infos, k, T, pfolio, backup, static):
  """
  Given the neighborhood of a given COP and the runtime infos, returns the 
  corresponding SUNNY schedule.
  """
  scores = {}
  times  = {}
  areas  = {}
  T -= sum(t for (s, t) in static)
  
  for solver in pfolio:
    scores[solver] = []
    times[solver] = 0.0
    areas[solver] = 0.0
  for inst in neighborhood:
    for solver in pfolio:
      scores[solver].append(infos[inst][solver]['score']) 
      times[solver] += infos[inst][solver]['otime']
      areas[solver] += infos[inst][solver]['area']
  max_score = 0
  min_time = 1000000000
  min_area = 1000000000
  best_pfolio = []
  # Select the best sub-portfolio.
  m = len(pfolio)
  for i in range(1, m + 1):
    for j in range(0, binom(m, i)):
      score = 0
      time = 0
      area = 0
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
    if ns == 0 or round(T / n * ns) == 0:
      continue
    schedule[solver] = T / n * ns
  tot_time = sum(schedule.values())
  if round(tot_time) < T:
    if backup in schedule.keys():
      schedule[backup] += T - tot_time
    else:
      schedule[backup]  = T - tot_time
  sorted_schedule = sorted(
    [(s, t) for (s, t) in schedule.items()],
    key = lambda x: times[x[0]]
  )
  # Merge static and dynamic schedule if last solver of static corresponds to 
  # first solver of the dynamic schedule.
  if static and static[-1][0] == sorted_schedule[0][0]:
    solver = static[-1][0]
    time = static[-1][1] + sorted_schedule[0][1]
    return static[0 : len(static) - 1] + \
           [(solver, time)]            + \
           sorted_schedule[1 : len(sorted_schedule)]
  else:
    return static + sorted_schedule
