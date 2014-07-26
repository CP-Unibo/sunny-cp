"""
From info and features files computes a corresponding knowledge base and the 
limits of each feature (i.e. the min/max value for each feature).
"""

import json
import csv
import copy
from math import isnan
from os import environ

prefix = environ['SUNNY_HOME'] + '/kb/'
suffix = 'csp'
kb = 'mznc'
infos_file = prefix + kb + '/infos_' + suffix + '_' + kb
feat_file  = prefix + 'all/features_' + suffix + '_all'
kb_file    = prefix + kb + '/kb_'       + suffix + '_' + kb
lim_file   = prefix + kb + '/lims_'     + suffix + '_' + kb
LB      = -1
UB      =  1
DEF_VAL = -1
with open(infos_file, 'r') as infile:
  infos = json.load(infile)
feat_reader = csv.reader(open(feat_file, 'r'), delimiter = '|')

'''
Associate to each problem the corrisponding features vector and compute the 
min/max value for every feature.
'''
print 'Computing features limits'
features = {}
lims = {}
n = 0
for row in feat_reader:
  inst = row[0]
  if inst not in infos.keys() or \
  (kb == 'all' and ('mznc12' in inst or 'mznc13' in inst)):
    continue
  feat_dict = eval(row[2])
  nan = float('nan')
  fv = [v for (k, v) in sorted(feat_dict.items())]
  if n == 0:
    n = len(fv)
    for i in range(0, n):
      if isnan(fv[i]):
        fv[i] = DEF_VAL
      lims[i] = [fv[i], fv[i]]
  else:
    assert n == len(fv)
    for i in range(0, n):
      if isnan(fv[i]):
        fv[i] = DEF_VAL
      if fv[i] < lims[i][0]:
        lims[i][0] = fv[i]
      if fv[i] > lims[i][1]:
        lims[i][1] = fv[i]
  features[inst] = fv

for i in range(0, n):
  if lims[i][0] == lims[i][1]:
    # Ignore constant features.
    lims[i] = None 

print 'Limits computed, scaling values and adding infos...'
print 'Size of non-filtered features space:',n
writer = csv.writer(open(kb_file, 'w'), delimiter = '|')
inf = float('inf')
for (inst, feat_vect) in features.items():
  new_feat = []
  for i in range(0, n):
    if not lims[i]:
      continue
    min_val = lims[i][0]
    max_val = lims[i][1]
    if feat_vect[i] == -inf:
      new_val = LB
    elif feat_vect[i] == inf:
      new_val = UB
    else:
      new_val = (UB - LB) * (feat_vect[i] - min_val) / (max_val - min_val) + LB
    assert LB <= new_val <= UB
    new_feat.append(new_val)
  # Adding runtime infos for the given problem.
  pb_infos = {} 
  for solver in infos[inst].keys():
    pb_infos[solver] = {}
    if suffix == 'cop':
      pb_infos[solver]['area']  = infos[inst][solver]['area']
      pb_infos[solver]['score'] = infos[inst][solver]['score']
      pb_infos[solver]['otime'] = infos[inst][solver]['otime']
    else:
      pb_infos[solver]['info'] = infos[inst][solver]['info']
      pb_infos[solver]['time'] = infos[inst][solver]['tot_time']
  writer.writerow([inst, new_feat, pb_infos])
print 'Size of filtered features space:',len([x for x in lims.values() if x])
with open(lim_file, 'w') as outfile:
  json.dump(lims, outfile)
