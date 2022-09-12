from concurrent.futures import ThreadPoolExecutor
import json
from multiprocessing import Event, Pool, Value
import os
from queue import Empty
from random import Random
import subprocess
from threading import Thread
from time import sleep
from repository_worker.WorkerError import WorkerError
import settings

from settings import FILENAME_REPO_JSON, FILENAME_WORKER_LOG


def _clean_up(repo_path, repo):
    """
    This method is called when a pipeline step execution failed and the keepclean flag is set. 
    It removes downloaded or cloned repositories from file system.
    """
    cmd = "rm -rf {}".format(repo["name"])
    try:
        output = subprocess.check_output(cmd.split(), cwd=repo_path)
    except subprocess.CalledProcessError:
        pass


def _general_worker_function(func, s, iolock, end_event, worker_id, locks):
    print("thread {} started!".format(worker_id))
    work_on = len(func) # defines the pipeline step function to execute
    while not end_event.is_set():
        try:
            if work_on < 0:
                # end of pipeline, start at last pipeline step
                work_on = len(func)-1

            # holds information about pipeline step, such as the execution function, input and output queue and counter
            current_pipeline_step = func[work_on]
            
            # get input
            try:
                # try to get input from input queue of current pipeline step
                repo_path, i = current_pipeline_step["input_queue"].get(block=True, timeout=1)
                # current pipeline step had input, hence try to execute last pipeline step next
                # this somehow defines the weightnig to prefer last pipeline steps
                work_on = len(func)-1
            except Empty:
                # no input available, hence try to execute a preceding pipeline step
                work_on -= 1
                continue
            
            
            # for stats
            current_pipeline_step["worker_count"].value += 1

            # read input
            # this is simply Github repository metadata
            with open(os.path.join(repo_path, FILENAME_REPO_JSON), "r") as g:
                repo = json.loads(g.read())
            
            # execute pipeline step
            try:
                log = current_pipeline_step["worker_func"](repo=repo, repo_path=repo_path, s=s, iolock=iolock, func=current_pipeline_step, locks=locks)
            except Exception as e:
                # pipeline step failed
                with open(os.path.join(repo_path, FILENAME_WORKER_LOG), "a+") as l:
                    # write errors to error log
                    l.write(str(e) + "\n")
                # remove downlaoded repository if specified  
                if s[settings.ARG_CLEAN_AFTER_FAILURE]:
                    _clean_up(repo_path, repo)

                # for stats
                current_pipeline_step["failed_value"].value += 1
                current_pipeline_step["worker_count"].value -= 1
                continue

            
            # write log
            with open(os.path.join(repo_path, FILENAME_WORKER_LOG), "a+") as l:
                l.write(log + "\n")

            # fill result queue
            if current_pipeline_step["output_queue"]:
                current_pipeline_step["output_queue"].put((repo_path, i))

            # for stats
            current_pipeline_step["count_value"].value += 1
            current_pipeline_step["worker_count"].value -= 1
            
        except Exception as e:
            # unknown Exception
            print(e)


def start(func_input_queue, s, iolock, locks, end_event):
    # set up worker pool
    daemon_threads = [Thread(target=_general_worker_function, daemon=True, args=[func_input_queue, s, iolock, end_event, i, locks]) for i in range(s[settings.ARG_PROCESS_LIMIT])]
    for daemon in daemon_threads:
        daemon.start()

    def end():
        if not end_event.is_set():
            end_event.set()
        print("wait for daemon workers to terminate")
        print("this might take a while ...")
        for daemon in daemon_threads:
            daemon.join()

    return end
