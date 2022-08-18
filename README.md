# Repository Miner
Repository Miner is a tool that can: 
- fetch github repositories
- clone fetched repositories
- compile projects in cloned repositories
- run a custom script on compiled project and cloned or feched repository data

### Features
- multiprocessing pipeline
- use multiple Github tokens to bypass rate limit
- fetch repositories with filters and in sort order

### Result Data
Results are stored in `<RESULTSFOLDER>`. Thereby, Repository Miner generates a subfolder for each repository:
````
<RESULTSFOLDER>
|---<repository full name>
    |---<repository name>/   (folder with repository clone)
    |---github.json          (general information about repository)
    |---download.log         (stout and sterr for git clone)
    |---compile.log          (stout and sterr for project compile)
    |---shell.log            (stout and sterr for costum shell script)
    |---worker.log           (information about last pipeline state)
    
|---<repository full name>
    |---...
````

### Pipeline
The basic pipeline is `fetch -> clone -> compile -> costum script`.
Although we can not change the pipeline order, we can skip certain steps. E. g. if only fetched repository data is required for a custom script, we can simply remove `--download` and `--compile` from the argument list and have the pipeline `fetch -> costum script`.
Pipeline action, e. g. the `clone` action, are handled seperate tasks and collected in queues.
Multiply worker processes are seeded by these queues and execute these tasks.
While running Repository Miner we gain information about these tasks and workers:

````
download success ratio: 582/586, compile success ratio: 164/567, execute success ratio: 101/164   ......   download worker: 6, compile worker: 15, execute worker: 0
````


### General Usage
````
usage: main.py [-h] --resultsfolder RESULTSFOLDER [--maxprocesses MAXPROCESSES] [--fetch] [--tokenfile TOKENFILE] [--sort {best-match,stars}] [--order {desc,asc}]
               [--fork {true,false}] [--filter [{lastcommitnotolderthan} ...]] [--download] [--compile] [--execonsuccess EXECONSUCCESS]

options:
  -h, --help            show this help message and exit
  --resultsfolder RESULTSFOLDER
                        folder to store results
  --maxprocesses MAXPROCESSES

fetch:
  Arguments for fetching repositories

  --fetch               fetch repositories
  --tokenfile TOKENFILE
  --sort {best-match,stars}
  --order {desc,asc}
  --fork {true,false}
  --filter [{lastcommitnotolderthan} ...]

download:
  Arguments for cloning repositories

  --download            clone fetched repositories

compile:
  Arguments for compile flag

  --compile             compile projects in downloaded repositories
  --execonsuccess EXECONSUCCESS
                        path to shell script that is executed on success
````


