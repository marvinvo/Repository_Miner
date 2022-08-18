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


def worker_pool(download_worker_func, input_queue, output_queue, s, iolock, nr_processes):
    count_value = Value('i', 0) #counts the finished downloaded projects
    end_event = Event()
    end_event.clear()
    # set up workers for project download
    download_pool = Pool(nr_processes, initializer=_worker_loop, initargs=(download_worker_func, input_queue, output_queue, count_value, s, iolock, end_event))

    def end():
        end_event.set()
        download_pool.close()
        download_pool.join()

    return [end, count_value]

def _clean_up(repo_path, repo):
    if "test" in str(repo_path):
        cmd = "rm -rf {}".format(repo["name"])
        try:
            output = subprocess.check_output(cmd.split(), cwd=repo_path)
        except subprocess.CalledProcessError:
            pass

def _worker_loop(worker_func, input_queue, output_queue, count_value, s, iolock, end_event):
    while not end_event.is_set():
        try:
            repo_path, i = input_queue.get(block=True, timeout=5)
        except Empty:
            continue

        with open(os.path.join(repo_path, FILENAME_REPO_JSON), "r") as g:
            repo = json.loads(g.read())
        
        
        try:
            # try to execute worker function
            log = worker_func(repo=repo, repo_path=repo_path, s=s, iolock=iolock)
        except WorkerError as e:
            with open(os.path.join(repo_path, FILENAME_WORKER_LOG), "a+") as l:
                l.write(str(e) + "\n")
            _clean_up(repo_path, repo)
            continue
        
        # write log
        with open(os.path.join(repo_path, FILENAME_WORKER_LOG), "a+") as l:
            l.write(log + "\n")

        # fill result queue
        if output_queue:
            output_queue.put((repo_path, i))

        # increase count value
        count_value.value += 1

def _general_worker_function(func, s, iolock, end_event, worker_id):
    print("thread {} started!".format(worker_id))
    work_on = len(func)
    while not end_event.is_set():
        if work_on == 0:
            work_on = len(func)
        # if (func[work_on]["output_queue"] and func[work_on]["output_queue"].full()) or func[work_on]["input_queue"].empty():
        #     work_on -= 1
        #     sleep(0.2)
        #     continue
        
        work_on -= 1
            
        try:
            repo_path, i = func[work_on]["input_queue"].get(block=True, timeout=1)
        except Empty:
            continue

        func[work_on]["worker_count"].value += 1

        with open(os.path.join(repo_path, FILENAME_REPO_JSON), "r") as g:
            repo = json.loads(g.read())
        
        
        try:
            # try to execute worker function
            log = func[work_on]["worker_func"](repo=repo, repo_path=repo_path, s=s, iolock=iolock)
        except Exception as e:
            with open(os.path.join(repo_path, FILENAME_WORKER_LOG), "a+") as l:
                l.write(str(e) + "\n")
            if s[settings.ARG_CLEAN_AFTER_FAILURE]:
                _clean_up(repo_path, repo)
            func[work_on]["failed_value"].value += 1
            func[work_on]["worker_count"].value -= 1
            continue

        
        # write log
        with open(os.path.join(repo_path, FILENAME_WORKER_LOG), "a+") as l:
            l.write(log + "\n")

        # fill result queue
        if func[work_on]["output_queue"]:
            func[work_on]["output_queue"].put((repo_path, i))

        # increase count value
        func[work_on]["count_value"].value += 1

        func[work_on]["worker_count"].value -= 1

def general_worker_pool(func_input_queue, s, iolock):
    end_event = Event()
    end_event.clear()

    # set up workers for project download
    # download_pool = ThreadPoolExecutor(max_workers=s[settings.ARG_PROCESS_LIMIT], initializer=_general_worker_function, initargs=(func_input_queue, s, iolock, end_event))
    #download_pool = Pool(s[settings.ARG_PROCESS_LIMIT], initializer=_general_worker_function, initargs=(func_input_queue, s, iolock, end_event))
    daemon_threads = [Thread(target=_general_worker_function, daemon=True, args=[func_input_queue, s, iolock, end_event, i]) for i in range(s[settings.ARG_PROCESS_LIMIT])]
    for daemon in daemon_threads:
        daemon.start()

    def end():
        end_event.set()
        for daemon in daemon_threads:
            daemon.join()

    return end
