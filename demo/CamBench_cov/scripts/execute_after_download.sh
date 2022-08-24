#! /usr/bin/env bash

#
# This script provides a rough search if specified packages are used in a given project or not.
# Only projects that might contain usages of pecified packages are further put into the pipeline.
#

# parameter: $1=absolute_repo_path, $2=absolute_project_path


_bash_source=$( dirname "${BASH_SOURCE[0]}" )
_bash_source="$(realpath "$_bash_source")"

# create regex from packages
# readarray -t packages < $_bash_source/../packages.txt;
# TODO replace IFS as this is not recommend to use
# IFS=$'\n' read -d '' -r -a packages < $_bash_source/packages.txt;

# cat "$_bash_source/../packages.txt" >&2;

regex=""
#for i in "${packages[@]}"
cat "$_bash_source/packages.txt" | while read i; do
    # also add *, e.g. java.* also imports java.security
    start=""
    # arr=$( echo $i | tr "." " " )
    echo "$i" | tr "\." "\n" | head -n1 | while read j; do
        start="$start.$j"
        regex="$regex|${start:1}\.\*"
    done
    regex="$regex|$i"
done
regex="${regex:1}" # remove first '|'

#echo "search for regex: $regex" >&2;

# search in all files for regex
find $2 -name '*.java' -o -name '*.java' | xargs -n1 cat | grep -q -E "$regex";






