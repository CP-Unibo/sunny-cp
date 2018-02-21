"""
This program is an utility to dipatch jobs remotely and build the files to create a KB.

The request file is a csv file with | as separator having the following columns:
- mzn file,
- dzn file if available,
- solvers to use (comma separated list)

It can be created also by running the command create_request_list
"""

import logging
import json
import datetime
import requests
import sqlite3
import os
import hashlib
import Queue
from threading import Thread
import sys
import time

import click

QUEUE = Queue.Queue()
MZN_ID = 0
DZN_ID = 1
SOL_ID = 2
OPTIONS_ID = 3

# sleep time in seconds after an http request
SLEEP_TIME = 1
SLEEP_TIME_AFTER_ERROR = 60

# requests timeout
REQUESTS_TIMEOUT = 3610


@click.group()
@click.option('--log-level',
              help='Log level (DEBUG, INFO, WARNING, ERROR or CRITICAL)',
              type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
              default="DEBUG")
def cli(log_level):
    # Configure logging
    logging.basicConfig(format="[%(asctime)s][%(levelname)s][%(name)s]%(message)s",
                        level=log_level)

################################
# Utility functions
################################

def get_hash_id(mzn_file,dzn_file):
    '''
    Computes the hash to be used as id for the instance
    '''
    h = hashlib.sha256()
    with open(mzn_file) as f:
        h.update(f.read())
    if dzn_file:
        with open(dzn_file) as f:
            h.update(f.read())
    id = h.hexdigest()
    return id

################################
# Get the list
################################

def get_mzn_dzn_pairs(dir_name):
    dirs = [os.path.join(dir_name,f) for f in os.listdir(dir_name) if os.path.isdir(os.path.join(dir_name,f))]
    mzn = [os.path.join(dir_name,f) for f in os.listdir(dir_name) if f.endswith(".mzn") and "/." not in f]
    dzn = [os.path.join(dir_name,f) for f in os.listdir(dir_name) if f.endswith(".dzn") and "/." not in f]

    ls = []
    for d in dirs:
        ls += get_mzn_dzn_pairs(d)

    if not mzn:
        if not dirs:
            logging.warning("In directory {} found {} mzn files and {} dzn files. Skipping directory".format(
                dir_name,len(mzn),len(dzn)))
        return ls
    if not dzn:
        return ls + [(x,"") for x in mzn]
    return ls + [(x,y) for x in mzn for y in dzn]

@click.command()
@click.option('--request-file',
              help='CSV containing the job to dispatch',
              type=click.Path(exists=False, file_okay=True, dir_okay=False, writable=True, readable=True,
                              resolve_path=True),
              default="requests.csv")
@click.option('--problems-dir',
              help='The directory containing the files to add in the request list',
              type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=False, readable=True,
                              resolve_path=True),
              default="./")
@click.option('--solver','-s',multiple=True,
              help='Solver to use',
              default=[])
@click.option('--database-file',
              help='Sqlite database file, if any, to avoid repeating experiments.',
              multiple=True,
              type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=False, readable=True,
                              resolve_path=True),
              default=[])
@click.option('--extra-options',
              help='Extra options for calling sunny, comma separated. E.g., -P=gecode,-a=',
              default="")
def create_request_list(
        request_file,
        problems_dir,
        solver,
        database_file,
        extra_options
        ):
    '''
    Create the request list using mzn, dzn files in a directory.
    '''
    if len(database_file) > 1:
        logging.error("Only one database is supported. Exiting")
        sys.exit(1)

    logging.info("Solvers to use: {}".format(",".join(solver)))

    mzn_dzn_pair = get_mzn_dzn_pairs(problems_dir)
    logging.info("Retrieved {} problems to solve".format(len(mzn_dzn_pair)))

    if database_file:
        logging.info("Computing the hash functions of the instances")
        maps_id_pair = {get_hash_id(x,y):(x,y) for (x,y) in mzn_dzn_pair}
        maps_pair_id = {maps_id_pair[x]:x for x in maps_id_pair}
        logging.info("Using the hash function {} unique problems to solve were found".format(len(maps_id_pair)))

        connection = sqlite3.connect(database_file[0])
        cursor = connection.cursor()
        with open(request_file,'wb') as f:
            for (x,y,z) in [(x,y,z) for z in solver for (x,y) in maps_pair_id]:
                cursor.execute("SELECT count(*) FROM results WHERE id = ? AND solvers= ?", (maps_pair_id[(x,y)],z))
                data = cursor.fetchone()[0]
                if data == 0:
                    f.write("{}|{}|{}|{}\n".format(x, y, z, extra_options))
                else:
                    logging.warning("Solver {} already used to solve problem {}".format(z,[x,y]))
        connection.close()

    else:
        with open(request_file,'wb') as f:
            for (x,y,z) in [(x,y,z) for z in solver for (x,y) in mzn_dzn_pair]:
                f.write("{}|{}|{}|{}\n".format(x,y,z,extra_options))

cli.add_command(create_request_list)


################################
# Get results running sunny remotely
################################


def parse_solver_output(output):
    '''
    Parses the output of the output of sunny into a json object
    '''
    result = {}
    optimization_problem = False
    result["result"] = "unk" # alternative values: sat,uns,opt
    result["solutions"] = {} # stores the solutions
    result["time"] = -1 # stores the final time of the algorithm when terminated before the timeout
    obj_val = -1
    time = -1
    try:
        for line in output.split("\n"):
            if line.startswith("% Current Best Bound: "):
                optimization_problem = True
                obj_val = int(line[len("% Current Best Bound: "):])
            elif line.startswith("% Current Solution Time: "):
                time = float(line[len("% Current Solution Time: "):])
            elif line.startswith("----------"):
                result["result"] = "sat"
                if optimization_problem:
                    result["solutions"][time] = obj_val
                else:
                    result["solutions"][time] = 0
                    result["time"] = time
            elif line.startswith("=========="):
                if optimization_problem:
                    result["result"] = "opt"
            elif line.startswith("=====UNSATISFIABLE====="):
                result["result"] = "uns"
            elif line.startswith("=====UNBOUNDED====="):
                result["result"] = "unb"
            elif line.startswith("=====UNKNOWN====="):
                result["result"] = "unk"
            elif line.startswith("% Search completed at time: "):
                result["time"] = float(line[len("% Search completed at time: "):])
        return result
    except ValueError as e:
        return {"error": unicode(e)}


def worker(thread_num,database_file,timeout,url,hostname):
    '''
    Sends jobs to the server, collects answers, parse them and update the DB
    '''
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    while not QUEUE.empty():
        try:
            item = QUEUE.get()
            try:
                logging.debug("Thread {} process request {}".format(thread_num, item))
                if os.path.isfile(item[MZN_ID]) and item[SOL_ID] and (not item[DZN_ID] or os.path.isfile(item[DZN_ID])):
                    id = get_hash_id(item[MZN_ID], item[DZN_ID] if item[DZN_ID] else "")
                    logging.debug("The hash of the files is {}".format(id))

                    # check if id is already in the DB or otherwise compute its feature vector
                    cursor.execute("SELECT count(*) FROM instances WHERE id = ?", (id,))
                    data = cursor.fetchone()[0]
                    if data == 0:
                        logging.debug("Instance {} not found in the DB".format(id))
                        files = {'mzn': open(item[MZN_ID], 'rb')}
                        if item[DZN_ID]:
                            files['dzn'] = open(item[DZN_ID], 'rb')
                        logging.debug("Thread {} sending request".format(thread_num))
                        response = requests.post(url + "/get_features", files=files,
                                                 headers={'host': hostname} if hostname else {},
                                                 timeout=REQUESTS_TIMEOUT
                                                 )
                        time.sleep(SLEEP_TIME)
                        logging.debug("Thread {} received answer with code {}.".format(thread_num, response.status_code))
                        # handle error in the answer
                        if response.status_code != requests.codes.ok:
                            logging.error("Error {}. Thread {}. Feature vector request ended up with error {}, response {}.".format(
                                item, thread_num, response.status_code, response.text))
                            time.sleep(SLEEP_TIME_AFTER_ERROR)
                            continue
                        # parse the answer
                        try:
                            feature_vector = [float(x) for x in response.text.replace("nan","1").split(",")]
                            # the s_goal is the feature having index 59
                            s_goal = feature_vector[59]
                            logging.debug("Obtained feature vector {}".format(feature_vector))
                        except ValueError:
                            logging.error(
                                "Error {}. Thread {}. Feature vector response {} can not be parsed.".format(
                                    item, thread_num, response.text))
                            time.sleep(SLEEP_TIME_AFTER_ERROR)
                            continue
                        # compute the type of the problem
                        goal = "sat"
                        if s_goal == 2:
                            goal = "min"
                        elif s_goal == 3:
                            goal = "max"
                        logging.debug("Update the DB with instance having id {}".format(id))
                        cursor.execute("INSERT or REPLACE INTO instances(id,mzn,dzn,type,features,date) VALUES" +
                                       "(?,?,?,?,?,?)", (
                                           id,
                                           item[MZN_ID],
                                           item[DZN_ID] if item[DZN_ID] else "",
                                           goal,
                                           unicode(feature_vector),
                                           datetime.datetime.now()))
                        connection.commit()
                    else:
                        cursor.execute("SELECT type FROM instances WHERE id = ?", (id,))
                        goal = cursor.fetchone()[0]

                    # try to solve the problem remotely
                    files = {'mzn': open(item[MZN_ID], 'rb'),
                             '-P': item[SOL_ID],
                             '-T': unicode(timeout)}
                    if item[DZN_ID]:
                        files['dzn'] = open(item[DZN_ID], 'rb')
                    if goal != "sat":
                        files['-a'] = ""
                    if item[OPTIONS_ID]:
                        ls = [x.split("=") for x in OPTIONS_ID.split(",")]
                        ls_errors = [ x for x in ls if len(x) != 2]
                        if ls_errors:
                            logging.warning("Ignoring options {} for instance {}".format(ls_errors,item))
                        for option in [x for x in ls if len(x) == 2]:
                            files[option[0]] = option[1]

                    logging.debug("Thread {} sending request".format(thread_num))
                    response = requests.post(url + "/process", files=files,
                                             headers={'host': hostname} if hostname else {},
                                             timeout=REQUESTS_TIMEOUT)
                    time.sleep(SLEEP_TIME)
                    logging.debug("Thread {} received answer with code {}.".format(thread_num,response.status_code))
                    if response.status_code != requests.codes.ok:
                        logging.error("Error {}. Thread {}. Ended up with error {}, response {}.".format(
                            item, thread_num, response.status_code, response.text))
                    else:
                        # parse the response
                        json_result = parse_solver_output(response.text)
                        if "error" in json_result:
                            logging.error("Error {}. Thread {}. Wrong parse of answer {} in response <<<<< {} >>>>>".format(
                                item, thread_num, json_result["error"],response.text
                            ))
                        else:
                            logging.debug("Parsed solution into json object {}".format(json.dumps(json_result)))
                            logging.debug("Update the DB for item {}".format(item))
                            cursor.execute("INSERT or REPLACE INTO results(id,solvers,timeout,date,output) VALUES (?,?,?,?,?)", (
                                id,
                                item[SOL_ID],
                                timeout,
                                datetime.datetime.now(),
                                json.dumps(json_result)))
                            connection.commit()
                            logging.info("OK {}|{}".format(item,id))
                else:
                    logging.error("ERROR {}. Thread {}. Request not well formed".format(item, thread_num, item[DZN_ID]))
            except requests.exceptions.RequestException as e:
                logging.critical("Error {}. Thread {}. Connection request exception {}. Time {}".format(
                    item, thread_num, e))
                time.sleep(SLEEP_TIME_AFTER_ERROR)
            except requests.exceptions.ConnectionError as e:
                logging.error("Error {}. Thread {}. Connection error {}. Time {}".format(
                    item, thread_num, e))
                time.sleep(SLEEP_TIME_AFTER_ERROR)
            finally:
                QUEUE.task_done()
        except Queue.Empty:
            # Handle empty queue here
            break

    connection.close()
    logging.info("Thread {} terminated".format(thread_num))



@click.command()
@click.option('--server-url',
              help='Server URL address',
              default='http://localhost')
@click.option('--server-port',
              help='Server IP port',
              default='80')
@click.option('--server-host',
              help='Custom header host if needed',
              default='')
@click.option('--database-file',
              help='Sqlite database file',
              type=click.Path(exists=False, file_okay=True, dir_okay=False, writable=True, readable=True,
                              resolve_path=True),
              default='sunny_db.db')
@click.option('--parallel-requests',
              help='Number of parallel request to make',
              default=1)
@click.option('--timeout',
              help='Timeout to use for running the solver',
              default=1800)
@click.option('--request-file',
              help='CSV containing the job to dispatch',
              type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True, readable=True,
                              resolve_path=True),
              default="requests.csv")
def send_jobs(server_url,
         server_port,
         server_host,
         parallel_requests,
         request_file,
         database_file,
         timeout):
    '''
    Solve the instances remotely and update the DB
    '''

    # Open database
    if os.path.exists(database_file):
        logging.info("Database file {} found".format(database_file))
    else:
        connection = sqlite3.connect(database_file)
        cursor = connection.cursor()
        logging.info("Create db schema in {}".format(database_file))
        sql_command = '''CREATE TABLE results (
        id TEXT,
        solvers TEXT,
        timeout INTEGER,
        date DATE,
        output TEXT,
        PRIMARY KEY ( id, solvers ) );'''
        cursor.execute(sql_command)
        sql_command = '''CREATE TABLE instances (
                id TEXT PRIMARY KEY,
                mzn TEXT,
                dzn TEXT,
                type TEXT,
                features TEXT,
                date DATE);'''
        cursor.execute(sql_command)
        connection.commit()
        connection.close()

    # Read the requests
    lines = []
    with open(request_file) as f:
        row_lines = f.readlines()
        for line in row_lines:
            if line.strip():
                lines.append(line.replace("\n","").split('|'))
                if len(lines[-1]) != 4:
                    logging.critical("The line {} of the request file {} is not formatted correctly".format(
                        line.strip(),request_file))
                    sys.exit(1)

    logging.info("Read {} requests from file {}".format(len(lines),request_file))

    # Add jobs in the queue
    for line in lines:
        QUEUE.put(line)

    for i in range(parallel_requests):
        worker_thread = Thread(target=worker, args=(i, database_file, timeout,
                                                    server_url + ":" + server_port,server_host))
        worker_thread.daemon = True
        worker_thread.start()

    QUEUE.join()
    logging.info("Execution terminated.")
cli.add_command(send_jobs)


################################
# Generate the input files for creating the KB
################################
@click.command()
@click.option('--database-file',
              help='Sqlite database file',
              type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True, readable=True,
                              resolve_path=True),
              default='sunny_db.db')
@click.option('--feature-file',
              help='Feature file to generate',
              type=click.Path(exists=False, file_okay=True, dir_okay=False, writable=True, readable=True,
                              resolve_path=True),
              default='feature_file.csv')
@click.option('--info-file',
              help='Info file to generate',
              type=click.Path(exists=False, file_okay=True, dir_okay=False, writable=True, readable=True,
                              resolve_path=True),
              default='info_file.csv')
@click.option('--timeout',
              help='The timeout of the KB',
              default=1800)
def generate_kb_files(
        database_file,
        info_file,
        feature_file,
        timeout):
    '''
    Export the database into sunny KB input
    '''

    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    instance_type = {}
    used_instances = set([])
    for row in cursor.execute("SELECT id,features,type FROM instances", ()):
        instance_type[row[0]] = row[2]
    logging.info("Processed {} instances".format(len(instance_type)))

    logging.info("Start to create the info_file")
    with open(info_file, 'wb') as f:
        for (id,solvers,timeout_inst,output) in cursor.execute("SELECT id,solvers,timeout,output FROM results", ()):
            # instance id not found in table
            if id not in instance_type:
                logging.warning("Id {} not found. Result ignored".format(id))
                continue
            result = json.loads(output)

            # timeout too low
            if timeout > timeout_inst and (result["time"] <=0 or result["time"] > timeout):
                logging.warning("Timeout {} for instance {} and solvers {} is not enough. Ignored".format(
                    timeout_inst,id,solvers))
                continue

            # solver ended up in error
            if result["result"] == "unk" and result["time"] > 0:
                logging.warning("Erronous execution for instance {} and solvers {}. Ignored".format(
                    id,solvers))
                continue

            # timeout too big
            if result["time"] > timeout or result["time"] <= 0:
                result["time"] = timeout
                if instance_type[id] == "sat":
                    result["result"] = "unk"
                else: # min or max problem
                    result["solutions"] = {float(i):result["solutions"][i] for i in result["solutions"]
                                           if float(i) < timeout}
                    if result["result"] == "uns":
                        result["result"] = "unk"
                    elif result["result"] == "opt" or result["result"] == "sat":
                        if result["solutions"]:
                            result["result"] = "sat"
                        else:
                            result["result"] = "unk"
            # update time and solutions
            if instance_type[id] == "sat":
                result["solutions"] = {}

            # compute the val value with invariant goal = sat \/ info = unk \/ info = uns <==> val = nan
            result["val"] = "nan"
            if result["solutions"]:
                if instance_type[id] == "min":
                    result["val"] = unicode(min(result["solutions"].values()))
                elif instance_type[id] == "max":
                    result["val"] = unicode(max(result["solutions"].values()))

            # discard the results where result is unknown
            if result["result"] == "unk":
                continue

            # stucture: inst|solver|goal|answer|time|val|values
            f.write("{}|{}|{}|{}|{}|{}|{}\n".format(
                id,
                solvers,
                instance_type[id],
                result["result"],
                result["time"],
                result["val"],
                json.dumps(result["solutions"]).replace('"','')
            ))
            used_instances.add(id)

    logging.info("Start to create the feature_file")
    instance_type = {}
    with open(feature_file,'wb') as f:
        for row in cursor.execute("SELECT id,features,type FROM instances", ()):
            if row[0] in used_instances:
                # structure: inst|[f_1, ..., f_n]
                f.write("{}|{}\n".format(row[0],row[1]))



    connection.close()
    logging.info("To generate the KB directory test_kb locally run 'python $SUNNY_HOME/kb/util/csv2kb.py -p . test_kb {} {}'".format(feature_file,info_file))
cli.add_command(generate_kb_files)

################################
# Check the KB for anomalies and solver errors
################################
@click.command()
@click.option('--database-file',
              help='Sqlite database file',
              type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True, readable=True,
                              resolve_path=True),
              default='sunny_db.db')
def check_anomalies(
        database_file,
        ):
    """
    Check for possible anomalies in the results
    """
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    # get all the results
    results = {}
    for row in cursor.execute("SELECT id,solvers,output FROM results", ()):
        if row[0] not in results:
            results[row[0]] = {}
        results[row[0]][row[1]] = json.loads(row[2])

    instances = {}
    for row in cursor.execute("SELECT id,mzn,dzn,type FROM instances", ()):
        instances[row[0]] = (row[1:])

    # list all errors (the ones where the solver terminated before the timeout) or unb
    for i in results:
        for j in results[i]:
            if results[i][j]["result"] == "unb":
                logging.info("UNBOUND: instance {}, solver {}".format(instances[i],j))
            elif results[i][j]["result"] == "unk" and results[i][j]["time"] > 0:
                logging.info("SOLVER ERROR: instance {}, solver {} terminated with unk before the timeout".format(instances[i][0:2], j))

    # opt value is consistent
    possible_erroneous_solvers = set([])
    for i in results:
        if instances[i][2] == "sat":
            sat = [j for j in results[i] if results[i][j]["result"] == "sat"]
            unsat = [j for j in results[i] if results[i][j]["result"] == "uns"]
            if sat and unsat:
                logging.info("SAT-UNSAT inconsistency: instance {}, sat {}, unsat {}".format(instances[i][0:2],sat,unsat))
                if len(sat) > len(unsat):
                    logging.info("Possible culprits {}".format(unsat))
                    possible_erroneous_solvers.update(unsat)
                elif len(sat) < len(unsat):
                    logging.info("Possible culprits {}".format(sat))
                    possible_erroneous_solvers.update(sat)
                else:
                    if not(set(sat).issubset(possible_erroneous_solvers) or set(unsat).issubset(possible_erroneous_solvers)):
                        logging.info("Impossible to automatically detect culprits. Manual intervention needed.")
        else: # min or max problems
            best_values = {}
            for j in results[i]:
                if results[i][j]["solutions"]:
                    if instances[i][2] == "min":
                        best_values[j] = min(results[i][j]["solutions"].values())
                    else:
                        best_values[j] = max(results[i][j]["solutions"].values())
            op_values = set()
            op_values.update([best_values[j] for j in best_values if results[i][j]["result"] == "opt"])
            if len(op_values) > 1:
                logging.info("TWO OPTIMA: instance {}, values {}".format(
                    instances[i][0:2],{x: best_values[x] for x in best_values if results[i][x]["result"] == "opt"}))
                culprit_dict = {x: [y for y in best_values if results[i][y]["result"] == "opt" and best_values[y] == x]
                                for x in op_values}
                culprit_list = sorted([(len(culprit_dict[x]),x) for x in culprit_dict])
                set_A = set(culprit_dict[culprit_list[0][1]])
                set_B = set(culprit_dict[culprit_list[1][1]])
                if culprit_list[0][0] < culprit_list[1][0]:
                    logging.info("Possible culprits {}".format(set_A))
                    possible_erroneous_solvers.update(set_A)
                else:
                    if not (set_A.issubset(possible_erroneous_solvers) or set_B.issubset(possible_erroneous_solvers)):
                        logging.info("Impossible to automatically detect culprits. Manual intervention needed.")
            op_values = set()
            op_values.update([best_values[j] for j in best_values if results[i][j]["result"] == "opt" and
                              j not in possible_erroneous_solvers])
            if op_values:
                if instances[i][2] == "min" and min(op_values) > min(best_values.values()):
                    logging.info("MIN less than OPTIMA: instance {}, optima {}, values {}".format(
                        instances[i][0:2], min(op_values),
                        {x: best_values[x] for x in best_values if best_values[x] < min(op_values)}))
                    possible_erroneous_solvers.update([x for x in best_values if best_values[x] < min(op_values)])
                elif instances[i][2] == "max" and max(op_values) > max(best_values.values()):
                    logging.info("MAX greater than OPTIMA: instance {}, optima {}, values {}".format(
                        instances[i][0:2], min(op_values),
                        {x: best_values[x] for x in best_values if best_values[x] > max(op_values)}))
                    possible_erroneous_solvers.update([x for x in best_values if best_values[x] > max(op_values)])
    logging.info("Possible automatically detected culprits: {}".format(possible_erroneous_solvers))

    # statistics per solver and marginal solver
    statistics = {}
    marginal_solver = {"not_solved": 0}
    for i in results:
        for j in results[i]:
            if j not in statistics:
                statistics[j] = {"total": 0}
            statistics[j]["total"] += 1
            if results[i][j]["result"] not in statistics[j]:
                statistics[j][results[i][j]["result"]] = 1
            else:
                statistics[j][results[i][j]["result"]] += 1

        if instances[i][2] == "sat":
            solvers = sorted([(results[i][x]["time"],x) for x in results[i] if
                               results[i][x]["result"] == "sat" or results[i][x]["result"] == "uns"])
        else:
            solvers = sorted([(results[i][x]["time"],x) for x in results[i] if
                               results[i][x]["result"] == "opt"])
            if not solvers:
                if instances[i][2] == "min":
                    solvers = sorted([(results[i][x]["time"],min(results[i][x]["solutions"].values()),x)
                                      for x in results[i] if results[i][x]["result"] == "sat" and results[i][x]["solutions"]])
                else:
                    solvers = sorted([(results[i][x]["time"],max(results[i][x]["solutions"].values()),x)
                                      for x in results[i] if results[i][x]["result"] == "sat" and results[i][x]["solutions"]])
        if solvers:
            if solvers[0][-1] in marginal_solver:
                marginal_solver[solvers[0][-1]] += 1
            else:
                marginal_solver[solvers[0][-1]] = 1
        else:
            marginal_solver["not_solved"] += 1
    logging.info("Solver responses: {}".format(json.dumps(statistics,indent=2)))
    logging.info("Marginal solver: {}".format(json.dumps(marginal_solver, indent=2)))
    logging.info("Total number of instances: {}".format(len(instances)))
cli.add_command(check_anomalies)

if __name__ == '__main__':
    cli()
