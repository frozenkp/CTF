# This is a dockerfile for pwn environment.
# Last update: 2018/03/12
# version 1.0.3

# Run command:
# docker run -it {--name pwn_env} {-v /??/data:/root/data} --cap-add=SYS_PTRACE --security-opt seccomp=unconfined frozenkp/pwn /bin/bash

FROM ubuntu

MAINTAINER frozenkp

WORKDIR /root

RUN apt-get update ; apt-get install -y git tmux gdb vim binutils python python-pip python-dev libssl-dev libffi-dev build-essential rubygems netcat nmap
# pwntools
RUN pip install --upgrade pip ; pip install --upgrade pwntools

# peda
RUN git clone https://github.com/longld/peda.git ~/peda ; echo "source ~/peda/peda.py" >> ~/.gdbinit

# pwngdb
RUN git clone https://github.com/scwuaptx/Pwngdb.git ; cp ~/Pwngdb/.gdbinit ~/

# onegadget
RUN gem install one_gadget

