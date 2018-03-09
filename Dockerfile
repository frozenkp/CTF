# This is a dockerfile for pwn environment.
# Last update: 2018/03/10

FROM ubuntu

MAINTAINER frozenkp

WORKDIR /root

RUN apt-get update
RUN apt-get install -y git tmux gdb vim binutils python python-pip python-dev libssl-dev libffi-dev build-essential rubygems

# pwntools
RUN pip install --upgrade pip & pip install --upgrade pwntools

# peda
RUN git clone https://github.com/longld/peda.git ~/peda
RUN echo "source ~/peda/peda.py" >> ~/.gdbinit

# pwngdb
RUN git clone https://github.com/scwuaptx/Pwngdb.git
RUN cp ~/Pwngdb/.gdbinit ~/

# onegadget
RUN gem install one_gadget

