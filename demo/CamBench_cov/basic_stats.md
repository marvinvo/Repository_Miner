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

    for i in */errors_compile.log; do cat $i; done | grep "Memory"


     
# SCRIPT ERRORS

echo */*/ | tr ' ' '\n' | wc -l

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
    echo */analysis_results/*/CryptoAnalysis-Report.json | tr ' ' '\n'

Number of Subsequent errors:
    for i in */analysis_results/*/CryptoAnalysis-Report.json; do grep -E '"preceding_error_ids" : .*[1234567890]+' $i ; done | wc -l
    for i in */analysis_results/*/CryptoAnalysis-Report.json; do grep -E '"subsequent_error_ids" : .*[1234567890]+' $i ; done | wc -l

Number of non Subsequent errors:
    for i in */analysis_results/*/CryptoAnalysis-Report.json; do grep '"preceding_error_ids" : \[ \]' $i ; done | wc -l

Multiple preceding errors:
    for i in */analysis_results/*/CryptoAnalysis-Report.json; do grep -E '"preceding_error_ids" : .*[1234567890]+,' $i ; done | wc -l
    for i in */analysis_results/*/CryptoAnalysis-Report.json; do grep -E '"preceding_error_ids" : .*[1234567890]+,' $i && echo $i; done
    for i in */analysis_results/*/CryptoAnalysis-Report.json; do grep -E '"ruleId" : "IncompleteOperation' $i && echo $i; done

Minimal Stargazers count
    for i in */github.json; do cat $i | tr ',' '\n' | grep stargazers_count | tr ' ' '\n'| tail -n1; done | sort -n | tail -1


Reset analysis data
    for i in *; do grep "execute_after_compile.sh Success" $i/worker.log && cp $i/worker.log $i/worker.log.temp; done

    for i in */worker.log.temp; do sudo sed -i '/zsh\ /opt/app/Repository_Miner/demo/CamBench_cov/scripts/execute_after_compile.sh\ Success/d' $i; done

    sudo sh -c 'grep -v "zsh /opt/app/Repository_Miner/demo/CamBench_cov/scripts/execute_after_compile.sh Success" $i/worker.log > $i/worker.log.temp'; done



    for i in *; do grep "execute_after_compile.sh Success" $i/worker.log && sudo mv $i/analysis_results $i/analysis_results_old && sudo mv $i/worker.log $i/worker.log.old && sudo mv $i/worker.log.temp $i/worker.log; done


    for i in *; do grep "execute_after_compile.sh Success" $i/worker.log && mkdir "../test/$i" && cp "$i/worker.log" "../test/$i/worker.log" && cp "$i/github.json" "../test/$i/github.json" && cp -r "$i/analysis_results" "../test/$i/analysis_results"; done

    for i in */analysis_results/*; do TEST=$(echo $i | tr "analysis_results" | tr '/' '_') && mkdir ../test2/$TEST && cp -r $i ../test2/$TEST; done
    for i in */analysis_results/*; do TEST=$(echo ${i/\/analysis_results\//__}) && && mkdir ../test2/$TEST && cp -r $i ../test2/$TEST; done
    for i in */; do mv $i/$(ls $i)/* $i; done
     for i in */; do echo $i; done
    mv * ../



Analysis with predicate took 3356999 for total of 474 projects

Predicate took 8186270 ms for total of 1916 modules => 0,01 sec on average, 0,01 sec on median
Analysis without predicate took 8159474 ms for total of 1916 modules => 1,99 sec on average, 0,37 sec on median
Discovered analysis seeds within 4511389 ms for total of 1987 modules! => 2,27 sec on average, 1,16 sec on median

1912
Analysis took 34979.8 sec for 1837
Analysis took 135.92 min for 75 projects
=> 43135 sec => 22,6 sec on average, 17.58 on median


On Average, CallGraph construction took 16,06 sec, discover analysis seeds took 2,27 sec, Analysis and predicate propagation took 4,26 sec and subsequent error mapping took 0,01 sec.
On Median, 

SAST=0;\
SASTTOTAL=0;\
SUBS=0;\
SUBSTOTAL=0;\
SUBSON=0;\
SUBSONTOTAL=0;\
SUBSOFF=0;\
SUBSOFFTOTAL=0;\
POC=0;\
POCTOTAL=0;\
TOTAL=0;\
for folder in *; do \
if [ -f "$folder/sast.log" ]; then \
if [ -f "$folder/subs.log" ]; then \
if [ -f "$folder/poc.log" ]; then \
if [ -f "$folder/subson.log" ]; then \
if [ -f "$folder/subsoff.log" ]; then \
TOTALN=$(echo $folder/**/subs | tr ' ' '\n' | wc -l ); \
TOTAL=$(( $TOTAL + $TOTALN ));\
SASTN=$(cat $folder/sast.log | grep "Static Analysis took" | grep -oP "\d+" | paste -sd+ | bc); \
SASTTOTALN=$(cat $folder/sast.log | grep -c "Static Analysis took");\
SASTTOTAL=$(( $SASTTOTALN + $SASTTOTAL ));\
SUBSN=$(cat $folder/subs.log | grep "Static Analysis took" | grep -oP "\d+" | paste -sd+ | bc); \
SUBSTOTALN=$(cat $folder/subs.log | grep -c "Static Analysis took");\
SUBSTOTAL=$(( $SUBSTOTALN + $SUBSTOTAL ));\
SUBSNON=$(cat $folder/subson.log | grep "Static Analysis took" | grep -oP "\d+" | paste -sd+ | bc); \
SUBSONTOTALN=$(cat $folder/subson.log | grep -c "Static Analysis took");\
SUBSONTOTAL=$(( $SUBSONTOTALN + $SUBSONTOTAL ));\
SUBSNOFF=$(cat $folder/subsoff.log | grep "Static Analysis took" | grep -oP "\d+" | paste -sd+ | bc); \
SUBSOFFTOTALN=$(cat $folder/subsoff.log | grep -c "Static Analysis took");\
SUBSOFFTOTAL=$(( $SUBSOFFTOTALN + $SUBSOFFTOTAL ));\
POCN=$(cat $folder/poc.log | grep "Static Analysis took" | grep -oP "\d+" | paste -sd+ | bc); \
POCTOTALN=$(cat $folder/poc.log | grep -c "Static Analysis took");\
POCTOTAL=$(( $POCTOTALN + $POCTOTAL ));\
SAST=$(($SAST + SASTN)); \
SUBS=$((SUBS + SUBSN)); \
SUBSON=$((SUBSON + SUBSNON)); \
SUBSOFF=$((SUBSOFF + SUBSNOFF)); \
POC=$((POC + POCN)); \
fi \
fi \
fi \
fi \
fi \
done

SAST=0;\
SASTTOTAL=0;\
SUBS=0;\
SUBSTOTAL=0;\
SUBSON=0;\
SUBSONTOTAL=0;\
SUBSOFF=0;\
SUBSOFFTOTAL=0;\
POC=0;\
POCTOTAL=0;\
TOTAL=0;\
STRING="Analysis finished in";\
for folder in *; do \
if [ -f "$folder/sast.log" ]; then \
if [ -f "$folder/subs.log" ]; then \
if [ -f "$folder/poc.log" ]; then \
if [ -f "$folder/subson.log" ]; then \
if [ -f "$folder/subsoff.log" ]; then \
TOTALN=$(echo $folder/**/subs | tr ' ' '\n' | wc -l ); \
TOTAL=$(( $TOTAL + $TOTALN ));\
SASTN=$(cat $folder/sast.log | grep "$STRING" | grep -oP "\d+" | paste -sd+ | bc); \
SASTTOTALN=$(cat $folder/sast.log | grep -c "$STRING");\
SASTTOTAL=$(( $SASTTOTALN + $SASTTOTAL ));\
SUBSN=$(cat $folder/subs.log | grep "$STRING"| grep -oP "\d+" | paste -sd+ | bc); \
SUBSTOTALN=$(cat $folder/subs.log | grep -c "$STRING");\
SUBSTOTAL=$(( $SUBSTOTALN + $SUBSTOTAL ));\
SUBSNON=$(cat $folder/subson.log | grep "$STRING" | grep -oP "\d+" | paste -sd+ | bc); \
SUBSONTOTALN=$(cat $folder/subson.log | grep -c "$STRING");\
SUBSONTOTAL=$(( $SUBSONTOTALN + $SUBSONTOTAL ));\
SUBSNOFF=$(cat $folder/subsoff.log | grep "$STRING" | grep -oP "\d+" | paste -sd+ | bc); \
SUBSOFFTOTALN=$(cat $folder/subsoff.log | grep -c "$STRING");\
SUBSOFFTOTAL=$(( $SUBSOFFTOTALN + $SUBSOFFTOTAL ));\
POCN=$(cat $folder/poc.log | grep "$STRING" | grep -oP "\d+" | paste -sd+ | bc); \
POCTOTALN=$(cat $folder/poc.log | grep -c "$STRING");\
POCTOTAL=$(( $POCTOTALN + $POCTOTAL ));\
SAST=$(($SAST + SASTN)); \
SUBS=$((SUBS + SUBSN)); \
SUBSON=$((SUBSON + SUBSNON)); \
SUBSOFF=$((SUBSOFF + SUBSNOFF)); \
POC=$((POC + POCN)); \
fi \
fi \
fi \
fi \
fi \
done



Analysis soot setup done in \d+(\.\d+)?


STRING="analysis seeds within \d+";\
for folder in *; do \
if [ -f "$folder/sast.log" ]; then \
if [ -f "$folder/subs.log" ]; then \
if [ -f "$folder/poc.log" ]; then \
if [ -f "$folder/subson.log" ]; then \
if [ -f "$folder/subsoff.log" ]; then \
cat $folder/sast.log | grep -oP "$STRING" | grep -oP "\d+(\.\d+)?" >> sast.stats; \
cat $folder/subs.log | grep -oP "$STRING" | grep -oP "\d+(\.\d+)?" >> subs.stats; \
cat $folder/subsoff.log | grep -oP "$STRING" | grep -oP "\d+(\.\d+)?" >> subsoff.stats; \
cat $folder/subson.log | grep -oP "$STRING" | grep -oP "\d+(\.\d+)?" >> subson.stats;\
cat $folder/poc.log | grep -oP "$STRING" | grep -oP "\d+(\.\d+)?" >> poc.stats; \
fi \
fi \
fi \
fi \
fi \
done
cat $folder/sast.log | grep -P "$STRING s" | grep -oP "\d+(\.\d+)?"; \
cat $folder/subs.log | grep "$STRING"| grep -oP "\d+(\.\d+)?"  >> subs.stats; \
cat $folder/subson.log | grep "$STRING" | grep -oP "\d+" >> subson.stats; \
cat $folder/subsoff.log | grep "$STRING"| grep -oP "\d+"  >> subsoff.stats; \
cat $folder/poc.log | grep "$STRING" | grep -oP "\d+" >> poc.stats; \

SAST=0;\
SUBS=0;\
SUBSON=0;\
SUBSOFF=0;\
POC=0;\
TOTAL=0;\
for folder in *; do \
if [ -f "$folder/sast.log" ]; then \
if [ -f "$folder/subs.log" ]; then \
if [ -f "$folder/poc.log" ]; then \
if [ -f "$folder/subson.log" ]; then \
if [ -f "$folder/subsoff.log" ]; then \
TOTAL=$(( $TOTAL + 1 ));\
SASTN=$(cat $folder/sast.log |  grep -oP "analysis seeds within \d+" | grep -oP "\d+" | paste -sd+ | bc); \
SUBSN=$(cat $folder/subs.log | grep -oP "analysis seeds within \d+" | grep -oP "\d+" | paste -sd+ | bc); \
SUBSNON=$(cat $folder/subson.log |  grep -oP "analysis seeds within \d+" | grep -oP "\d+" | paste -sd+ | bc); \
SUBSNOFF=$(cat $folder/subsoff.log |  grep -oP "analysis seeds within \d+" | grep -oP "\d+" | paste -sd+ | bc); \
POCN=$(cat $folder/poc.log |  grep -oP "analysis seeds within \d+" | grep -oP "\d+" | paste -sd+ | bc); \
SAST=$(($SAST + SASTN)); \
SUBS=$((SUBS + SUBSN)); \
SUBSON=$((SUBSON + SUBSNON)); \
SUBSOFF=$((SUBSOFF + SUBSNOFF)); \
POC=$((POC + POCN)); \
fi \
fi \
fi \
fi \
fi \
done

SAST=0;\
SUBS=0;\
SUBSON=0;\
SUBSOFF=0;\
POC=0;\
TOTAL=0;\
for folder in *; do \
if [ -f "$folder/sast.log" ]; then \
if [ -f "$folder/subs.log" ]; then \
if [ -f "$folder/poc.log" ]; then \
if [ -f "$folder/subson.log" ]; then \
if [ -f "$folder/subsoff.log" ]; then \
TOTAL=$(( $TOTAL + 1 ));\
SASTN=$(cat $folder/sast.log |  grep -c "analysis seeds within"); \
SUBSN=$(cat $folder/subs.log | grep -c "analysis seeds within"); \
SUBSNON=$(cat $folder/subson.log |  grep -c  "analysis seeds within"); \
SUBSNOFF=$(cat $folder/subsoff.log |  grep -c  "analysis seeds within"); \
POCN=$(cat $folder/poc.log |  grep -c "analysis seeds within"); \
SAST=$(($SAST + SASTN)); \
SUBS=$((SUBS + SUBSN)); \
SUBSON=$((SUBSON + SUBSNON)); \
SUBSOFF=$((SUBSOFF + SUBSNOFF)); \
POC=$((POC + POCN)); \
fi \
fi \
fi \
fi \
fi \
done

SAST=0;\
SUBS=0;\
SUBSON=0;\
SUBSOFF=0;\
POC=0;\
TOTAL=0;\
for folder in *; do \
if [ -f "$folder/sast.log" ]; then \
if [ -f "$folder/subs.log" ]; then \
if [ -f "$folder/poc.log" ]; then \
if [ -f "$folder/subson.log" ]; then \
if [ -f "$folder/subsoff.log" ]; then \
TOTAL=$(( $TOTAL + 1 ));\
SASTN=$(cat $folder/sast.log |  grep -oP "\d+ analysis seeds within" | grep -oP "\d+" | paste -sd+ | bc); \
SUBSN=$(cat $folder/subs.log | grep -oP "\d+ analysis seeds within"| grep -oP "\d+" | paste -sd+ | bc); \
SUBSNON=$(cat $folder/subson.log |  grep -oP "\d+ analysis seeds within"| grep -oP "\d+" | paste -sd+ | bc); \
SUBSNOFF=$(cat $folder/subsoff.log |  grep -oP "\d+ analysis seeds within" | grep -oP "\d+" | paste -sd+ | bc); \
POCN=$(cat $folder/poc.log |  grep -oP "\d+ analysis seeds within" | grep -oP "\d+" | paste -sd+ | bc); \
SAST=$(($SAST + SASTN)); \
SUBS=$((SUBS + SUBSN)); \
SUBSON=$((SUBSON + SUBSNON)); \
SUBSOFF=$((SUBSOFF + SUBSNOFF)); \
POC=$((POC + POCN)); \
fi \
fi \
fi \
fi \
fi \
done

########
########
########

SAST=0;\
SUBS=0;\
POC=0;\
TOTAL=0;\
for folder in *; do \
if [ -f "$folder/sast.log" ]; then \
if [ -f "$folder/subs.log" ]; then \
if [ -f "$folder/poc.log" ]; then \
TOTAL=$(( $TOTAL + 1 ));\
SASTN=$(cat $folder/sast.log | grep -oP "analysis seeds within \d+" | grep -oP "\d+" | paste -sd+ | bc); \
SUBSN=$(cat $folder/subs.log |  grep -oP "analysis seeds within \d+" | grep -oP "\d+" | paste -sd+ | bc); \
POCN=$(cat $folder/poc.log | grep -oP "analysis seeds within \d+" | grep -oP "\d+" | paste -sd+ | bc); \
SAST=$(($SAST + SASTN)); \
SUBS=$((SUBS + SUBSN)); \
POC=$((POC + POCN)); \
fi \
fi \
fi \
done



SAST=0;\
SUBS=0;\
POC=0;\
TOTAL=0;\
for folder in *; do \
if [ -f "$folder/sast.log" ]; then \
if [ -f "$folder/subs.log" ]; then \
if [ -f "$folder/poc.log" ]; then \
TOTAL=$(( $TOTAL + 1 ));\
SASTN=$(cat $folder/sast.log | grep "Analysis soot setup done in " | grep -oP "\d+" | paste -sd+ | bc); \
SUBSN=$(cat $folder/subs.log | grep "Analysis soot setup done in " | grep -oP "\d+" | paste -sd+ | bc); \
POCN=$(cat $folder/poc.log | grep "Analysis soot setup done in " | grep -oP "\d+" | paste -sd+ | bc); \
SAST=$(($SAST + SASTN)); \
SUBS=$((SUBS + SUBSN)); \
POC=$((POC + POCN)); \
fi \
fi \
fi \
done

SAST=0;\
SUBS=0;\
POC=0;\
TOTAL=0;\
for folder in *; do \
if [ -f "$folder/sast.log" ]; then \
if [ -f "$folder/subs.log" ]; then \
if [ -f "$folder/poc.log" ]; then \
TOTAL=$(( $TOTAL + 1 ));\
SASTN=$(cat $folder/sast.log | grep -c "Analysis soot setup done in "); \
SUBSN=$(cat $folder/subs.log | grep -c "Analysis soot setup done in "); \
POCN=$(cat $folder/poc.log | grep -c "Analysis soot setup done in "); \
SAST=$(($SAST + SASTN)); \
SUBS=$((SUBS + SUBSN)); \
POC=$((POC + POCN)); \
fi \
fi \
fi \
done


SAST=0;\
SUBS=0;\
POC=0;\
TOTAL=0;\
for folder in *; do \
if [ -f "$folder/sast.log" ]; then \
if [ -f "$folder/subs.log" ]; then \
if [ -f "$folder/poc.log" ]; then \
TOTAL=$(( $TOTAL + 1 ));\
SASTN=$(cat $folder/sast.log | grep -c "Static Analysis took "); \
SUBSN=$(cat $folder/subs.log | grep -c "Static Analysis took "); \
POCN=$(cat $folder/poc.log | grep -c "Static Analysis took "); \
SAST=$(($SAST + SASTN)); \
SUBS=$((SUBS + SUBSN)); \
POC=$((POC + POCN)); \
fi \
fi \
fi \
done


SAST=0;\
SUBS=0;\
POC=0;\
TOTAL=0;\
for folder in *; do \
if [ -f "$folder/sast.log" ]; then \
if [ -f "$folder/subs.log" ]; then \
if [ -f "$folder/poc.log" ]; then \
TOTAL=$(( $TOTAL + 1 ));\
SASTN=$(cat $folder/sast.log | grep -c "Analysis soot setup done in "); \
SUBSN=$(cat $folder/subs.log | grep -c "Analysis soot setup done in "); \
POCN=$(cat $folder/poc.log | grep -c "Analysis soot setup done in "); \
SAST=$(($SAST + SASTN)); \
SUBS=$((SUBS + SUBSN)); \
POC=$((POC + POCN)); \
fi \
fi \
fi \
done



for folder in *; do \
if [ -f "$folder/sast.log" ]; then \
if [ -f "$folder/subs.log" ]; then \
if [ -f "$folder/poc.log" ]; then \
mkdir "../test/$folder"; \
cp "$folder/sast.log" "../test/$folder/sast.log"; \
cp "$folder/subs.log" "../test/$folder/subs.log"; \
cp "$folder/poc.log" "../test/$folder/poc.log"; \
cp -r "$folder/sast_and_subspoc_analysis_results/" "../test/$folder/sast_and_subspoc_analysis_results"; \
fi \
fi \
fi\
done