FROM python:2-onbuild
MAINTAINER Jacopo Mauro

# last updated 20150820
# build image invoking the command
# sudo docker build -t sunny:g12 ./base_dockerfile/

# install minizinc suite
RUN cd / && \
  wget https://github.com/MiniZinc/libminizinc/releases/download/2.0.6/minizinc-2.0.6-linux64.tar.gz && \
  tar -zxvf minizinc-2.0.6-linux64.tar.gz && \
  rm -rf minizinc-2.0.6-linux64.tar.gz
ENV PATH /minizinc-2.0.6/bin:$PATH


# install packages for compiling the feature extractor
RUN apt-get update && \
  apt-get install -y flex bison && \
  rm -rf /var/lib/apt/lists/*

    
# install feature extractor
RUN cd / && \
  git clone --depth=1 https://github.com/CP-Unibo/sunny-cp && \
  cd /sunny-cp && \
  tar -xjvf mzn2feat-1.1.2.tar.bz2 && \
  cd /sunny-cp/mzn2feat && \
  bash install --no-xcsp
ENV MZN2FEAT_HOME /sunny-cp/mzn2feat
ENV PATH /sunny-cp/mzn2feat/bin:$PATH


# install sunny-cp
RUN cd /sunny-cp && \
  bash install
ENV SUNNY_HOME /sunny-cp
ENV PATH /sunny-cp/bin:$PATH


WORKDIR /sunny-cp
ENTRYPOINT ["sunny-cp", "--g12"]

