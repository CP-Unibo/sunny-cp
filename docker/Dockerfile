FROM alpine/git AS repos
RUN cd / && \
  git clone --depth=1 https://github.com/CP-Unibo/sunny-cp.git && \
  git clone --depth=1 https://github.com/CP-Unibo/mzn2feat.git


FROM python:3.7.15-slim-bullseye

# Install minizinc from official docker image
COPY --from=minizinc/minizinc:2.6.4-focal /usr/local/share/minizinc /usr/local/share/minizinc
COPY --from=minizinc/minizinc:2.6.4-focal /usr/local/share/minizinc/Preferences.json /usr/local/share/minizinc/Preferences.json
COPY --from=minizinc/minizinc:2.6.4-focal /usr/local/bin /usr/local/bin

COPY --from=repos /sunny-cp /sunny-cp
COPY --from=repos /mzn2feat /mzn2feat
 
# Install packages for compiling the feature extractor and minizin suite
RUN apt-get update && \
  apt-get install -y \
    make g++\
    flex \
	  bison && \
  rm -rf /var/lib/apt/lists/* && \
  pip3 install \
	  psutil \
	  click

# Install sunny-cp and the feature extractor
ENV MZN2FEAT_HOME /mzn2feat
ENV PATH /mzn2feat/bin:$PATH
ENV PATH /sunny-cp/bin:$PATH

RUN cd /mzn2feat && \
  bash install --no-xcsp && \
  cd /sunny-cp && \
  bash install.sh


WORKDIR /sunny-cp
CMD ["/bin/bash"]



