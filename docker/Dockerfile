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

# Install ortools
RUN ( [ -d /solvers_exec ] || mkdir /solvers_exec ) && \
	cd /solvers_exec && \
	wget https://github.com/google/or-tools/releases/download/v6.4/or-tools_flatzinc_Debian-9.1-64bit_v6.4.4495.tar.gz && \
	tar xvfz or-tools_flatzinc_Debian-9.1-64bit_v6.4.4495.tar.gz && \
	rm or-tools_flatzinc_Debian-9.1-64bit_v6.4.4495.tar.gz && \
	mv or-tools_flatzinc_Debian-9.1-64bit_v6.4.4495 ortools

# Install choco
RUN apt-get update && \
		apt-get install -y openjdk-8-jre-headless && \
		rm -rf /var/lib/apt/lists/*
RUN ( [ -d /solvers_exec ] || mkdir /solvers_exec ) && \
	cd /solvers_exec && \
  mkdir choco && \
	cd choco && \
	wget https://github.com/chocoteam/choco-parsers/releases/download/choco-parsers-4.0.4/choco-parsers-4.0.4-with-dependencies.jar

# Install picat
RUN ( [ -d /solvers_exec ] || mkdir /solvers_exec ) && \
	cd /solvers_exec && \
	wget http://picat-lang.org/download/picat22_linux64.tar.gz  && \
	tar xvfz picat22_linux64.tar.gz && \
	rm picat22_linux64.tar.gz && \
	mv Picat picat && \
	cd picat && \
	wget http://picat-lang.org/flatzinc/fzn_picat_sat.pi  && \
	wget http://picat-lang.org/flatzinc/fzn_picat_cp.pi  && \
	wget http://picat-lang.org/flatzinc/fzn_parser.pi  && \
	wget http://picat-lang.org/flatzinc/fzn_tokenizer.pi

# Install jacop
RUN apt-get update && \
		apt-get install -y openjdk-8-jre-headless && \
		rm -rf /var/lib/apt/lists/*
RUN ( [ -d /solvers_exec ] || mkdir /solvers_exec ) && \
	cd /solvers_exec && \
	mkdir jacop && \
	cd jacop && \
	wget http://central.maven.org/maven2/org/jacop/jacop/4.4.0/jacop-4.4.0.jar

# Install minisat
RUN ( [ -d /solvers_exec ] || mkdir /solvers_exec ) && \
	cd /solvers_exec && \
	wget https://dtai.cs.kuleuven.be/krr/files/software/minisatid/minisatid-3.11.0-Linux.tar.gz && \
	gzip -d minisatid-3.11.0-Linux.tar.gz && \
	tar -xvf minisatid-3.11.0-Linux.tar && \
	mv minisatid-3.11.0-Linux minisatid && \
	rm minisatid-3.11.0-Linux.tar
ENV LD_LIBRARY_PATH $LD_LIBRARY_PATH:/solvers_exec/minisatid/lib

# Install haifacsp
RUN ( [ -d /solvers_exec ] || mkdir /solvers_exec ) && \
	cd /solvers_exec && \
	wget --no-check-certificate http://ie.technion.ac.il/~ofers/HCSP/hcsp-1.3.0-x86_64.tar.xz && \
	tar -xJf hcsp-1.3.0-x86_64.tar.xz && \
	mv hcsp-1.3.0-x86_64 haifacsp && \
	rm hcsp-1.3.0-x86_64.tar.xz

# Mistral
# Does not compile anymore -> temporarly removed
#RUN ( [ -d /solvers_exec ] || mkdir /solvers_exec ) && \
#	cd /solvers_exec && \
#	git clone --depth 1 https://github.com/ehebrard/Mistral-2.0.git && \
#	mv Mistral-2.0 mistral  && \
#	cd mistral_exec && \
#	make
#ENV PATH $PATH:/solvers_exec/mistral/bin

# Install feature extractor
RUN cd / && \
  git clone --depth=1 https://github.com/CP-Unibo/mzn2feat.git && \
  cd /mzn2feat && \
  bash install --no-xcsp
ENV MZN2FEAT_HOME /mzn2feat
ENV PATH /mzn2feat/bin:$PATH

# install sunny-cp
RUN cd / && \
  git clone --depth=1 https://github.com/CP-Unibo/sunny-cp.git && \
  cd /sunny-cp && \
  bash install
ENV PATH /sunny-cp/bin:$PATH
WORKDIR /sunny-cp
CMD ["python","/sunny-cp/src/sunny_server.py"]


