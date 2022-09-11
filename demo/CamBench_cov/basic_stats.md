# GENERAL STATS
tail -n1 general_stats.log

# TIMEOUT ERRORS
    for i in */worker.log; do cat $i; done | grep "Timeout" | wc -l

# Execute before compile
    for i in */worker.log; do cat $i; done | grep "zsh /opt/app/Repository_Miner/demo/CamBench_cov/scripts/execute_after_download.sh Success" | wc -l

# COMPILE ERRORS

Compile Success:
    for i in */worker.log; do cat $i; done | grep "Compile Success" | wc -l

Output all compile errors:
     

No Android SDK
    for i in */errors_compile.log; do cat $i; done | grep "ANDROID_SDK_ROOT" | wc -l

Unable to start Gradle daemon
    for i in */errors_compile.log; do cat $i; done | grep "Unable to start the daemon process" | wc -l

Unknown build tool
    for i in */worker.log; do cat $i; done | grep "Unknown Build Tool" | wc -l

Gradle build error count
    for i in */errors_compile.log; do cat $i; done | grep "Get more help at https://help.gradle.org" | wc -l

# SCRIPT ERRORS

Output all script errors:
    for i in */errors_shell.log; do cat $i; done

Analysis Results:
    for i in */errors_download.log; do cat $i; done


    for i in */worker.log; do cat $i; done | grep "zsh /opt/app/Repository_Miner/demo/CamBench_cov/scripts/execute_after_compile.sh Success" | wc -l

Gradle build error count
    for i in */worker.log; do cat $i; done | grep "Compile Success" | wc -l

    for i in */worker.log; do cat $i; done | grep "zsh /opt/app/Repository_Miner/demo/CamBench_cov/scripts/execute_after_download.sh Success" | wc -l


# Analysis
Get all available analysis results
    echo */analysis_results/ | tr ' ' '\n' | wc -l

Get all available analysis results
    echo */analysis_results/*/CryptoAnalysis-Report.json | tr ' ' '\n'

Number of Subsequent errors:
    for i in */analysis_results/*/CryptoAnalysis-Report.json; do grep -E '"preceding_error_ids" : .*[1234567890]+' $i ; done | wc -l
    for i in */analysis_results/*/CryptoAnalysis-Report.json; do grep -E '"subsequent_error_ids" : .*[1234567890]+' $i ; done | wc -l

Number of non Subsequent errors:
    for i in */analysis_results/*/CryptoAnalysis-Report.json; do grep '"preceding_error_ids" : \[ \]' $i ; done | wc -l

Multiple preceding errors:
    for i in */analysis_results/*/CryptoAnalysis-Report.json; do grep -E '"preceding_error_ids" : .*[1234567890]+,' $i ; done | wc -l
    for i in */analysis_results/*/CryptoAnalysis-Report.json; do grep -qE '"preceding_error_ids" : .*[1234567890]+,' $i && echo $i; done

Minimal Stargazers count
    for i in */github.json; do cat $i | tr ',' '\n' | grep stargazers_count | tr ' ' '\n'| tail -n1; done | sort -n | head -1


    for i in *; do grep "execute_after_compile.sh Success" $i/worker.log && mkdir "../test/$i" && cp "$i/worker.log" "../test/$i/worker.log" && cp -r "$i/analysis_results" "../test/$i/analysis_results"; done

    for i in */analysis_results/*; do TEST=$(echo $i | tr "analysis_results" | tr '/' '_') && mkdir ../test2/$TEST && cp -r $i ../test2/$TEST; done
    for i in */analysis_results/*; do TEST=$(echo ${i/\/analysis_results\//__}) && && mkdir ../test2/$TEST && cp -r $i ../test2/$TEST; done
    for i in */; do mv $i/$(ls $i)/* $i/* && rm -rf $i/$(ls $i); done
     for i in */; do echo $i; done
    mv * ../