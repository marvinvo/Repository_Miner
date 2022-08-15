# Repository Miner
Repository Miner is a tool that automatically clone Github repositories on a large scale. Further it can try to compile projects in cloned repositories.

### Features
- download repos and compile projects in parallel with multiprocessing
- use multiple Github tokens to bypass rate limit
- fetch repositories sort by best-match or stars in ascending or descending order
- apply multiple filters before download, e. g. fork or last commit date

### General Usage
````
usage: main.py [-h] [--download] [--compile] --resultsfolder RESULTSFOLDER 
        [--maxprocesses MAXPROCESSES] [--addtokenfile ADDTOKENFILE] [--maxdownload MAXDOWNLOAD]
        [--sort {best-match,stars}] [--order {desc,asc}] [--isfork {true,false}] [--lastcommitnotolderthan days]

Fetch, Filter, Download Projects from Github and Compile Downloaded Projects

options:
  -h, --help            show this help message and exit
  --download            Fetch, Filter and Download Projects
  --compile             Compile Downloaded Projects
  --resultsfolder RESULTSFOLDER
                        Folder Path to store results
  --maxprocesses MAXPROCESSES

download:
  Arguments for download flag

  --addtokenfile ADDTOKENFILE
  --maxdownload MAXDOWNLOAD
  --sort {best-match,stars}
                        sort downloaded projects
  --order {desc,asc}    sort order for downloaded projects

compile:
  Arguments for compile flag
````


