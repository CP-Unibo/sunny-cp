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
COPY --from=jacopomauro/minizinc /tool/MiniZincIDE /tool/MiniZincIDE
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
ENV PATH /tool/sunny-cp/bin:$PATH
RUN cd /tool && \
  git clone --depth=1 https://github.com/CP-Unibo/sunny-cp.git && \
  cd sunny-cp && \
  bash install.sh

# or-tools
COPY --from=jacopomauro/or-tools /tool/or-tools /tool/ortools
RUN mkdir -p /tool/sunny-cp/solvers/ortools && \
    ln -s /tool/ortools/ortools/flatzinc/mznlib /tool/sunny-cp/solvers/ortools/mzn-lib && \
    ln -s /tool/ortools/bin/fzn-or-tools /tool/sunny-cp/solvers/ortools/fzn-exec && \
    echo "all_opt = '-a'\n\
free_opt  = '-f'" > /tool/sunny-cp/solvers/ortools/opts


# Install choco
COPY --from=jacopomauro/choco /tool/choco /tool/choco
RUN mkdir -p /tool/sunny-cp/solvers/choco && \
    ln -s /tool/choco/mzn-lib /tool/sunny-cp/solvers/choco/mzn-lib && \
    ln -s /tool/choco/fzn-choco /tool/sunny-cp/solvers/choco/fzn-exec && \
    echo "all_opt = '-a'\n\
free_opt  = '-f'" > /tool/sunny-cp/solvers/choco/opts

# Install picat
COPY --from=jacopomauro/picat /tool/picat /tool/picat
RUN mkdir -p /tool/sunny-cp/solvers/picat && \
    ln -s /tool/picat/mzn-lib /tool/sunny-cp/solvers/picat/mzn-lib && \
    ln -s /tool/picat/fzn-picat /tool/sunny-cp/solvers/picat/fzn-exec && \
    echo "all_opt = '-a'\n\
free_opt  = '-f'" > /tool/sunny-cp/solvers/picat/opts

# Install jacop
COPY --from=jacopomauro/jacop /tool/jacop /tool/jacop
RUN mkdir -p /tool/sunny-cp/solvers/jacop && \
    ln -s /tool/jacop/mzn-lib /tool/sunny-cp/solvers/jacop/mzn-lib && \
    ln -s /tool/jacop/fzn-jacop /tool/sunny-cp/solvers/jacop/fzn-exec && \
    echo "all_opt = '-a'\n\
free_opt  = ''" > /tool/sunny-cp/solvers/jacop/opts

# Install yuck
COPY --from=jacopomauro/yuck /tool/yuck /tool/yuck
RUN mkdir -p /tool/sunny-cp/solvers/yuck && \
    ln -s /tool/yuck/mzn-lib /tool/sunny-cp/solvers/yuck/mzn-lib && \
    ln -s /tool/yuck/fzn-yuck /tool/sunny-cp/solvers/yuck/fzn-exec && \
    echo "all_opt = ''\n\
free_opt  = ''" > /tool/sunny-cp/solvers/yuck/opts

### Not updated solvers but kept because still working
### haifacsp solutions should be checked

# Install minisatid
COPY --from=jacopomauro/minisatid:v3.11.0 /tool/minisatid /tool/minisatid
RUN mkdir -p /tool/sunny-cp/solvers/minisatid && \
    mkdir -p /tool/sunny-cp/solvers/minisatid/mzn-lib && \
    ln -s /tool/minisatid/fzn-minisatid /tool/sunny-cp/solvers/minisatid/fzn-exec && \
    echo "all_opt = '-a'\n\
free_opt  = ''" > /tool/sunny-cp/solvers/minisatid/opts
ENV LD_LIBRARY_PATH "$LD_LIBRARY_PATH:/tool/minisatid/lib"


# Install haifacsp
COPY --from=jacopomauro/haifacsp:v1.3.0 /tool/haifacsp /tool/haifacsp
RUN mkdir -p /tool/sunny-cp/solvers/haifacsp && \
    ln -s /tool/haifacsp/mzn-lib /tool/sunny-cp/solvers/haifacsp/mzn-lib && \
    ln -s /tool/haifacsp/fzn-haifacsp /tool/sunny-cp/solvers/haifacsp/fzn-exec && \
    echo "all_opt = '-a'\n\
free_opt  = ''" > /tool/sunny-cp/solvers/haifacsp/opts

# expose port 9001 for the sunny-cp server
EXPOSE 9001

RUN cd /tool/sunny-cp && \
  bash install.sh
WORKDIR /tool/sunny-cp
CMD ["python","/tool/sunny-cp/src/sunny_server.py"]



