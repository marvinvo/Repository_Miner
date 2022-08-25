#! /usr/bin/env bash


#
# This script executes CamBench_cov on compiled projects.
# It returns a non-zero exit status if no usages of a specified package was found.
#

# parameter: $1=absolute_repo_path, $2=absolute_project_path

_bash_source=$( dirname "${BASH_SOURCE[0]}" )
_bash_source="$(realpath "$_bash_source")"
cambench="$_bash_source/lib/CamBench_cov.jar"
packages_to_scan="$_bash_source/packages.txt"
analysis_result_folder="$1/analysis_results"
execute_on_success="$_bash_source/scripts/execute_on_success.sh"


mkdir "$analysis_result_folder";

cat "$packages_to_scan" >&2

i=0;
for folder in $1/**/classes/ ; do
    echo "Search for usages of specified packages in $folder" >&2;
    mkdir "$analysis_result_folder/classes_folder_$i";
    report_path="$analysis_result_folder/classes_folder_$i";
    echo "execute: java -jar '$cambench' --result-path $report_path --project-path $folder --packages-to-scan $(readlink -f $packages_to_scan);" >&2;
    java -jar "$cambench" --result-path "$report_path" --project-path "$folder" --packages-to-scan "$(readlink -f $packages_to_scan)";
    if [[ $? -eq 0 ]]
    then
        i=$(( i + 1 ));
        echo "Usages of specified packages found in $folder. Results are stored in $report_path" >&2;
        zsh $execute_on_success $1 $2 $report_path || true
    else 
        echo "No crypto api calls found in $folder" >&2;
        rm -rf $report_path;
    fi
done

if [[ $i -gt 0 ]]
then
    exit 0;
else
    echo "No crypto api calls found for this project" >&2;
    rm -rf "$analysis_result_folder";
    exit 1;
fi
