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

import click

QUEUE = Queue.Queue()
MZN_ID = 0
DZN_ID = 1
SOL_ID = 2


@click.group()
@click.option('--log-level',
              help='Log level (DEBUG, INFO, WARNING, ERROR or CRITICAL)',
              type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
              default="DEBUG")
def cli(log_level):
    # Configure logging
    logging.basicConfig(level=log_level)

################################
# Get the list
################################

def get_mzn_dzn_pairs(dir_name):
    dirs = [os.path.join(dir_name,f) for f in os.listdir(dir_name) if os.path.isdir(os.path.join(dir_name,f))]
    mzn = [os.path.join(dir_name,f) for f in os.listdir(dir_name) if f.endswith(".mzn")]
    dzn = [os.path.join(dir_name,f) for f in os.listdir(dir_name) if f.endswith(".dzn")]

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
@click.option('--solvers','-s',multiple=True,
              help='Solver to use',
              default=[])
def create_request_list(
        request_file,
        problems_dir,
        solvers
        ):
    '''
    Create the request list using mzn, dzn files in a directory.
    '''
    logging.info("Solvers to use: {}".format(",".join(solvers)))

    mzn_dzn_pair = get_mzn_dzn_pairs(problems_dir)
    logging.info("Retrieved {} problems to solve".format(len(mzn_dzn_pair)))

    triples = [(x,y,z) for (x,y) in mzn_dzn_pair for z in solvers]
    with open(request_file,'wb') as f:
        for (x,y,z) in [(x,y,z) for (x,y) in mzn_dzn_pair for z in solvers]:
            f.write("{}|{}|{}\n".format(x,y,z))
cli.add_command(create_request_list)


################################
# Get results running sunny remotely
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
                    if len(result["solutions"]) > 0:
                        result["result"] = "opt"
                    else:
                        result["result"] = "uns"
                else:
                    result["result"] = "uns"
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
                    response = requests.post(url + "/get_features", files=files, headers={'host': hostname} if hostname else {})
                    logging.debug("Thread {} received answer with code {}.".format(thread_num, response.status_code))
                    # handle error in the answer
                    if response.status_code != requests.codes.ok:
                        logging.error("Error {}. Feature vector request ended up with error {}, response {}.".format(
                            item, response.status_code, response.text))
                        QUEUE.task_done()
                        continue
                    # parse the answer
                    try:
                        feature_vector = [float(x) if "nan" not in x else 0 for x in response.text.split(",")]
                        # the s_goal is the feature having index 59
                        s_goal = feature_vector[59]
                        logging.debug("Obtained feature vector {}".format(feature_vector))
                    except ValueError:
                        logging.error(
                            "Error {}. Feature vector response {} can not be parsed.".format(
                                item, response.text))
                        QUEUE.task_done()
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

                logging.debug("Thread {} sending request".format(thread_num))
                response = requests.post(url + "/process", files=files, headers={'host': hostname} if hostname else {})
                logging.debug("Thread {} received answer with code {}.".format(thread_num,response.status_code))
                if response.status_code != requests.codes.ok:
                    logging.error("Error {}. Ended up with error {}, response {}.".format(
                        item,response.status_code,response.text))
                else:
                    # parse the response
                    json_result = parse_solver_output(response.text)
                    if "error" in json_result:
                        logging.error("Error {}. Wrong parse of answer {} in response <<<<< {} >>>>>".format(
                            item, json_result["error"],response.text
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
                logging.error("ERROR {}. Request not well formed".format(item, item[DZN_ID]))
            QUEUE.task_done()
        except Queue.Empty:
            # Handle empty queue here
            break
        except requests.exceptions.RequestException as e:
            logging.critical("Connection problems {}. Request discarded.".format(unicode(e)))
            QUEUE.task_done()
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
                if len(lines[-1]) != 3:
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

    logging.info("Start to create the feature_file")
    instance_type = {}
    with open(feature_file,'wb') as f:
        for row in cursor.execute("SELECT id,features,type FROM instances", ()):
            instance_type[row[0]] = row[2]
            # structure: inst|[f_1, ..., f_n]
            f.write("{}|{}\n".format(row[0],row[1]))
    logging.info("Processed {} instances".format(len(instance_type)))


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

    connection.close()
    logging.info("To generate the KB directory test_kb locally run 'csv2kb.py -p ./ test_kb {} {}'".format(feature_file,info_file))
cli.add_command(generate_kb_files)



if __name__ == '__main__':
    cli()
