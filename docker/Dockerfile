FROM python:2-stretch
MAINTAINER Jacopo Mauro

# expose port 9001 for the sunny-cp server
EXPOSE 9001

# Install python modules
RUN pip install \
	psutil \
	click

# Install packages for compiling the feature extractor and minizin suite
RUN apt-get update && \
  apt-get install -y \
    flex \
		bison \
		nano \
		libqt5core5a \
    libqt5gui5 \
    libqt5network5 \
    libqt5webkit5 \
    libqt5widgets5 && \
  rm -rf /var/lib/apt/lists/*

# Install minizinc suite
RUN cd / && \
  wget https://github.com/MiniZinc/MiniZincIDE/releases/download/2.1.6/MiniZincIDE-2.1.6-bundle-linux-x86_64.tgz && \
  tar -zxvf MiniZincIDE-2.1.6-bundle-linux-x86_64.tgz && \
  rm -rf MiniZincIDE-2.1.6-bundle-linux-x86_64.tgz && \
	mv MiniZincIDE-2.1.6-bundle-linux-x86_64 minizinc
ENV PATH /minizinc:$PATH

# Install feature extractor
RUN cd / && \
  git clone -b server --depth=1 https://github.com/CP-Unibo/sunny-cp.git && \
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
CMD ["python","/sunny-cp/src/sunny_server.py"]

# Install ortools
RUN ( [ -d /solvers_exec ] || mkdir /solvers_exec ) && \
	cd /solvers_exec && \
	wget https://github.com/google/or-tools/releases/download/v6.4/or-tools_flatzinc_Debian-9.1-64bit_v6.4.4495.tar.gz && \
	tar xvfz or-tools_flatzinc_Debian-9.1-64bit_v6.4.4495.tar.gz && \
	rm or-tools_flatzinc_Debian-9.1-64bit_v6.4.4495.tar.gz && \
	mv or-tools_flatzinc_Debian-9.1-64bit_v6.4.4495 ortools_exec && \
  cd /sunny-cp && bash install

# Install choco
RUN apt-get update && \
		apt-get install -y openjdk-8-jre-headless && \
		rm -rf /var/lib/apt/lists/*
RUN ( [ -d /solvers_exec ] || mkdir /solvers_exec ) && \
	cd /solvers_exec && \
  mkdir choco_exec && \
	cd choco_exec && \
	wget https://github.com/chocoteam/choco-parsers/releases/download/choco-parsers-4.0.4/choco-parsers-4.0.4-with-dependencies.jar && \
  cd /sunny-cp && bash install

# Install picat
RUN ( [ -d /solvers_exec ] || mkdir /solvers_exec ) && \
	wget http://picat-lang.org/download/picat22_linux64.tar.gz  && \
	cd /solvers_exec && \
	mv picat22_linux64 picat && \
	cd picat && \
	wget http://picat-lang.org/flatzinc/fzn_picat_sat.pi  && \
	wget http://picat-lang.org/flatzinc/fzn_picat_cp.pi  && \
	wget http://picat-lang.org/flatzinc/fzn_parser.pi  && \
	wget http://picat-lang.org/flatzinc/fzn_tokenizer.pi  && \
  cd /sunny-cp && bash install

