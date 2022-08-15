from math import ceil
from multiprocessing.connection import wait
import os
from time import sleep
from xmlrpc.client import Boolean
from download.Download_Worker import download_worker_func
from compile.Compile_Worker import compile_worker_func
from search.Get_Repositories import Get_Repositories
from filter.Last_Commit_Not_Older_Than import Filter
from multiprocessing import Lock, Process, Queue, Value, Pool
import argparse, sys
from settings import Settings


def set_up_fetch(download_settings, args, result_queue):
    # add credentials to authenticate request to Git API
    with open(args['addtokenfile'], 'r') as f:
        download_settings.user_token_queue = [[row[0], row[1], None] for row in [line.replace('\n','').split(',') for line in f.readlines()]]

    g = Get_Repositories()
    g.settings = download_settings
    f = Filter()
    f.settings = download_settings

    # TODO probably better to set with Settings object
    # set up search from args
    filters = []
    if 'is-fork' in args:
        g._fork = args['isfork']
    else:
        g._fork = None
    if 'sort' in args:
        g._sort = args['sort']
    if 'order' in args:
        g._order = args['order']

    # set up filter from args
    if args['lastcommitnotolderthan']:
        filters += [f.last_commit_not_older_than(args['lastcommitnotolderthan'])]

    def start():
        # get generator that fetch and filter projects 
        repo = g.getRepositoriesGeneratorWithFilter(*filters)

        # fill result queue
        for i in range(args['maxdownload']):
            result_queue.put((next(repo),i)) # automatically blocks when queue is full

        # None in queue implicit tells download processes to terminate
        for _ in range(result_queue._maxsize):
            result_queue.put((None,None))
        
    return start


def set_up_download(input_queue, result_queue, nr_processes):
    downloaded_projects = Value('i', 0) #counts the finished downloaded projects

    # set up workers for project download
    download_pool = Pool(nr_processes, initializer=download_worker_func, initargs=(input_queue, downloaded_projects, result_queue, iolock, settings))

    def end():
        download_pool.close()
        download_pool.join() 

    return end


def set_up_compile(input_queue, nr_processes):
    compiled_projects = Value('i', 0) #counts the finished downloaded projects

    # set up workers for project compilation
    compile_pool = Pool(nr_processes, initializer=compile_worker_func, initargs=(input_queue, compiled_projects, iolock, settings))

    def end():
        compile_pool.close()
        compile_pool.join() 
        
    return end


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Fetch, Filter, Download Projects from Github and Compile Downloaded Projects')
    argparser.add_argument('--download', help='Fetch, Filter and Download Projects', action='store_true')
    argparser.add_argument('--compile', help='Compile Downloaded Projects', action='store_true')
    argparser.add_argument('--resultsfolder', help='Folder Path to store results', required=True)
    argparser.add_argument('--maxprocesses', type=int, default=20)
    # download
    argdownload = argparser.add_argument_group('download', 'Arguments for download flag')
    argdownload.add_argument('--addtokenfile', required='--download' in sys.argv)
    argdownload.add_argument('--maxdownload', type=int, default=100)
    argdownload.add_argument('--sort', nargs=1, choices=['best-match', 'stars'],default='stars', help='sort downloaded projects')
    argdownload.add_argument('--order', nargs=1, choices=['desc', 'asc'], default='desc', help='sort order for downloaded projects')
    # filter
    argfilter = argdownload.add_argument_group('filter', 'available filter applied before download')
    argfilter.add_argument('--isfork', choices=['true', 'false'])
    argfilter.add_argument('--lastcommitnotolderthan', type=int, metavar='days', nargs=1, help='latest commit must be within set days')
    # compile
    argcompile = argparser.add_argument_group('compile', 'Arguments for compile flag')

    args = vars(argparser.parse_args(sys.argv[1:]))

    # maximal number of parallel processes to start
    NCORE = 2 if args['maxprocesses'] < 2 else args['maxprocesses']

    settings = Settings()
    # path where downloaded projects are stored or should be stored
    settings.result_path = args['resultsfolder']

    if args['addtokenfile']:
        # add credentials to authenticate request to Git API
        with open(args['addtokenfile'], 'r') as f:
            settings.user_token_queue = [[row[0], row[1], None] for row in [line.replace('\n','').split(',') for line in f.readlines()]]

    

    if args['download'] and args['compile']:
        # set up queues for multiprocessing
        download_queue = Queue(int(NCORE/2)) # processed by download workers
        compile_queue = Queue(int(NCORE/2)) # processed by compile workers
        iolock = Lock() # general lock might be required for certain io actions

        start_func = set_up_fetch(settings, args, download_queue)
        end_download = set_up_download(download_queue, compile_queue, int(NCORE/2))
        end_compile = set_up_compile(compile_queue, int(NCORE/2))
        start_func()
        end_download()
        end_compile()
        exit(0)

    if args['download'] and not args['compile']:
        # set up queues for multiprocessing
        download_queue = Queue(NCORE) # processed by download workers
        iolock = Lock() # general lock might be required for certain io actions

        start_func = set_up_fetch(settings, args, download_queue)
        end_download = set_up_download(download_queue, None, NCORE)
        start_func()
        end_download()
        exit(0)

    if not args['download'] and args['compile']:
        # set up queues for multiprocessing
        compile_queue = Queue(NCORE) # processed by compile workers
        iolock = Lock() # general lock might be required for certain io actions

        end_compile = set_up_compile(compile_queue, NCORE)
        # start compilation
        for folder in os.listdir(settings.result_path):
            f = os.path.join(settings.result_path, folder)
            # checking if it is a file
            if os.path.isdir(f):
                compile_queue.put(f)
        
        
        for _ in range(compile_queue._maxsize):
            compile_queue.put(None)
        
        end_compile()
        exit(0)



