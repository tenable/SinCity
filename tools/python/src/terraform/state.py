from config import get_sincity_config
from builder.templating import apply_template, get_jinja_env
from common import find_root_dir, get_terraform_provider_dir
from terraform.api import init_terraform, apply_terraform
from os import path
import os
import logging
from misc.io_utils import remove_files_with_pattern

state_management_dir = path.join(
    find_root_dir(), 'terraform', 'state_management')


def clear_terraform_state_backend(provider: str) -> None:
    """
    Clears any existing terraform state backend.
    """

    state_file = get_state_management_file_path(provider)

    # If we found the state file, clear it
    if path.exists(state_file):
        os.remove(state_file)

    provider_dir = get_terraform_provider_dir(provider)

    # Now remove all files related to terraform in this module
    pattern = path.join(provider_dir, '*.tfstate')
    remove_files_with_pattern(pattern, True)
    pattern = path.join(provider_dir, '*.tfstate.backup')
    remove_files_with_pattern(pattern, True)
    pattern = path.join(provider_dir, '.terraform')
    remove_files_with_pattern(pattern, True)


def apply_terraform_state_backend(backend: str, create_backend: bool, cfg: dict) -> None:
    """
    Applies the terraform state backend strategy provided.
    """

    # If we are running on local terraform state backend, simply delete the current state
    if backend == 'local':
        clear_terraform_state_backend(cfg.get('provider'))
        return

    # Get the backend path
    backend_state_file_path = path.join(state_management_dir, f'{backend}.tf')
    backend_state_file_create_path = path.join(
        state_management_dir, f'{backend}_create.tf')

    # If this provider does not exist
    if not path.exists(backend_state_file_path):
        logging.error(
            f'The state management backend {backend} does not exist!')
        exit(22)

    # If we detected that a pre-run is required for this backend
    if path.exists(backend_state_file_create_path) and create_backend:
        logging.info(
            f'Detect that the backend {backend} requires a pre-run and "init_backend" was set, applying state backend initialize process...')

        apply_state_backend_create(backend_state_file_create_path, cfg)

    # Now apply the template for this state file and save it
    target_file = get_state_management_file_path(cfg.get('provider'))
    apply_state_template(backend_state_file_path, target_file, cfg)


def apply_state_template(state_file: str, target_file: str, cfg: dict[str, str]):
    env = get_jinja_env(state_management_dir)

    # Copy the state backend strategy to the target path
    apply_template(env, state_file, target_file, cfg)


def apply_state_backend_create(backend_create_file_path: str, cfg: dict[str, str]):
    create_dir = get_create_dir(cfg['provider'])
    # Create the pre-run directory if required
    os.makedirs(create_dir, exist_ok=True)

    # Now create the target file
    target_file = path.join(create_dir, 'main.tf')

    # And apply the template and copy it to the target create file
    apply_state_template(backend_create_file_path, target_file, cfg)

    # Now init the terraform directory and apply the required provider
    init_terraform(create_dir)

    # Now applies the create required for this backend to work
    apply_terraform(create_dir)


def get_state_management_file_path(provider: str) -> str:
    """
    Returns the state management file path.
    """

    return path.join(get_terraform_provider_dir(
        provider), 'state_backend.tf')


def get_create_dir(provider: str):
    return path.join(get_terraform_provider_dir(provider), '.state_backend')
