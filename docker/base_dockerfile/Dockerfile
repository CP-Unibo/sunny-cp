FROM python:2-onbuild
MAINTAINER Jacopo Mauro

# install minizinc suite
RUN cd / && \
  wget http://www.minizinc.org/downloads/release-1.6/minizinc-1.6-x86_64-unknown-linux-gnu.tar.gz && \
  tar -zxvf minizinc-1.6-x86_64-unknown-linux-gnu.tar.gz && \
  rm -rf minizinc-1.6-x86_64-unknown-linux-gnu.tar.gz && \
  cd /minizinc-1.6 && \
  ./SETUP
ENV PATH /minizinc-1.6/bin:$PATH


# install packages for compiling the feature extractor
RUN apt-get update && \
  apt-get install -y flex bison && \
  rm -rf /var/lib/apt/lists/*

    
# install feature extractor
RUN cd / && \
  git clone https://github.com/jacopoMauro/sunny-cp.git && \
  cd /sunny-cp && \
  tar -xjvf mzn2feat-1.0.tar.bz2 && \
  cd /sunny-cp/mzn2feat && \
  sh install.sh   
ENV MZN2FEAT_HOME /sunny-cp/mzn2feat
ENV PATH /sunny-cp/mzn2feat/bin:$PATH


# install sunny-cp
RUN cd /sunny-cp && \
  sh install.sh
ENV SUNNY_HOME /sunny-cp
ENV PATH /sunny-cp/bin:$PATH


WORKDIR /sunny-cp
ENTRYPOINT ["sunny-cp"]


