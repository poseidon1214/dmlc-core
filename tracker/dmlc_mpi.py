#!/usr/bin/env python
"""
DMLC submission script, MPI version
"""
import argparse
import sys
import os
import subprocess
import tracker
from threading import Thread

parser = argparse.ArgumentParser(description='DMLC script to submit dmlc job using MPI')
parser.add_argument('-n', '--nworker', required=True, type=int,
                    help = 'number of worker proccess to be launched')
parser.add_argument('-s', '--server-nodes', default = 0, type=int,
                    help = 'number of server nodes to be launched')
parser.add_argument('-v', '--verbose', default=0, choices=[0, 1], type=int,
                    help = 'print more messages into the console')
parser.add_argument('-H', '--hostfile', type=str,
                    help = 'the hostfile of mpi server')
parser.add_argument('command', nargs='+',
                    help = 'command for dmlc program')
args = parser.parse_args()
#
# submission script using MPI
#
def mpi_submit(nworker, nserver, pass_envs):
    """
      customized submit script, that submit nslave jobs, each must contain args as parameter
      note this can be a lambda function containing additional parameters in input
      Parameters
         nworker number of slave process to start up
         nserver number of server nodes to start up
         pass_envs enviroment variables to be added to the starting programs
    """
    env = os.environ.copy()

    for k, v in pass_envs.items():
        env[k] = str(v)

    sargs = ' '.join(args.command)
    if args.hostfile is None:
        cmd = 'mpirun -n %d' % (nworker + nserver)
    else:
        cmd = 'mpirun -n %d --hostfile %s ' % (nworker + nserver, args.hostfile)

    for k, v in pass_envs.items():
        cmd += ' -env %s %s' % (k, v)
        # cmd += ' -x %s' % k
    cmd += ' '
    cmd += ' '.join(args.command)

    print '%s' % cmd
    # known issue: results do not show in emacs eshell
    def run():
        subprocess.check_call(cmd, shell = True, env = env)
    thread = Thread(target = run, args=())
    thread.setDaemon(True)
    thread.start()

# call submit, with nslave, the commands to run each job and submit function
tracker.submit(args.nworker, args.server_nodes, fun_submit = mpi_submit,
               verbose = args.verbose, pscmd= (' '.join(args.command)))
