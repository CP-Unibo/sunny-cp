FROM sunny:v2
MAINTAINER Jacopo Mauro

# install gecode
RUN apt-get update && \
  apt-get install -y flatzinc && \
  rm -rf /var/lib/apt/lists/*
COPY ./gecode /sunny-cp/solvers/gecode

# install gecode from sources
# cd /solvers_exec
# wget http://www.gecode.org/download/gecode-4.4.0.tar.gz
# tar -zxvf gecode-4.4.0.tar.gz
# cd gecode-4.4.0
# ./configure ./configure --disable-examples --disable-set-vars
# make depend
# make flatzinc
# ENV PATH /solvers_exec/gecode-4.4.0/tools/flatzinc:$PATH
# COPY ./gecode /sunny-cp/solvers/gecode



# install choco
COPY ./choco_exec /solvers_exec/choco_exec
COPY ./choco /sunny-cp/solvers/choco
ENV PATH /solvers_exec/choco_exec:$PATH


# install haifacsp
COPY ./haifacsp_exec /solvers_exec/haifacsp_exec
COPY ./haifacsp /sunny-cp/solvers/haifacsp


# install izplus
# updated 06192015
COPY ./izplus_exec /solvers_exec/izplus_exec
COPY ./izplus /sunny-cp/solvers/izplus
ENV PATH /solvers_exec/izplus_exec:$PATH


# install minisatid
COPY ./minisatid_exec /solvers_exec/minisatid_exec
COPY ./minisatid /sunny-cp/solvers/minisatid
ENV PATH /solvers_exec/minisatid_exec:$PATH

# install minisatid from sources
# cd /solvers_exec
# wget https://dtai.cs.kuleuven.be/krr/files/software/minisatid/minisatid-3.11.0-source.zip
# unzip minisatid-3.11.0-source.zip
# mkidr minisatid_exec
# cd minisatid_exec
# cmake /solvers_exec/krr-minisatid-869bec4a8bfb -DCMAKE_INSTALL_PREFIX=./ -DCMAKE_BUILD_TYPE="Release"
# make -j 4
# make test
# make install
# rm -rf /solvers_exec/krr-minisatid-869bec4a8bfb
# rm -rf /solvers_exec/minisatid-3.11.0-source.zip
# COPY ./minisatid /sunny-cp/solvers/minisatid
# change version number 3.11.0
# ENV PATH /solvers_exec/minisatid_exec/bin:$PATH

# install ortools
COPY ./ortools_exec /solvers_exec/ortools_exec
COPY ./ortools /sunny-cp/solvers/ortools
ENV PATH /solvers_exec/ortools_exec:$PATH


RUN cd /sunny-cp && \
  sh install.sh


