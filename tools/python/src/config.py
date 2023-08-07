import json
import os
from typing import TypedDict
import logging
from common import find_root_dir

HONEYMOON_CONFIG_PATH = os.path.join(find_root_dir(), '.sincity_config.json')


class SinCityConfig(TypedDict):
    provider: str
    region: str
    state_backend: str
    state_backend_name: str


def delete_config(verbose: bool = True) -> None:
    if config_exists():
        # Remove the existing sincity configurations
        os.remove(HONEYMOON_CONFIG_PATH)
        if verbose:
            logging.info("SinCity config was deleted")
    else:
        if verbose:
            logging.info("SinCity config does not exist")


def config_exists() -> bool:
    return os.path.exists(HONEYMOON_CONFIG_PATH)


def validate_sincity_config(config: dict) -> None:
    if 'provider' not in config:
        logging.info('Config is missing the provider field!')
        exit(1)

    if config['provider'] == 'aws' or config['provider'] == 'azure':
        if 'region' not in config:
            logging.info('Config is missing region')
            exit(1)


def get_sincity_config(verify_exists: bool = False) -> SinCityConfig:
    if not config_exists():

        if verify_exists:
            logging.error('No config was found! please run setup before')
            exit(1)

        return None

    with open(HONEYMOON_CONFIG_PATH, 'r', encoding='utf-8') as f:
        text = f.read()
        config = json.loads(text)
        validate_sincity_config(config)

    return config


def write_sincity_config(cfg: dict) -> None:
    with open(HONEYMOON_CONFIG_PATH, 'w', encoding='utf-8') as f:
        f.write(get_pretty_config_str(cfg))


def get_pretty_config_str(cfg: dict) -> None:
    return json.dumps(cfg, indent=4)
