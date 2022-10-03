FROM alpine:latest

# install dependencies
RUN apk update
RUN apk add git &&\
 apk add bash &&\
 apk add maven &&\
 apk add python3 &&\
 apk add gradle &&\
 apk add openjdk8 &&\
 apk add openjdk11 &&\
 apk add py3-pip &&\
 pip install requests &&\
 apk add zsh

# set workdir
WORKDIR /opt/app

# get Repository Miner
RUN git clone https://github.com/marvinvo/Repository_Miner.git;

# get RepoReaper
RUN git clone https://github.com/RepoReapers/reaper.git;

ENV REPOREAPER=/opt/app/reaper/batch_score.py

ENV REPOMINER=/opt/app/Repository_Miner/main.py

# copy files to workdir
COPY . .

# Settings for Repository Miner
ENV GITHUB_TOKENS="/opt/app/CREDENTIALS.txt"
ENV RESULTS_FOLDER="/opt/app/results"
ENV MAX_PROCESSES="1"

# Settings for Repository Reaper

# replace execute_on_success.sh with script that invokes CC_SUBS
RUN mv "/opt/app/run_cc_subs.sh" "/opt/app/Repository_Miner/demo/CamBench_cov/scripts/execute_on_success.sh"

WORKDIR /opt/app/Repository_Miner/demo/CamBench_cov
# run the scan
CMD zsh $CAMBENCH_COV