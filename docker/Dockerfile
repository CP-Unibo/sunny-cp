FROM python:2-stretch
MAINTAINER Jacopo Mauro

# Install packages for compiling the feature extractor and minizin suite
RUN apt-get update && \
  apt-get install -y \
    flex \
	bison \
	# for gecode
	libgl1 \
	# for choco and jacop
	openjdk-8-jre-headless && \
  rm -rf /var/lib/apt/lists/* && \
  pip install \
	psutil \
	click

# minizinc + gecode + chuffed
COPY --from=jacopomauro/minizinc:v2.2.1 /tool/MiniZincIDE /tool/MiniZincIDE
ENV PATH "$PATH:/tool/MiniZincIDE/bin"
ENV LD_LIBRARY_PATH "$LD_LIBRARY_PATH:/tool/MiniZincIDE/lib"

# Install feature extractor
RUN cd /tool && \
  git clone --depth=1 https://github.com/CP-Unibo/mzn2feat.git && \
  cd mzn2feat && \
  bash install --no-xcsp
ENV MZN2FEAT_HOME /tool/mzn2feat
ENV PATH /tool/mzn2feat/bin:$PATH

# install sunny-cp (basic one with only minizinc solvers)
RUN cd /tool && \
  git clone --depth=1 https://github.com/CP-Unibo/sunny-cp.git && \
  cd sunny-cp && \
  bash install.sh
ENV PATH /tool/sunny-cp/bin:$PATH

# or-tools
COPY --from=jacopomauro/or-tools:v6.9.1 /tool/or-tools /tool/ortools
RUN mkdir -p /tool/sunny-cp/solvers/ortools && \
    ln -s /tool/ortools/ortools/flatzinc/mznlib_sat /tool/sunny-cp/solvers/ortools/mzn-lib && \
    ln -s /tool/ortools/bin/fzn-or-tools /tool/sunny-cp/solvers/ortools/fzn-exec && \
    echo "all_opt = '-a'\n\
free_opt  = '-f'" > /tool/sunny-cp/solvers/ortools/opts


# Install choco
COPY --from=jacopomauro/choco:v4.0.4 /tool/choco /tool/choco
RUN mkdir -p /tool/sunny-cp/solvers/choco && \
    ln -s /tool/choco/mzn-lib /tool/sunny-cp/solvers/choco/mzn-lib && \
    ln -s /tool/choco/fzn-choco /tool/sunny-cp/solvers/choco/fzn-exec && \
    echo "all_opt = '-a'\n\
free_opt  = '-f'" > /tool/sunny-cp/solvers/choco/opts

# Install picat
COPY --from=jacopomauro/picat:v2.5 /tool/picat /tool/picat
RUN mkdir -p /tool/sunny-cp/solvers/picat && \
    ln -s /tool/picat/mzn-lib /tool/sunny-cp/solvers/picat/mzn-lib && \
    ln -s /tool/picat/fzn-picat /tool/sunny-cp/solvers/picat/fzn-exec && \
    echo "all_opt = '-a'\n\
free_opt  = '-f'" > /tool/sunny-cp/solvers/picat/opts

# Install jacop
COPY --from=jacopomauro/jacop:v4.4.0 /tool/jacop /tool/jacop
RUN mkdir -p /tool/sunny-cp/solvers/jacop && \
    ln -s /tool/jacop/mzn-lib /tool/sunny-cp/solvers/jacop/mzn-lib && \
    ln -s /tool/jacop/fzn-jacop /tool/sunny-cp/solvers/jacop/fzn-exec && \
    echo "all_opt = '-a'\n\
free_opt  = '-f'" > /tool/sunny-cp/solvers/jacop/opts

# Install minisatid
COPY --from=jacopomauro/minisatid:v3.11.0 /tool/minisatid /tool/minisatid
RUN mkdir -p /tool/sunny-cp/solvers/minisatid && \
    mkdir -p /tool/sunny-cp/solvers/minisatid/mzn-lib && \
    ln -s /tool/minisatid/fzn-minisatid /tool/sunny-cp/solvers/minisatid/fzn-exec && \
    echo "all_opt = '-a'\n\
free_opt  = ''" > /tool/sunny-cp/solvers/minisatid/opts
ENV LD_LIBRARY_PATH "$LD_LIBRARY_PATH:/tool/minisatid/lib"


# Install haifacsp
# not available anymore online
#RUN cd /solvers_exec && \
#	wget --no-check-certificate http://ie.technion.ac.il/~ofers/HCSP/hcsp-1.3.0-x86_64.tar.xz && \
#	tar -xJf hcsp-1.3.0-x86_64.tar.xz && \
#	mv hcsp-1.3.0-x86_64 haifacsp && \
#	rm hcsp-1.3.0-x86_64.tar.xz && \
#	mv /sunny-cp/docker_solvers/haifacsp /sunny-cp/solvers

# Mistral
# Compiles but does not print output on zebra instance and other instances
#RUN cd /solvers_exec && \
#	git clone --depth 1 --recursive https://github.com/ehebrard/Mistral-2.0.git && \
#	mv Mistral-2.0 mistral  && \
#	cd mistral && \
#	make && \
#	mv /sunny-cp/docker_solvers/mistral /sunny-cp/solvers
#ENV PATH $PATH:/solvers_exec/mistral/fz

# install the added solver in sunny-cp

# expose port 9001 for the sunny-cp server
EXPOSE 9001

RUN cd /tool/sunny-cp && \
  bash install.sh
WORKDIR /tool/sunny-cp
CMD ["python","/sunny-cp/src/sunny_server.py"]



