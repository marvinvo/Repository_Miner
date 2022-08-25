# TIMEOUT ERRORS
    for i in */worker.log; do cat $i; done | grep "Timeout" | wc -l

# COMPILE ERRORS

Output all compile errors:
    for i in */errors_compile.log; do cat $i; done

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

Gradle build error count
    for i in */worker.log; do cat $i; done | grep "zsh /opt/app/Repository_Miner/demo/CamBench_cov/scripts/execute_after_compile.sh Success" | wc -l
    