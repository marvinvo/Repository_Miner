#! /usr/bin/env bash


#
# This script executes CamBench_cov on compiled projects.
# It returns a non-zero exit status if no usages of a specified package was found.
#

# parameter: $1=absolute_repo_path, $2=absolute_project_path

#MEMORY_JAVA=3G
#STACKSIZE_JAVA=2M

_bash_source=$( dirname "${BASH_SOURCE[0]}" )
_bash_source="$(realpath "$_bash_source")"
tools="$_bash_source/tools"
cambench="$_bash_source/lib/CamBench_cov.jar"
packages_to_scan="$_bash_source/packages.txt"
analysis_result_folder="$1/analysis_results"


mkdir "$analysis_result_folder";

cat "$packages_to_scan" >&2

i=0;
for folder in $2/**/echobuild/**/*.jar; do
    java -Xmx$MEMORY_JAVA -Xss$STACKSIZE_JAVA -jar "$cambench" --result-path "$report_path" --project-path "$folder" --result-dir "/" --packages-to-scan "$(readlink -f $packages_to_scan)" --include-jars;
    if [[ $? -eq 0 ]]
    then
        i=$(( i + 1 ));
        echo "Usages of specified packages found in $folder. Results are stored in $report_path" >&2;
        # all tools now analyze this jar
        for tool in $tools/*; do
            $tool/analyze_jar.sh $folder $analysis_result_folder
        done
    else 
        echo "No crypto api calls found in $folder" >&2;
        rm -rf $report_path;
    fi
done
