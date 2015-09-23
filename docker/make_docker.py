'''
Python script for making the Docker file.
'''
import os
import sys
import shutil
from subprocess import Popen

DEF_PFOLIO = set([
  'choco', 'g12cpx', 'g12lazyfd', 'g12fd', 'g12cbc', 
  'gecode', 'haifacsp', 'izplus', 'minisatid', 'ortools'
])

def add(solver, dockerfile):
  dockerfile.write('\n\n# Install ' + solver + '\n')
  if solver == 'choco':
    dockerfile.write('COPY ./choco_exec /solvers_exec/choco_exec\n')
    dockerfile.write('RUN  cd /solvers_exec/choco_exec && ')
    dockerfile.write('wget https://github.com/chocoteam/choco-parsers/releases/download/choco-parsers-3.3.0/choco-parsers-3.3.0-with-dependencies.jar\n')
    dockerfile.write('COPY ./choco /sunny-cp/solvers/choco\n')
    dockerfile.write('ENV PATH /solvers_exec/choco_exec:$PATH\n')
  elif solver == 'gecode':
    dockerfile.write('RUN cd /solvers_exec && ')
    dockerfile.write('wget http://www.gecode.org/download/gecode-4.4.0.tar.gz && ')
    dockerfile.write('tar -zxvf gecode-4.4.0.tar.gz && ')
    dockerfile.write('cd gecode-4.4.0 && ')
    dockerfile.write('./configure --disable-examples --disable-set-vars --prefix=/solvers_exec/gecode-4.4.0 && ')
    dockerfile.write('make && make install\n')
    dockerfile.write('ENV PATH /solvers_exec/gecode-4.4.0/bin:$PATH\n')
    dockerfile.write('ENV LD_LIBRARY_PATH=/solvers_exec/gecode-4.4.0/lib:$LD_LIBRARY_PATH\n')
  elif solver == 'minisatid':
    dockerfile.write('RUN cd /solvers_exec && ')
    dockerfile.write('wget https://dtai.cs.kuleuven.be/krr/files/software/minisatid/minisatid-3.11.0-source.zip && ')
    dockerfile.write('unzip minisatid-3.11.0-source.zip && ')
    dockerfile.write('mkdir minisatid_exec && ')
    dockerfile.write('cd minisatid_exec && ')
    dockerfile.write('cmake /solvers_exec/krr-minisatid-869bec4a8bfb -DCMAKE_INSTALL_PREFIX=./ -DCMAKE_BUILD_TYPE="Release" && ')
    dockerfile.write('make -j 4 && make install && ')
    dockerfile.write('rm -rf /solvers_exec/krr-minisatid-869bec4a8bfb && ')
    dockerfile.write('rm -rf /solvers_exec/minisatid-3.11.0-source.zip\n')
    dockerfile.write('ENV PATH /solvers_exec/minisatid_exec/bin:$PATH\n')
  dockerfile.write('COPY ./' + solver + ' /sunny-cp/solvers/' + solver +'\n')
    
def main(args):
  print '% Preparing Dockerfile...',
  docker_path = '/'.join(os.path.realpath(__file__).split('/')[:-1])
  shutil.copyfile(docker_path + '/base-dockerfile', docker_path + '/Dockerfile')
  dockerfile = open(docker_path + '/Dockerfile', 'a')
  if args:
    solvers = args[0]
    pfolio = set(solvers.split(','))
    if not pfolio <= DEF_PFOLIO:
      print >> sys.stderr, 'Error!',pfolio,'is not a subset of',str(DEF_PFOLIO)
      sys.exit(2)
    dockerfile.write('\n\n# create directory where to save the solvers executables\n')
    dockerfile.write('RUN mkdir /solvers_exec\n')
    dockerfile.write('# install utilities\n')
    dockerfile.write('RUN echo deb http://http.debian.net/debian jessie-backports main >> /etc/apt/sources.list && apt-get update && apt-get install -y unzip openjdk-8-jre-headless cmake && rm -rf /var/lib/apt/lists/*\n')
    for solver in pfolio - set(['g12lazyfd', 'g12fd', 'g12cbc']):
      add(solver, dockerfile)
  dockerfile.write('\n\n# install sunny-cp\n')
  dockerfile.write('RUN cd /sunny-cp && bash install\n')
  dockerfile.write('ENV PATH /sunny-cp/bin:$PATH\n')
  dockerfile.write('WORKDIR /sunny-cp\n')
  dockerfile.write('ENTRYPOINT ["sunny-cp"]\n')
  print '...done!'

if __name__ == '__main__':
  main(sys.argv[1:])