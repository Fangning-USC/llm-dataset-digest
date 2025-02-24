"""Save to json format function."""
import json


def save_to_json(path: str, item: dict, item_name: str) -> None:
    """This function save a dict into json format.

    Args:
        path: path for saving the file.
        item: dictionary of the item to be saved.
        item_name: name of the dictionary to be saved.

    Returns:
        return iterator to non-empty rows.
    """
    with open(("\\\\?\\" + path + "\\" + item_name), "w") as outfile:  # noqa
        json.dump(item, outfile, indent=4)
