'''
Module for defining a feature extractor that computes the feature vector of a
problem. A feature extractor is simply a class that implements the static method
extract_features(args) to return the feature vector.
The default extractor is mzn2feat, but the user can define its own extractor by
simply implementing a corresponding new class (see example below).

Actually using a static class is no more powerful than using only functions.
This is done for keeping all the auxiliary functions in the same class and for
possible future extensions.
'''

from math import isnan
from subprocess import PIPE
import os
import json
import psutil

class mzn2feat:

  @staticmethod
  def extract_features(args):
    problem = args[0]
    not_norm_vector = mzn2feat.extract(problem)
    if not not_norm_vector:
      return None
    lims_file = args[1]

    with open(lims_file, 'r') as infile:
      lims = json.load(infile)
    return mzn2feat.normalize(not_norm_vector, lims)

  @staticmethod
  def extract(problem):
    """
    Extracts the features from a MiniZinc model by exploiting the mzn2feat
    features extractor.
    """
    mzn_path = problem.mzn_path
    dzn_path = problem.dzn_path
    cmd = 'mzn2feat -i ' + mzn_path
    if dzn_path:
      cmd += ' -d ' + dzn_path
    proc = psutil.Popen(cmd.split(), stdout = PIPE)
    (out, err) = proc.communicate()
    # Failure in features extraction.
    if proc.returncode != 0:
      return []
    features = out.split(",")
    feat_vector = [
      float(features[i]) for i in range(0, len(features))
    ]
    return feat_vector

  @staticmethod
  def normalize(feat_vector, lims, lb = -1, ub = 1, def_value = -1):
    """
    Given a feature vector, it returns a normalized one in which constant
    features are removed and feature values are scaled in [lb, ub] by
    exploiting the information already computed in lims dictionary.
    """
    norm_vector = []
    for i in range(0, len(feat_vector)):
      j = str(i)
      if lims[j][0] != lims[j][1]:
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

'''
# Example.
class new_extractor:

  @staticmethod
  def extract_features(args):
    #args parsing and processing
    ...
    return feature_vector
'''
