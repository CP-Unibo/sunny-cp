FROM sunny:v1
MAINTAINER Jacopo Mauro

# install gecode
RUN apt-get update && \
  apt-get install -y flatzinc && \
  rm -rf /var/lib/apt/lists/*
COPY ./gecode /sunny-cp/solvers/gecode


RUN cd /sunny-cp && \
  sh install.sh


