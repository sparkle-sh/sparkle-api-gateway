FROM ubuntu:latest
RUN apt-get update && apt-get install -y \ 
    software-properties-common sudo tmux vim wget curl
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update

WORKDIR /sparkle-api-gateway/
COPY . /sparkle-api-gateway/

RUN yes | ./bin/deps.sh
RUN yes | ./bin/venv.sh

EXPOSE 7775