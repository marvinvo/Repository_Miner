#! /usr/bin/env bash


# RESULTS_FOLDER="/Users/marvinvogel/Downloads/test5"
# GITHUB_TOKENS="/Users/marvinvogel/Documents/Uni/CamBench/docker/CREDENTIALS.txt"
# MAX_PROCESSES="20"
FORK="false"

_bash_source=$( dirname "${BASH_SOURCE[0]}" )
_bash_source="$(realpath "$_bash_source")"
_execute_after_compile="$_bash_source/docker/execute_after_compile.sh"


python3 "$_bash_source/../../main.py" --resultsfolder "$RESULTS_FOLDER" --tokenfile "$GITHUB_TOKENS" \
--download --compile --execonsuccess "zsh $_execute_after_compile" \
--maxprocesses $MAX_PROCESSES --writestats \
--fork $FORK \
--lastsort $LASTSORT