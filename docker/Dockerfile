FROM python:2-onbuild
MAINTAINER Jacopo Mauro

# Install minizinc suite
RUN cd / && \
  wget https://github.com/MiniZinc/MiniZincIDE/releases/download/2.0.14/MiniZincIDE-2.0.14-bundle-linux-x86_64.tgz && \
  tar -zxvf MiniZincIDE-2.0.14-bundle-linux-x86_64.tgz && \
  rm -rf MiniZincIDE-2.0.14-bundle-linux-x86_64.tgz && \
	mv MiniZincIDE-2.0.14-bundle-linux-x86_64 minizinc
ENV PATH /minizinc:$PATH


# Install packages for compiling the feature extractor
RUN apt-get update && \
  apt-get install -y flex bison qt5-default && \
  rm -rf /var/lib/apt/lists/*

    
# Install feature extractor
RUN cd / && \
  git clone --depth=1 https://github.com/CP-Unibo/sunny-cp.git && \
  cd /sunny-cp && \
  tar -xjvf mzn2feat-1.2.1.tar.bz2 && \
  cd /sunny-cp/mzn2feat && \
  bash install --no-xcsp
ENV MZN2FEAT_HOME /sunny-cp/mzn2feat
ENV PATH /sunny-cp/mzn2feat/bin:$PATH


# install sunny-cp
RUN cd /sunny-cp && bash install
ENV PATH /sunny-cp/bin:$PATH
WORKDIR /sunny-cp
ENTRYPOINT ["sunny-cp"]
