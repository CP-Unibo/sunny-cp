FROM sunny:v1
MAINTAINER Jacopo Mauro

# create directory where to save the solvers executables/srcs/...
RUN mkdir /solvers_exec
# install utilities
RUN apt-get update && \
  apt-get install -y unzip openjdk-8-jre  && \
  rm -rf /var/lib/apt/lists/*

