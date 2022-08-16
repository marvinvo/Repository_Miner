import itertools
from math import ceil
from multiprocessing.connection import wait
import os
from queue import Full
from time import sleep
from xmlrpc.client import Boolean
from multiprocessing import Event, Lock, Process, Queue, Value, Pool
import argparse, sys
from repository_worker.Worker import general_worker_pool
from repository_worker.Download_Worker import download_worker_func
from repository_worker.ShellScript_Worker import script_worker_func
from repository_worker.Compile_Worker import compile_worker_func
import settings
from settings import Settings
from repository_fetcher.Get_Repositories import Get_Repositories

def _fetch_process_func(settings, maxdownload, output_queue, end_event):
    g = Get_Repositories(settings)
    # get generator that fetch and filter projects 
    gen = g.getRepositoryGeneratorFromSettings()
    # fill output queue
    for i in itertools.count(start=1):
        repo = next(gen)
        output_queue.put((repo,i))

def start_fetch(settings, output_queue):
    end_event = Event()
    end_event.clear()
    p = Pool(1, initializer=_fetch_process_func, initargs=(settings, 3, output_queue, end_event))

    def stop():
        end_event.set()
        p.close()
        p.join()
        
        
    return stop()

def clear_queue(queue):
    while not queue.empty():
        queue.get()



if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Fetch, Filter, Download Projects from Github and Compile Downloaded Projects')
    # general
    argparser.add_argument('--{}'.format(settings.ARG_RESULTFOLDER), help='folder to store results', required=True)
    argparser.add_argument('--{}'.format(settings.ARG_PROCESS_LIMIT), type=int, default=20)

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
    
    # compile
    argcompile = argparser.add_argument_group('compile', 'Arguments for compile flag')
    argcompile.add_argument('--{}'.format(settings.ARG_COMPILE), help='compile projects in downloaded repositories', action='store_true')

    # shell
    argcompile.add_argument('--{}'.format(settings.ARG_SHELL_SCRIPT), help='path to shell script that is executed on success')


    args = vars(argparser.parse_args(sys.argv[1:]))

    s = Settings()
    s.parse_args(args)
        
    # TODO fill queues to continue
    required_queues = sum([s[settings.ARG_COMPILE], s[settings.ARG_DOWNLOAD], s[settings.ARG_SHELL_SCRIPT] != None])
    process_limit = max(2, s[settings.ARG_PROCESS_LIMIT])
    queue_limit = max(1, int(process_limit/2))
    queues = [Queue(queue_limit) for i in range(required_queues)] + [None,]
    iolock = Lock() # general lock might be required for certain io actions
    
    print("set up pipeline")
    def start_func():
        return
    # worker_func, input_queue, output_queue, count_value
    func = []

    if s[settings.ARG_DOWNLOAD]:
        func += [{"worker_func": download_worker_func, "name": "download"}]
    if s[settings.ARG_COMPILE]:
        func += [{"worker_func": compile_worker_func, "name": "compile"}]
    if s[settings.ARG_SHELL_SCRIPT]:
        func += [{"worker_func": script_worker_func, "name": "execute"}]

    for i in range(required_queues):
        func[i]["input_queue"] = queues[i]
        func[i]["output_queue"] = queues[i+1]
        func[i]["count_value"] = Value('i', 0)
        func[i]["failed_value"] = Value('i', 0)
        func[i]["worker_count"] = Value('i', 0)

    end_workers = general_worker_pool(func, s, iolock)
    print("pipeline is ready")

    if s[settings.ARG_FETCH]:
        g = Get_Repositories(s)
        # get generator that fetch and filter projects 
        gen = g.getRepositoryGeneratorFromSettings()
        
        # write stats
        i=0
        while func[-1]["count_value"].value < 100:
            # fill input queue
            repo = next(gen)
            queues[0].put((repo,i))
            stats = "{}   ......   {}".format(", ".join(["{}: {}".format(f["name"] + " success ratio", "{}/{}".format(f["count_value"].value, f["failed_value"].value + f["count_value"].value)) for f in func]), ", ".join(["{}: {}".format(f["name"] + " worker", f["worker_count"].value) for f in func]) )
            print(stats, end='\r')
            i+=1

    end_workers()
    exit(0)
        

