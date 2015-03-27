FROM sunny:v2
MAINTAINER Jacopo Mauro

# install gecode
RUN apt-get update && \
  apt-get install -y flatzinc && \
  rm -rf /var/lib/apt/lists/*
COPY ./gecode /sunny-cp/solvers/gecode


# install choco
COPY ./choco_exec /solvers_exec/choco_exec
COPY ./choco /sunny-cp/solvers/choco
ENV PATH /solvers_exec/choco_exec:$PATH


# install haifacsp
COPY ./haifacsp_exec /solvers_exec/haifacsp_exec
COPY ./haifacsp /sunny-cp/solvers/haifacsp


# install izplus
COPY ./izplus_exec /solvers_exec/izplus_exec
COPY ./izplus /sunny-cp/solvers/izplus
ENV PATH /solvers_exec/izplus_exec:$PATH


# install minisatid
COPY ./minisatid_exec /solvers_exec/minisatid_exec
COPY ./minisatid /sunny-cp/solvers/minisatid
ENV PATH /solvers_exec/minisatid_exec:$PATH


# install ortools
COPY ./ortools_exec /solvers_exec/ortools_exec
COPY ./ortools /sunny-cp/solvers/ortools
ENV PATH /solvers_exec/ortools_exec:$PATH


RUN cd /sunny-cp && \
  sh install.sh


