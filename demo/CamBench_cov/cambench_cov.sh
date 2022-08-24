#! /usr/bin/env bash


# RESULTS_FOLDER="/Users/marvinvogel/Downloads/test5"
# GITHUB_TOKENS="/Users/marvinvogel/Documents/Uni/CamBench/docker/CREDENTIALS.txt"
# MAX_PROCESSES="20"
FORK="false"

_bash_source=$( dirname "${BASH_SOURCE[0]}" )
_bash_source="$(realpath "$_bash_source")"
_execute_after_download="$_bash_source/scripts/execute_after_download.sh"
_execute_after_compile="$_bash_source/scripts/execute_after_compile.sh"

echo $_execute_after_download
echo $_execute_after_compile

python3 "$_bash_source/../../main.py" --resultsfolder "$RESULTS_FOLDER" --tokenfile "$GITHUB_TOKENS" \
--fetch --download --execAfterDownload "zsh $_execute_after_download" --compile --execonsuccess "zsh $_execute_after_compile" \
--maxprocesses $MAX_PROCESSES --keepclean --writestats \
--fork $FORK 