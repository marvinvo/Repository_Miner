ARG_FETCH = "fetch"
ARG_DOWNLOAD = "download"
ARG_COMPILE = "compile"
ARG_RESULTFOLDER = "resultsfolder"
ARG_PROCESS_LIMIT = "maxprocesses"
ARG_TOKEN_FILE = "tokenfile"
ARG_SORT = "sort"
ARG_ORDER = "order"
ARG_FORK = "fork"
ARG_FILTER = "filter"
ARG_LAST_SORT = "lastsort"

ARG_EXEC_AFTER_FETCH = "" # probably unneccassary feature
ARG_EXEC_AFTER_DOWNLOAD = "execAfterDownload"
ARG_SHELL_SCRIPT = "execonsuccess" # this is acutally ARG_EXEC_AFTER_COMPILE

ARG_CLEAN_AFTER_FAILURE = "keepclean"
ARG_STATS_TO_FILE = "writestats"

FILENAME_REPO_JSON = "github.json"
FILENAME_WORKER_LOG = "worker.log"
FILENAME_DOWNLOAD_LOG = "download.log"
FILENAME_COMPILE_LOG = "compile.log"
FILENAME_SHELL_LOG = "shell.log"
FILENAME_EXTENSION_FOR_ERRORS = "errors_" # e.g. errors_shell.log for shell errors

TIMEOUT_DOWNLOAD = 600
TIMEOUT_COMPILE = 800
TIMEOUT_SHELL = 300

class Settings(dict):
    
    def parse_args(self, args):
        for key in args:
            self[key] = args[key]
        if ARG_TOKEN_FILE in self:
            with open(self[ARG_TOKEN_FILE], 'r') as f:
                self[ARG_TOKEN_FILE] = [[row[0], row[1], None] for row in [line.replace('\n','').split(',') for line in f.readlines()]]

