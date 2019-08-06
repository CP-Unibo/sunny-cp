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

# update ortools (from Debian to Ubuntu 16.04 version)
# note: latest version does not work since globals are differentiated from cp and sat modality
# RUN cd /solvers_exec && \
#     rm -rf ortools && \
# 	wget https://github.com/google/or-tools/releases/download/v6.4/or-tools_flatzinc_Ubuntu-16.04-64bit_v6.4.4495.tar.gz && \
# 	tar xvfz or-tools_flatzinc_Ubuntu-16.04-64bit_v6.4.4495.tar.gz && \
# 	rm or-tools_flatzinc_Ubuntu-16.04-64bit_v6.4.4495.tar.gz && \
# 	mv or-tools_flatzinc_Ubuntu-16.04-64bit_v6.4.4495 ortools


# to add new solver copy all its directories in the right place
# COPY ... ...

RUN cd /tool/sunny-cp && \
    git pull && \
    bash install.sh

# update the mzn-exec scripts
RUN cp /tool/sunny-cp/minizinc_challenge/basic.sh /entry_data/exec





