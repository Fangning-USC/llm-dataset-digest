"""Load json file function."""
import glob
import json
from pathlib import Path


def load_jsonfile(root_dir: str, verbose: bool = False) -> list:
    """This function loads all json files recursively in the root directory.

    Args:
        root_dir: input document name or path.
        verbose: True to print the filenames.

    Returns:
        list of the loaded json data.
    """
    data = []
    for filename in glob.iglob(root_dir + "**/**", recursive=True):
        try:
            data.append(json.loads(Path(filename).read_text()))
            if verbose is True:
                print(filename)
        except:  # noqa
            pass
    return data
