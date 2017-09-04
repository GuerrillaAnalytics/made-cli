import errno
import os


def input_build_name(source_id, source_label, version, schema):
    """create a folder path for a given input"""

    # TODO Check source_id does not contain spaces

    path = os.path.join(source_id.lower() + "_" + source_label.lower(),
                        version.zfill(3), schema)
    return path


def input_create(source_id, source_label, schema, version):
    """Creates an input folder tree in the correct structure"""
    path = input_build_name(source_id, source_label, version, schema)
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
    pass
