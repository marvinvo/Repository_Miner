# 1 - set base image
FROM alpine:3.15.6

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
 apk add curl &&\
 pip install requests &&\
 apk add zsh

# set workdir
WORKDIR /opt/app

# get Repository Miner
RUN git clone https://github.com/marvinvo/Repository_Miner.git;
ENV CAMBENCH_REAL=/opt/app/cambench_real.sh

# copy files to workdir
COPY . .

ENV GITHUB_TOKENS="/opt/app/CREDENTIALS.txt" \
    RESULTS_FOLDER="/opt/app/Repository_Miner/demo/CamBench_real/dataset" \
    MAX_PROCESSES=20 \
    MEMORY_JAVA="3G" \ 
    STACKSIZE_JAVA="2M" \
    LASTSORT=99999999 \
    TOOLS="/opt/app/Repository_Miner/demo/CamBench_real/tools"


# required by the shell scripts
WORKDIR /opt/app/Repository_Miner/demo/CamBench_real

# run the scan
CMD zsh $CAMBENCH_REAL