FROM sunny:v2
MAINTAINER Jacopo Mauro

# install gecode
# updated 2014
RUN apt-get update && \
  apt-get install -y flatzinc && \
  rm -rf /var/lib/apt/lists/*
COPY ./gecode /sunny-cp/solvers/gecode

# install gecode from sources (version 4.4.0)
# cd /solvers_exec
# wget http://www.gecode.org/download/gecode-4.4.0.tar.gz
# tar -zxvf gecode-4.4.0.tar.gz
# cd gecode-4.4.0
#  ./configure --disable-examples --disable-set-vars --prefix=/solvers_exec/gecode-4.4.0
# make
# make install 
# ENV PATH /solvers_exec/gecode-4.4.0/bin:$PATH
# ENV LD_LIBRARY_PATH=/solvers_exec/gecode-4.4.0/lib:$LD_LIBRARY_PATH
# COPY ./gecode /sunny-cp/solvers/gecode



# install choco (version 3.3.0 that attended the MiniZinc Challenge 2014)
# updated 20141209
COPY ./choco_exec /solvers_exec/choco_exec
RUN cd /solvers_exec/choco_exec && \
  wget https://github.com/chocoteam/choco-parsers/releases/download/choco-parsers-3.3.0/choco-parsers-3.3.0-with-dependencies.jar
COPY ./choco /sunny-cp/solvers/choco
ENV PATH /solvers_exec/choco_exec:$PATH


# install haifacsp
# updated 2014
COPY ./haifacsp_exec /solvers_exec/haifacsp_exec
COPY ./haifacsp /sunny-cp/solvers/haifacsp
#
# updated 20150716
# COPY ./haifacsp /sunny-cp/solvers/haifacsp


# install izplus
# updated 20150619
COPY ./izplus_exec /solvers_exec/izplus_exec
COPY ./izplus /sunny-cp/solvers/izplus
ENV PATH /solvers_exec/izplus_exec:$PATH


# install minisatid
# updated 2014
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
# updated 20150706
COPY ./ortools_exec /solvers_exec/ortools_exec
COPY ./ortools /sunny-cp/solvers/ortools
ENV PATH /solvers_exec/ortools_exec:$PATH


RUN cd /sunny-cp && \
  sh install.sh


