import logging
from common import run_command, check_requirements, \
    get_terraform_provider_dir, get_ansible_dir
from config import get_sincity_config, write_sincity_config, \
    delete_config
from terraform.state import clear_terraform_state_backend, \
    apply_terraform_state_backend
from terraform.api import init_terraform
from builder.build import apply_provider_templates
from .generate_ssh_keys import generate_ssh_keys


def setup_sincity(arguments: dict):
    # Get the provider we want to setup sincity for
    provider = arguments['<provider>']

    # If it's a fresh installation, remove the existing config if exists
    if arguments['--fresh']:
        delete_config(False)
        clear_terraform_state_backend(provider)

    # Check if sincity can run on this system
    check_requirements()

    # Generate new SSH keys
    generate_ssh_keys(True)

    # Now validate the arguments provided
    validate_arguments(arguments, provider)

    # Generate the configurations
    cfg = generate_config_from_args(arguments, provider)

    # Setup the required logics
    setup_terraform(provider, arguments, cfg)
    setup_ansible(arguments)

    # Now save the configurations
    write_sincity_config(cfg)

    logging.info("SinCity infrastructure is now ready to be applied!")


def setup_terraform(provider: str, arguments, cfg: dict[str, str]):
    """
    Initializes terraform and exits if it had failed.
    """

    terraform_dir = get_terraform_provider_dir(provider)

    # Apply the provider templates, this must happen in order
    # to allow terraform to initialize
    apply_provider_templates(cfg, {'config': cfg, 'network': {}})

    # First apply the state backend
    state_backend = arguments['--state-backend']
    create_state_backend = arguments['--create-state-backend']
    apply_terraform_state_backend(state_backend, create_state_backend, cfg)

    # Now initialize terraform
    init_terraform(terraform_dir)


def setup_ansible(arguments: dict):
    """
    Installs ansible requirements and sets up ansible. Exits if fails.
    """

    cmd = 'ansible-galaxy install -r requirements.yml'

    if '--ignore-certs' in arguments:
        cmd += ' --ignore-certs'

    returncode = run_command(cmd,
                             cwd=get_ansible_dir())

    if returncode != 0:
        logging.error(f'Failed to setup ansible! error code: {returncode}')
        exit(1)


def generate_config_from_args(arguments: dict, provider: str) -> dict[str, str]:
    cfg = {
        "provider": provider,
    }

    # If AWS provided was provided, save the region applied
    if provider == 'aws' or provider == 'azure':
        cfg['region'] = arguments['--region']

    # If a custom state backend was provided
    if '--state-backend' in arguments:
        cfg['state_backend'] = arguments['--state-backend']

    if '--state-backend-name' in arguments:
        cfg['state_backend_name'] = arguments['--state-backend-name']

    if provider == 'azure':
        cfg['subscription_id'] = arguments['--subscription-id']
        cfg['azure_domain'] = arguments['--azure-domain']

    return cfg


def validate_arguments(arguments: dict, provider):
    """
    Validates that the arguments provided are correct.
    """

    if get_sincity_config():
        logging.info(
            "SinCity was already setup, add '--fresh' to force the setup")
        exit(1)

    if (provider == 'aws' or provider == 'azure') and not arguments['--region']:
        logging.error(
            'No region was provided! provide a region using --region')
        exit(1)

    if provider == 'azure' and not arguments['--subscription-id']:
        logging.error(
            'No subscription id was provided! provide a subscription using --subscription_id')
        exit(1)

    if provider == 'azure' and not arguments['--azure-domain']:
        logging.error(
            'No azure_domain was provided! provide a azure_domain using --azure_domain')
        exit(1)

    if arguments['--state-backend'] != 'local':
        if not arguments.get('--state-backend-name', None):
            logging.error(
                'Please provide --state-backend-name, for example: \
                    if state will be stored on S3, set the S3 bucket name')
            exit(1)
