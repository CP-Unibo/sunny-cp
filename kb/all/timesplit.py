"""
Computes the ideal timesplit solvers given a dataset of COPs.
"""

import os
import sys
import json
import csv
from math import ceil, floor

BACKUP_SOLVER = 'g12cpx'
TIMEOUT       = 1800.0
MIN_SHIFT     = 5
MIN_TIME      = 1
MAX_SOLV      = float("inf")
path          = os.environ['SUNNY_HOME'] + '/kb/all'
info_file     = path + '/infos_cop_all'
sched_file    = path + '/schedules'
sched_writer  = csv.writer(open(sched_file, 'w'), delimiter = '|')
with open(info_file, 'r') as infile:
  infos = json.load(infile)

def best_solver(inst, solvers):
  rank = [
    (1 - infos[inst][s]['score'], 
    infos[inst][s]['otime'],
    infos[inst][s]['area'],
    s)
    for s in solvers
  ]
  return min(rank)[3]
  
def get_shift(inst, solver, solvers, split_time):
  item = infos[inst]
  beh = [
    (float(t), v)
    for (t, v) in item[solver]['norm'].items() 
    if float(t) <= split_time
  ]
  res_shift = [0, 0, None]
  for (t, v) in beh:
    for s1 in set(solvers) - set([solver]):
      for (t1, v1) in item[s1]['norm'].items():
	t1 = float(t1)
	if t1 == 0.0:
	  t1 = 1.0
        if t1 < t and v1 <= v:
          shift = [t - t1, t1, s1]
          if shift[0] > res_shift[0]:
            res_shift = shift
  return res_shift

def time_split(inst, solvers, timeout = TIMEOUT, backup = BACKUP_SOLVER,
               min_shift = MIN_SHIFT, min_time = MIN_TIME, max_solv = MAX_SOLV):
  s2 = best_solver(inst, solvers)
  best = s2
  if not s2:
    return (backup, [[backup, timeout]])
  shifts = []
  schedule = [[s2, timeout]]
  tot_shift  = 0
  split_time = timeout
  max_shift  = timeout
  num_solv   = 1
  while max_shift >= min_shift and num_solv < max_solv:
    max_shift = min_shift - 1
    tf = float(infos[inst][s2]['fzn_time'])
    shift = get_shift(inst, s2, solvers, split_time)
    delta = shift[0]
    time  = shift[1]  
    tm = schedule[0][1] - delta - time - tf
    delta -= tf
    if delta > max_shift and min([time, tm]) >= min_time:
      max_shift    = delta
      split_time   = time
      split_solver = shift[2]
      schedule[0][1] -= max_shift + split_time
      schedule.insert(0, [split_solver, split_time])
      tot_shift += max_shift
      num_solv  += 1
      s2 = split_solver
  schedule[len(schedule) - 1][1] += tot_shift
  return (best, schedule)

def main(args):
  sorted_items = sorted(infos.items())
  for (inst, item) in sorted_items:
    (best, schedule) = time_split(inst, item.keys())
    if len(schedule) > 1:
      row = [inst, len(schedule)]
      timesplit = ''
      for [solver, time] in schedule:
	timesplit += solver + ' ' + str(int(ceil(time))) + ' '
      row.extend([timesplit, ])
      sched_writer.writerow(row)
    
if __name__ == '__main__':
    main(sys.argv[1:])
