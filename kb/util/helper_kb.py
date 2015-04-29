'''
Helper functions for creating a knowledge base.
'''

import os
import csv
import sys
import json
  
def compute_infos(
  info_file, timeout, lb_score, ub_score, lb_area, ub_area, check
):
  """
  Computes the runtime information for the CSP/COP knowledge bases.
  """
  print 'Processing runtime infos...'
  reader = csv.reader(open(info_file, 'r'), delimiter = '|')
  kb_csp = {}
  kb_cop = {}
  min_val = {}
  max_val = {}
  min_values = {}
  max_values = {}
  nan = float('nan')
  for row in reader:
    inst = row[0]
    solv = row[1]
    goal = row[2]
    info = row[3]
    time = float(row[4])
    val = float(row[5])
    values = dict((float(t), v) for (t, v) in eval(row[6]).items())
    
    if check:
      check_invariant(
        'info = unk \/ (goal != sat /\ info = sat) <==> time = T',
        info == 'unk' or goal != 'sat' and info == 'sat',
        time == timeout,
        inst,
        solv
      )
      check_invariant(
        'goal = sat \/ info = unk \/ info = uns <==> val = nan',
        goal == 'sat' or info in ['unk', 'uns'],
        val != val,
        inst,
        solv
      )
      last_val = [v for (t, v) in values.items() if t == max(values.keys())]
      check_invariant(
        't_i < T AND v_k = val AND (values = {} <==> val = nan)',
        True,
        not [t for t in values.keys() if t > timeout] and \
        (not last_val or last_val[0] == val)           and \
        (not values or val == val) and (values or val != val),
        inst,
        solv
      )
    
    if goal != 'sat':
      if inst not in kb_cop.keys():
        kb_cop[inst] = {}
        min_val[inst] = float('+inf')
        max_val[inst] = float('-inf')
        min_values[inst] = float('+inf')
        max_values[inst] = float('-inf')
      kb_cop[inst][solv] = {
        'goal': goal, 'info': info, 'time': time, 'val': val, 'values': values
      }
      if val == val:
        if val < min_val[inst]:
          min_val[inst] = val
        if val > max_val[inst]:
          max_val[inst] = val
      if values:
        vals = values.values()
        if min(vals) < min_values[inst]:
          min_values[inst] = min(vals)
        if max(vals) > max_values[inst]:
          max_values[inst] = max(vals)
    else:
      if inst not in kb_csp.keys():
        kb_csp[inst] = {}
      kb_csp[inst][solv] = {'info': info, 'time': time}
  
  if kb_cop:
    print 'Computing solving score and area...'
    for inst, item in kb_cop.items():
      for solver in item.keys():
        values = item[solver]['values']
        info   = item[solver]['info']
        goal   = item[solver]['goal']
        val    = item[solver]['val']
        time   = item[solver]['time']
        item[solver]['score'] = get_score(
          info, val, lb_score, ub_score, min_val[inst], max_val[inst], goal, 
          check
        )
        #print inst, solver
        item[solver]['area'] = get_area(
          info, lb_area, ub_area, min_values[inst], max_values[inst], goal, 
          time, timeout, values, check
        )
        del item[solver]['values']
        del item[solver]['info']
        del item[solver]['goal']
        del item[solver]['val']
  
  return kb_csp, kb_cop

def check_invariant(inv, a, b, inst, solv):
  """
  Checks if the property inv: a <==> b holds for instance inst and solver solv.
  """
  if (a and not b) or (b and not a):
    print 'Error! Invariant',inv,'violated by solver',solv,'on instance',inst
    raise Exception('Violated invariant.')

def get_score(info, val, lb, ub, min_val, max_val, goal, check):
  """
  Returns the solving score
  """
  if info == 'unk':
    return 0
  elif info in ['opt', 'uns']:
    return 1
  if min_val == max_val:
    return ub
  s = (ub - lb) * (val - min_val) / (max_val - min_val)
  if check:
    assert 0 <= round(s, 5) <= ub - lb
  if goal == 'min':
    return ub - s
  else:
    return lb + s

def get_area(
  info, lb, ub, min_val, max_val, goal, time, timeout, values, check
):
  """
  Returns the solving area.
  """
  if info == 'unk':
    return timeout
  if info in ['uns', 'unb']:
    return time
  scaled_vals = sorted([
    (t, scale(v, lb, ub, min_val, max_val, goal)) for (t, v) in values.items()
  ])
  n = len(scaled_vals) - 1
  a = scaled_vals[0][0]
  #print a, 
  for i in range(0, n):
    a += scaled_vals[i][1] * (scaled_vals[i + 1][0] - scaled_vals[i][0])
  if info == 'opt':
    t = time
  else:
    t = timeout
  a += scaled_vals[n][1] * (t - scaled_vals[n][0])
  if check:
    assert t >= scaled_vals[n][0]
    assert 0 <= round(a, 5) <= timeout
  return a

def scale(val, lb, ub, min_val, max_val, goal):
  if min_val == max_val:
    return lb
  if goal == 'min':
    s = lb + (ub - lb) * (val - min_val) / (max_val - min_val)
  else:
    s = lb + (ub - lb) * (max_val - val) / (max_val - min_val)
  assert lb <= s <= ub
  return s

def make_kb(kb_path, kb_name, feat_file, lb, ub, scale, const, kb_csp, kb_cop):
  print 'Processing features...'
  reader = csv.reader(open(feat_file, 'r'), delimiter = '|')
  os.mkdir(kb_path)
  print 'Created the knowledge base folder:',kb_path
  csp_writer = csv.writer(
    open(kb_path + '/' + kb_name  + '_csp', 'w'), delimiter = '|'
  )
  cop_writer = csv.writer(
    open(kb_path + '/' + kb_name  + '_cop', 'w'), delimiter = '|'
  )
  features = {}
  lims_csp = {}
  lims_cop = {}
  insts_csp = kb_csp.keys()
  insts_cop = kb_cop.keys()
  for row in reader:
    inst = row[0]
    feat_vector = eval(row[1])
    if inst in insts_csp:
      writer = csp_writer
      info = kb_csp[inst]
      lims = lims_csp
    else:
      writer = cop_writer
      info = kb_cop[inst]
      lims = lims_cop
    if not scale and not const:
      kb_row = [inst, feat_vector]
      kb_row.append(info)
      writer.writerow(kb_row)
      continue
      
    if not lims:
      for i in range(0, len(feat_vector)):
        lims[i] = [feat_vector[i], feat_vector[i]]
    else:
      for i in range(0, len(feat_vector)):
        if feat_vector[i] < lims[i][0]:
          lims[i][0] = feat_vector[i]
        elif feat_vector[i] > lims[i][1]:
          lims[i][1] = feat_vector[i]
    
    features[inst] = feat_vector
  
  if scale or const:
    for (inst, feat_vector) in features.items():
      new_feat_vector = []
      if inst in insts_csp:
        info = kb_csp[inst]
        lims = lims_csp
        writer = csp_writer
      else:
        info = kb_cop[inst]
        lims = lims_cop
        writer = cop_writer
      for i in range(0, len(feat_vector)):
        if const and lims[i][0] == lims[i][1]:
           # Constant feature.
           continue
        if scale:
          min_val = lims[i][0]
          max_val = lims[i][1]
          if min_val == max_val:
            # Don't remove constant features but scale values. 
            new_val = lb
          else:
            # Remove constants and scale.
            x = (feat_vector[i] - min_val) / (max_val - min_val)
            new_val = lb + (ub - lb) * x
          assert lb <= new_val <= ub
        else:
          # Remove constants but don't scale.
          new_val = feat_vector[i]
        new_feat_vector.append(new_val)
      kb_row = [inst, new_feat_vector, info]
      writer.writerow(kb_row)
  else:
    print 'Features processed!'
    return
  
  for i in ['csp', 'cop']:
    lim_file = kb_path + '/' + kb_name + '_lims_' + i
    with open(lim_file, 'w') as outfile:
      json.dump(eval('lims_' + i), outfile)
  print 'Features processed,',
  if const and scale:
    print 'scaled all values, and removed constant features!'
  elif const:
    print 'and removed constant features!'
  else:
    print 'and scaled all values!'
