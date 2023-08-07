#!/bin/python
"""Shynet

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@                   @@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@     /////#      /*****/     @@@@@@@@@@@@@@
@@@@@@@@@@@@@    //                       ***/   @@@@@@@@@@@
@@@@@@@@@@@   /,                              ***   @@@@@@@@
@@@@@@@@@  /*                                    **   @@@@@@
@@@@@@@  //                 @@@@@@@                **   @@@@
@@@@@@  /                &&&@@@@@@@  @               **  @@@
@@@@@  /                ,& .&@@@@@@@@@                **  @@
@@@@  /             @@  @   @@@@@@@   @ ,@@            **  @
@@@@ /           @@@@@  @   @@@@@@@   @  @@  @          *  @
@@@  /  ###      @@@@@  @             @  @@  @(/(       */ @
@@@  /  ###      @@.@@  @             &  @@  @@/%       **  
@@@  /  ### ****@@@ @@  &&&.@@@@@@@ @&@  @@   @ .####*  ,* @
@@@@    ### ####@@@@@@ @@   @@@@@     @  @@  @@  ####**,,**@
@@@@@ /  ## ####@@@@@@ ,,   @@@@@@@   @@ @@*  &@ ####,*,,*@@
@@@@@  / (# ####@@@@@@ @@   @@@@@@@   @@ @@@  @@#####,,,*@@@
@@@@@@@  .# ####@@@@@  @@   @@@@@@@   @@ @@@  @@ ####*. @@@@
@@@@@@@@  * ### @@@@@  @@   @@@@@@@   @@ @@@  @@ ####  @@@@@
@@@@@@@@@@  ### @@@@@  @    @@@@@@@@  @@  @@  @@ (*  @@@@@@@
@@@@@@@@@@@@@  @@@.@@  @,   @@@@@@@@  (@  @@  @@@ @@@@@@@@@@
@@@@@@@@@@@@@@@@  .@@  @.   @@@@@@@@@@ @  @@   @@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@   @    @@@@@@@@@@ @   @@@@@@@@@@@@@@@@@

Provision & Configure your infrastructure like never before

Usage:
  sincity setup <provider> [--region=<region>] [--subscription-id=<subscription-id>] [--azure-domain=<azure-domain>] [--ignore-certs] [--fresh] [--state-backend=<state-backend>] [--state-backend-name=<state-backend-name>] [--create-state-backend]
  sincity apply [--only=<logic>] [--ansible-tags=<tags>] [--ansible-env=<ansenv>] [--ansible-playbook=<playbook>] [--wait=<wait>]
  sincity build [--topologies=<topologies>] [--scenarios=<scenarios>] [--strategy=<strategy>]
  sincity sync inventory [--local]
  sincity config [<action>]
  sincity print [<action>] [--format=<format>]
  sincity compose [--topology=<topology>]
  sincity generate keys
  sincity destroy
  sincity test
  sincity (-h | --help)
  sincity --version

Options:
  -h --help                         Show this screen.
  apply                             Applies the sincity infrastructure.
  setup                             Sets up sincity for the first time.
  test                              Checks all required dependencies exist.
  config [<action>]                 Apply the provided action (print\delete) on the config [default: print].
  build [--topologies] [--scenarios] [--strategy]       Builds the required code from the 'network.json' in order to provision and configure the network. If scenarios is specified, generates a new 'network.json' file which consists of the provided scenarios and based on the existing 'network.json' file. Set '--topologies' to create a new fresh 'network.json' based on any of the topologies provided under the 'topologies' directory. Set '--strategy' to '--replace' which will replace lists under the json file instead of adding them.
  sync inventory [--local]          Syncs the inventory with the correct server addresses, use --local to use local IP addresses.
  print [<action>] [--format]         Prints required data (config\techniques), here you can print either configurations or the techniques. Use --format to change the format.
  compose [--topology]              Uses OpenAI to generate an environment topology file or improve an existing one.
  generate keys                     Generates new SSH keys (done automatically when new SinCity environment is setup).
  estroy                           Destroys the entire infrastructure.
  --fresh                           Sets up sincity as fresh installation by removing the existing config.
  --state-backend=<state-backend>   Sets terraform state management backend [default: local], options: local\s3.
  --state-backend-name=<state-backend-name> Sets the state backend storage name. For example, if S3 was chosen as the state backend, the created S3 will be with the supplied name.
  --create-state-backend            Creates the state backend required. For example, if S3 was provided, will create the S3 bucket and other required dependencies using the provided '--state-backend-name'.
  --only=<logic>                    Either only provisions or configures the environments (--only=provision\configure).
  --ansible-tags=<tags>             Apply the ansible infrastructure only with the provided tags.
  --ansible-env=<ansenv>            The environment to apply the configurations on (windows\\linux\\all) [default: all].
  --ansible-playbook=<playbook>     The name of the playbook to play, the '--ansible-env' argument must be provided as well [default: main.yml].
  --ignore-certs                    When installs the ansible-galaxy collections during setup, ignores the certificates (SSL).
  --wait=<wait>                     Set the wait time when terraform finished applying [default: 180].
  --region=<region>                 Required only for AWS provided, provides the region to be used when provisioning.
  --format=<format>                 The format to print out [default: csv].
  --version                         Show version.
"""

import logging
import pprint
from docopt import docopt
from common import run_command, is_provider_supported, check_requirements, SUPPORTED_PROVIDERS, get_terraform_provider_dir
from config import get_sincity_config,  delete_config, get_pretty_config_str
from builder.build import update_ansible_inventory, build_infrastructure
from cli.setup import setup_sincity
from cli.apply import apply_sincity
from terraform.state import clear_terraform_state_backend
from cli.print_supported_techniques import print_supported_techniques


def apply_config_action(action: str, format: str = 'csv'):
    if not action:
        action = 'print'

    if action == 'delete':
        provider = get_sincity_config().get('provider', '')
        delete_config()

        if provider:
            clear_terraform_state_backend(provider)
    else:
        logging.info(get_pretty_config_str(get_sincity_config(True)))


def compose_infrastructure(arguments: dict):
    from ai.topology_composer import generate_ai_topology, improve_ai_topology

    topology = arguments.get('--topology')

    if topology:
        improve_ai_topology(topology)
    else:
        generate_ai_topology()


def print_action(action: str, format: str):
    if action == 'config':
        return apply_config_action(action)
    elif action == 'techniques':
        return print_supported_techniques(format)


def test_sincity():
    check_requirements(True)


def update_inventory(arguments: dict):
    update_ansible_inventory(get_sincity_config(True), arguments['--local'])


def generate_ssh_keys(arguments: dict):
    from .generate_ssh_keys import generate_ssh_keys
    generate_ssh_keys()


def destroy_sincity(arguments: dict):
    cfg = get_sincity_config(True)
    terraform_dir = get_terraform_provider_dir(cfg['provider'])
    returncode = run_command(
        f'terraform destroy -auto-approve', cwd=terraform_dir)

    if returncode != 0:
        logging.info(f"Terraform destroy failed, exit code: {returncode}")
        exit(1)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='SinCity v0.0.1')
    provider = arguments['<provider>']

    if provider and not is_provider_supported(provider):
        logging.info(
            f'The provider {provider} is not supported, supported providers are:')
        pprint.PrettyPrinter().plogging.info(SUPPORTED_PROVIDERS)
        exit(42)

    if arguments['setup']:
        setup_sincity(arguments)
    elif arguments['apply']:
        apply_sincity(arguments)
    elif arguments['config']:
        apply_config_action(arguments['<action>'])
    elif arguments['test']:
        test_sincity()
    elif arguments['build']:
        build_infrastructure(arguments)
    elif arguments['sync'] and arguments['inventory']:
        update_inventory(arguments)
    elif arguments['compose']:
        compose_infrastructure(arguments)
    elif arguments['generate'] and arguments.get('keys') is True:
        generate_ssh_keys(arguments)
    elif arguments['destroy']:
        destroy_sincity(arguments)
    elif arguments['print']:
        print_action(arguments['<action>'], arguments['--format'])

    # logging.info(arguments)
