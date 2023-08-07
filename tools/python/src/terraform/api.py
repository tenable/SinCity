from common import run_command
import logging


def init_terraform(cwd: str):
    """
    Executes the 'terraform init' command in the provided current directory.
    """

    returncode = run_command(
        f'terraform init', cwd=cwd)

    if returncode != 0:
        logging.info("Failed to initialize terraform!")
        exit(1)


def apply_terraform(cwd: str):
    """
    Executes the 'terraform apply' command in the provided current directory.
    """

    logging.info('Applying terraform infrastructure provisioning...')

    # Now apply the terraform infrastructure
    returncode = run_command(
        'terraform apply -auto-approve', cwd=cwd)

    if returncode != 0:
        logging.error(
            f'Terraform exited with code {returncode}, apply failed')
        exit(1)

    logging.info('Terraform applied successfully!')
