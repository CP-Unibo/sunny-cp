FROM minizinc/mznc2018:1.0
MAINTAINER Jacopo Mauro

# Install packages
RUN apt-get update && \
  apt-get install -y \
    python-dev \
    python-pip \
    openjdk-8-jre-headless \
    wget \
    nano && \
  rm -rf /var/lib/apt/lists/*

# Install python modules
RUN pip install \
	psutil \
	click

# install feature extractor
COPY --from=jacopomauro/sunny-cp /mzn2feat /mzn2feat
ENV MZN2FEAT_HOME /mzn2feat
ENV PATH /mzn2feat/bin:$PATH

# install basic sunny-cp
COPY --from=jacopomauro/sunny-cp /sunny-cp /sunny-cp
COPY --from=jacopomauro/sunny-cp /solvers_exec /solvers_exec
ENV PATH /sunny-cp/bin:$PATH

# update ortools (from Debian to Ubuntu 16.04 version)
# note: latest version does not work since globals are differentiated from cp and sat modality
RUN cd /solvers_exec && \
    rm -rf ortools && \
	wget https://github.com/google/or-tools/releases/download/v6.4/or-tools_flatzinc_Ubuntu-16.04-64bit_v6.4.4495.tar.gz && \
	tar xvfz or-tools_flatzinc_Ubuntu-16.04-64bit_v6.4.4495.tar.gz && \
	rm or-tools_flatzinc_Ubuntu-16.04-64bit_v6.4.4495.tar.gz && \
	mv or-tools_flatzinc_Ubuntu-16.04-64bit_v6.4.4495 ortools

# env variable for minisat
ENV LD_LIBRARY_PATH $LD_LIBRARY_PATH:/solvers_exec/minisatid/lib

# to add new solver copy all its directories in the right place
# COPY ... ...

# update the mzn-exec scripts
RUN echo $'#!/bin/bash \n\
sunny-cp -f "$@" \n' > /minizinc/mzn-exec-par && \
echo $'#!/bin/bash \n\
sunny-cp -f "$@" \n' > /minizinc/mzn-exec-free

RUN cd /sunny-cp && \
    bash install.sh




