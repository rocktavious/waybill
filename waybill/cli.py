import os
import yaml
from yaml import Loader
from pyul.coreUtils import DotifyDict
from battalion.api import *

waybill_template = """
echo "    - {command}"

function {command}()
{{
  docker pull {docker_id}
  docker run -it --rm -v ~/.{command}:/.{command} "{docker_id}" {command} $@
}}
"""

def construct_yaml_map(self, node):
    # Override the default string handling function 
    # to always return unicode objects
    return DotifyDict(self.construct_mapping(node))
Loader.add_constructor(u'tag:yaml.org,2002:map', construct_yaml_map)

def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and (os.access(fpath, os.X_OK) or os.access(fpath, os.F_OK))

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


class waybill(CLI):
    
    class State:
        version = "0.0.1"

    def get_waybill_dir(self):
        return os.path.dirname(self.state.config_file)

    def get_waybills(self):
        waybill_dir = self.get_waybill_dir()
        if os.path.exists(waybill_dir):
            files = [os.path.join(waybill_dir, f) for f in os.listdir(waybill_dir)]
            for f in [f for f in files if os.path.isfile(f) and os.path.splitext(f)[-1] == '.waybill']:
                yield f

    @command
    def create(cli, command, docker_id):
        """Creates waybill shims from a given command name and docker image"""
        content = waybill_template.format(command=command,
                                          docker_id=docker_id)
        waybill_dir = cli.get_waybill_dir()
        waybill_filename = os.path.join(waybill_dir, command + '.waybill')
        with open(waybill_filename, 'wb') as filehandle:
            filehandle.write(content)
        cli.log.info('Created waybill {0}'.format(waybill_filename))

    @command
    def load(cli, yaml_filename):
        """Creates waybill shims from a given yaml file definiations"""
        """Expected Definition:
        - name: NAME
          docker_id: IMAGE
        - name: NAME
          docker_id: IMAGE
        """
        with open(yaml_filename, 'rb') as filehandle:
            for waybill in yaml.load(filehandle.read()):
                cli.create(waybill.name,
                           waybill.docker_id)

    @command
    def list(cli):
        """Prints out the list of known waybills"""
        for waybill in cli.get_waybills():
            cli.log.info(waybill)

    @command
    def clear(cli):
        for waybill in cli.get_waybills():
            cli.log.info('Removing waybill {0}'.format(waybill))
            os.remove(waybill)

    @command
    def shellinit(cli):
        """Implements the waybill shims in the active shell"""
        output = 'eval echo "Initializing Waybills"'
        if which('docker') is None:
            raise ValueError("Unable to find program 'docker'.  Please make sure it is installed and setup properly")
        for waybill in cli.get_waybills():
            output += ' && source {0}'.format(waybill)
        return output
            


def main():
    waybill.main()


if __name__ == "__main__":
    main()