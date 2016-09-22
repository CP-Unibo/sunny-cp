'''
Python script for making the Docker file.
'''
import os
import sys
import shutil
from subprocess import Popen

DEF_PFOLIO = set([
	'g12lazyfd', 'g12fd', 'g12cbc',	'gecode',
  'choco', 'chuffed', 'haifacsp',
  #, 'izplus', 'minisatid', 'ortools'
])



def add(solver, dockerfile):
  	dockerfile.write('\n\n# Install ' + solver + '\n')
  	script_directory = os.path.dirname(os.path.realpath(__file__))
  	docker_file_map = {
  		'choco' : 'choco.docker',
			'chuffed' : 'chuffed.docker',
			'haifacsp': 'haifacsp.docker',
  		}
  	if solver in docker_file_map:
  	  	with open(script_directory + "/" + docker_file_map[solver], "r") as f:
  	  	  	for line in f:
  	  	  		dockerfile.write(line)
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
    for solver in pfolio - set(['g12lazyfd', 'g12fd', 'g12cbc', 'gecode']):
      add(solver, dockerfile)
  dockerfile.write('\n\n# install sunny-cp\n')
  dockerfile.write('RUN cd /sunny-cp && bash install\n')
  dockerfile.write('ENV PATH /sunny-cp/bin:$PATH\n')
  dockerfile.write('WORKDIR /sunny-cp\n')
  dockerfile.write('ENTRYPOINT ["sunny-cp"]\n')
  print '...done!'

if __name__ == '__main__':
  main(sys.argv[1:])
