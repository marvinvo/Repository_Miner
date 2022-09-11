import itertools
from math import ceil
from multiprocessing.connection import wait
import os
from queue import Full
from time import sleep
from xmlrpc.client import Boolean
from queue import Queue
import threading
from multiprocessing import Event, Lock, Process, Value, Pool
import argparse, sys
from repository_worker.Worker import general_worker_pool
from repository_worker.Download_Worker import download_worker_func
from repository_worker.ShellScript_Worker import script_worker_func
from repository_worker.Compile_Worker import compile_worker_func
import settings
from settings import Settings
from repository_fetcher.Get_Repositories import Get_Repositories
import sys

def clear_queue(queue):
    while not queue.empty():
        queue.get()

#
# FUNCTIONS TO INITIAL FILL QUEUES
#

def fetched(output_queue, s, end_event):
    # find repositories that are already fetched
    for _, dirnames, _ in os.walk(s[settings.ARG_RESULTFOLDER]):
        for dir in dirnames:
            if end_event.is_set():
                return

            project_path = os.path.join(s[settings.ARG_RESULTFOLDER], dir)
            log_path = os.path.join(s[settings.ARG_RESULTFOLDER], dir, settings.FILENAME_WORKER_LOG)
            github_json = os.path.join(s[settings.ARG_RESULTFOLDER], dir, settings.FILENAME_REPO_JSON)
            if not os.path.exists(log_path) and os.path.exists(github_json):
                output_queue.put((project_path, 0))
            if os.path.exists(github_json):
                if not os.path.exists(log_path):
                    output_queue.put((project_path, 0))
                else:
                    with open(log_path, 'r') as log:
                        if len(log.readlines()) == 0:
                            output_queue.put((project_path, 0))
                



    # fetch new repositories from github
    print("start fetching from github")
    g = Get_Repositories(s)
    # get generator that fetch and filter projects 
    gen = g.getRepositoryGeneratorFromSettings()
    
    # write stats
    i=0
    while not end_event.is_set():
        # fill input queue
        repo = next(gen)
        output_queue.put((repo,i))
        i+=1

    

def last_state(output_queue, s, end_event, last_state):
    for dirpath, dirnames, filenames in os.walk(s[settings.ARG_RESULTFOLDER]):
        for dir in dirnames:
            if end_event.is_set():
                return

            project_path = os.path.join(s[settings.ARG_RESULTFOLDER], dir)
            log_path = os.path.join(s[settings.ARG_RESULTFOLDER], dir, settings.FILENAME_WORKER_LOG)
            if not os.path.exists(log_path):
                continue

            with open(log_path, 'r') as log:
                # TODO file could be empty
                lines = log.readlines()
                if not lines:
                    continue
                last_line = lines[-1]
                if "Failed" in last_line or "Timeout" in last_line:
                    continue
                if last_state in last_line:
                    output_queue.put((project_path, 0))
                
def downloaded(output_queue, s, end_event):
    last_state(output_queue, s, end_event, "Download")

def compiled(output_queue, s, end_event):
    last_state(output_queue, s, end_event, "Compile")

def after_download_script(output_queue, s, end_event):
    last_state(output_queue, s, end_event, "{}".format(s[settings.ARG_EXEC_AFTER_DOWNLOAD]))

#
# Stats Process Function
#
def print_stats(s, func, end_event):
    if s[settings.ARG_STATS_TO_FILE]:
        stats_file = os.path.join(s[settings.ARG_RESULTFOLDER], "general_stats.log")
        while not end_event.is_set():
            stats = "{}   ......   {}\n".format(", ".join(["{}: {}".format(f["name"] + " success ratio", "{}/{}".format(f["count_value"].value, f["failed_value"].value + f["count_value"].value)) for f in func]), ", ".join(["{}: {}".format(f["name"] + " worker", f["worker_count"].value) for f in func]) )
            with open(stats_file, "a+") as f:
                f.write(stats)
            sleep(10)
    else:
        UP = "\x1B[{}A".format(len(func)+4)
        CLR = "\x1B[0K"
        while not end_event.is_set():
            stats = f"{CLR}\n========================================={CLR}\n{CLR}"
            stats += f"{CLR}\n".join(["{}: {}".format(f["name"].split("/")[-1] + " success ratio & worker", "{}/{}, {}".format(f["count_value"].value, f["failed_value"].value + f["count_value"].value, f["worker_count"].value)) for f in func])
            stats += f"\n========================================={CLR}\n{CLR}"
            stats += f"{UP}"
            print(stats)
            sleep(1)

#
# workers process function
#
def workers(func, s, iolock, locks):
    return general_worker_pool(func, s, iolock, locks)

#python3 main.py --resultsfolder /Users/marvinvogel/Downloads/test5 --tokenfile ../CREDENTIALS.txt --fetch --download --compile --execonsuccess ../run_cambench_cov.sh

if __name__ == '__main__':
    # due to unexpected exit errors
    sys.setrecursionlimit(20000)
    argparser = argparse.ArgumentParser(description='Fetch, Filter, Download Projects from Github and Compile Downloaded Projects')
    # general
    argparser.add_argument('--{}'.format(settings.ARG_RESULTFOLDER), help='folder to store results', required=True)
    argparser.add_argument('--{}'.format(settings.ARG_PROCESS_LIMIT), type=int, default=20)
    argparser.add_argument('--{}'.format(settings.ARG_STATS_TO_FILE), action='store_true')

    # fetch
    argfetch = argparser.add_argument_group('fetch', 'Arguments for fetching repositories')
    argfetch.add_argument('--{}'.format(settings.ARG_FETCH), help='fetch repositories', action='store_true')
    argfetch.add_argument('--{}'.format(settings.ARG_TOKEN_FILE), required='--{}'.format(settings.ARG_FETCH) in sys.argv)
    argfetch.add_argument('--{}'.format(settings.ARG_SORT), nargs=1, choices=['best-match', 'stars'],default='stars')
    argfetch.add_argument('--{}'.format(settings.ARG_ORDER), nargs=1, choices=['desc', 'asc'], default='desc')
    argfetch.add_argument('--{}'.format(settings.ARG_FORK), choices=['true', 'false'])
    argfetch.add_argument('--{}'.format(settings.ARG_FILTER), nargs='*', choices=['lastcommitnotolderthan'])

    # download
    argdownload = argparser.add_argument_group('download', 'Arguments for cloning repositories')
    argdownload.add_argument('--{}'.format(settings.ARG_DOWNLOAD), help='clone fetched repositories', action='store_true')
    argdownload.add_argument('--{}'.format(settings.ARG_CLEAN_AFTER_FAILURE), help='removes cloned repository after failure', action='store_true')
    argdownload.add_argument('--{}'.format(settings.ARG_EXEC_AFTER_DOWNLOAD), help='path to shell script that is executed after download')
    
    # compile
    argcompile = argparser.add_argument_group('compile', 'Arguments for compile flag')
    argcompile.add_argument('--{}'.format(settings.ARG_COMPILE), help='compile projects in downloaded repositories', action='store_true')

    # shell
    argcompile.add_argument('--{}'.format(settings.ARG_SHELL_SCRIPT), help='path to shell script that is executed on success')


    args = vars(argparser.parse_args(sys.argv[1:]))

    s = Settings()
    s.parse_args(args)
        
    # TODO fill queues to continue
    required_queues = sum([s[settings.ARG_COMPILE], s[settings.ARG_DOWNLOAD], s[settings.ARG_SHELL_SCRIPT] != None, s[settings.ARG_EXEC_AFTER_DOWNLOAD] != None])
    process_limit = max(2, s[settings.ARG_PROCESS_LIMIT])
    queue_limit = max(1, int(process_limit/2))
    queues = [Queue(queue_limit) for i in range(required_queues)] + [None,]
    iolock = Lock() # general lock might be required for certain io actions
    
    print("set up pipeline")
    
    queue_fill_functions = []

    func = []
    if s[settings.ARG_FETCH]:
        queue_fill_functions += [fetched,] # this is not implemented as worker
    if s[settings.ARG_DOWNLOAD]:
        func += [{"worker_func": download_worker_func, "name": "download"}]
        queue_fill_functions += [downloaded,]
    if s[settings.ARG_EXEC_AFTER_DOWNLOAD]:
        func += [{"worker_func": script_worker_func, "name": s[settings.ARG_EXEC_AFTER_DOWNLOAD]}]
        queue_fill_functions += [after_download_script,]
    if s[settings.ARG_COMPILE]:
        func += [{"worker_func": compile_worker_func, "name": "compile"}]
        queue_fill_functions += [compiled,]
    if s[settings.ARG_SHELL_SCRIPT]:
        func += [{"worker_func": script_worker_func, "name": s[settings.ARG_SHELL_SCRIPT]}]
        queue_fill_functions += [lambda *x:x,] # add dummy function because this cannot fill any queue

    for i in range(required_queues):
        func[i]["input_queue"] = queues[i]
        func[i]["output_queue"] = queues[i+1]
        func[i]["count_value"] = Value('i', 0)
        func[i]["failed_value"] = Value('i', 0)
        func[i]["worker_count"] = Value('i', 0)

    end_event = Event()
    end_event.clear()
                   
    end_daemon_workers = workers(func, s, iolock, locks={"gradle": Lock()})
    #worker_process = Process(target=workers, args=(func, s))
    #worker_process.daemon = True
    #worker_process.start()

    print("pipeline is ready")

    stats_thread = threading.Thread(target=print_stats, args=(s, func, end_event), daemon = True)
    stats_thread.start()

    print("start filling worker queues...")
    for i in range(1, len(queue_fill_functions)+1):
        queue_fill_functions[-i](func[-i+1]["input_queue"], s, end_event)


    

    #end_workers()
    exit(0)
        

