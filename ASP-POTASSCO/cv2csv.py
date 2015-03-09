import csv

# Name of the scenario.
SCENARIO = 'ASP-POTASSCO'
# No. of repetitions.
REPS = 1
# No. of folds.
FOLDS = 10
# Default value for missing features.
DEF_FEAT_VALUE = -1
# Solving timeout (seconds)
TIMEOUT = 600

for i in range(1, REPS + 1):
  for j in range(1, FOLDS + 1):
    path = 'cv/rep_' + str(i) + '_fold_' + str(j) + '/'
    
    # Creating ASP-POTASSCO.feat
    reader = csv.reader(
      open(path + 'train_feature_values.arff'), delimiter = ','
    )
    writer = csv.writer(open(path + SCENARIO + '.feat', 'w'), delimiter = '|')
    for row in reader:
      feats = []
      for f in row[1]:
	if f == '?':
	  f = DEF_FEAT_VALUE
	else:
	  # Features should be not negative.
	  assert float(f) >= 0
	feats.append(f)
      writer.writerow([row[0], row[1]])
    
    # Creating ASP-POTASSCO.info
    reader = csv.reader(
      open(path + 'train_algorithm_runs.arff'), delimiter = ','
    )
    writer = csv.writer(open(path + SCENARIO + '.info', 'w'), delimiter = '|')
    goal = 'sat'
    val = 'nan'
    values = {}
    for row in reader:
      inst = row[0]
      solver = row[2]
      info = row[4]
      if info != 'ok':
	# Problem not solved.
	answer = 'unk'
	time = TIMEOUT
      else:
	# We assume the problem satisfiable if runstatus = ok.
	answer = 'sat'
	time = float(row[3])
      writer.writerow([inst, solver, goal, answer, time, val, values])
    
     
    
    
      