import errno
import os


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
    path = input_build_name(source_id, source_name, version)
    try:
        os.makedirs(os.path.join(root_folder, path))
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
    pass
