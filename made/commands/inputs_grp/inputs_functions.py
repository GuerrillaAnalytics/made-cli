import errno
import os
import re


def input_build_name(source_id, source_name, version, raw_or_formatted="raw"):
    """create a folder path for a given input"""

    valid = {"raw", "formatted"}
    if raw_or_formatted not in valid:
        raise ValueError("raw_or_formatted: must have value 'raw' or 'formatted'")

    source_id = source_id.lower()
    version = str(version).zfill(3)

    # TODO Check source_id does not contain spaces

    path = os.path.join(source_id + "_" + source_name,
                        version, raw_or_formatted, "data")
    return path


def input_create(root_folder, source_id, source_name, version):
    """Creates an input folder tree in the correct structure"""

    raw_path = input_build_name(source_id, source_name, version, "raw")
    formatted_path = input_build_name(source_id, source_name, version, "formatted")

    try:
        os.makedirs(os.path.join(root_folder, raw_path))
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(raw_path):
            pass
        else:
            raise

    try:
        os.makedirs(os.path.join(root_folder, formatted_path))
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(formatted_path):
            pass
        else:
            raise

    pass


def input_audit_path(input_base_folder):
    """ Audit an input folder to check it
    has the right path formats"""
    result = []

    # Check base name is correct

    # Check subfolders only of format dd
    subfolders = os.listdir(input_base_folder)
    if len(subfolders) == 0:
        tup = ("ERR0003", input_base_folder, "Base folder contains files")
        result.append(tup)

    for item in subfolders:
        if not os.path.isdir(item):
            tup = ("ERR0001", item, "Unexpected file in input folder")
            result.append(tup)
        else:
            pattern = re.compile("^[0-9]{3}$")

            # Test the folder has an acceptable name
            matchResult = re.match(pattern, item)
            if matchResult is None:
                tup = ("ERR0002", item, "Incorrectly formatted input version folder")
                result.append(tup)

    return result