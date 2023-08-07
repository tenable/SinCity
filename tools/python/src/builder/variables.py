from common import find_root_dir
import os
from misc.dict_loader import get_merged_dict_from_folder


def get_assets_variables_or_empty(root_dir: str = None) -> None:
    """
    Returns the variables from 'assets.json' if exists, if not, returns empty variables dictionary.
    """

    if not root_dir:
        root_dir = find_root_dir(root_dir)

    assets_dir = os.path.join(root_dir, 'assets')

    # If the assets file exists, read variables from there
    if os.path.exists(assets_dir):
        output = get_merged_dict_from_folder(assets_dir)
        return output

    return {}
