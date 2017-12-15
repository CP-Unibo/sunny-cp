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
		nano  && \
		# qt libraires already comes with minizinc ide
    #    libqt5core5a \
    #    libqt5gui5 \
    #    libqt5network5 \
    #    libqt5webkit5 \
    #    libqt5widgets5 && \
  rm -rf /var/lib/apt/lists/*

# Install minizinc suite
RUN cd / && \
  wget https://github.com/MiniZinc/MiniZincIDE/releases/download/2.1.6/MiniZincIDE-2.1.6-bundle-linux-x86_64.tgz && \
  tar -zxvf MiniZincIDE-2.1.6-bundle-linux-x86_64.tgz && \
  rm -rf MiniZincIDE-2.1.6-bundle-linux-x86_64.tgz && \
	mv MiniZincIDE-2.1.6-bundle-linux-x86_64 minizinc
ENV PATH /minizinc:$PATH
ENV LD_LIBRARY_PATH $LD_LIBRARY_PATH:/minizinc/lib


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
