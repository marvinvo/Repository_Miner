# Repository Miner
Repository Miner is a tool that automatically clone Github repositories on a large scale. Further it can try to compile projects in cloned repositories.

### Features
- download repos and compile projects in parallel
- use multiple Github tokens to bypass rate limit
- fetch repositories sort by best-match or stars in ascending or descending order
- apply multiple filters before download, e. g. fork or last commit date

### General Usage
````
main.py [-h] [--download] [--compile] --resultsfolder RESULTSFOLDER [--maxprocesses MAXPROCESSES] 
  [--addtokenfile ADDTOKENFILE] [--maxdownload MAXDOWNLOAD]
  [--sort {best-match,stars}] [--order {desc,asc}] [--isfork {true,false}] [--lastcommitnotolderthan days]
````


