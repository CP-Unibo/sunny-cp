FROM minizinc/mznc2019:1.0
MAINTAINER Jacopo Mauro & Tong Liu

# Install packages
RUN apt-get update && \
  apt-get install -y \
    python-dev \
    python-pip \
    # for gecode
    libgl1 \
    # for choco and jacop
    openjdk-8-jre-headless \
    wget \
    git \
    nano && \
  rm -rf /var/lib/apt/lists/*

# Install python modules
RUN pip install \
	psutil \
	click

# install feature extractor, sunny and basic solvers
COPY --from=jacopomauro/sunny-cp /tool /tool
ENV MZN2FEAT_HOME /tool/mzn2feat
ENV PATH /tool/mzn2feat/bin:$PATH
ENV PATH /tool/sunny-cp/bin:$PATH

# env variable for minisat
ENV LD_LIBRARY_PATH $LD_LIBRARY_PATH:/tool/minisatid/lib

# to add new solver copy all its directories in the right place
# COPY ... ...

RUN cd /tool/sunny-cp && \
    git pull && \
    bash install.sh

# update the mzn-exec scripts
RUN cp /tool/sunny-cp/minizinc_challenge/basic.sh /entry_data/exec && \
    echo "#!/bin/bash                              "  >  /minizinc/mzn-exec-par && \
    echo "/entry_data/exec \"\$@\"                 "  >> /minizinc/mzn-exec-par && \
    chmod a+x /minizinc/mzn-exec-par && \
    cp /minizinc/mzn-exec-par /minizinc/mzn-exec-free








