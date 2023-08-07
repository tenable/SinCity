import os
import shutil
from wcmatch import glob, wcmatch

JSON_YAML_FIND_PATTERN = '.{json,yaml,yml}'


def find_file_with_pattern(root_dir: str, pattern: str) -> str:
    """
    Finds a specific find within the provided pattern. If multiple files are found,
    returns the 1st one. If no files are found, return null.
    """

    results = wcmatch.WcMatch(root_dir, pattern,
                              flags=wcmatch.BRACE | wcmatch.GLOBSTAR).match()
    if len(results) >= 1:
        return results[0]

    return None


def get_files_with_pattern(pattern: str, recursive: bool = True) -> list[str]:
    return glob.glob(pattern, flags=wcmatch.BRACE | wcmatch.GLOBSTAR | wcmatch.RECURSIVE)


def remove_files_with_pattern(pattern: str, recursive: bool = True) -> list[str]:
    """
    Finds all files that match a specific pattern and removes them.
    """
    path_deleted = []

    for path in glob.glob(pattern, flags=wcmatch.BRACE | wcmatch.GLOBSTAR | wcmatch.RECURSIVE):
        if os.path.isfile(path):
            os.remove(path)
        else:
            shutil.rmtree(path)

        path_deleted.append(path_deleted)

    return path_deleted
