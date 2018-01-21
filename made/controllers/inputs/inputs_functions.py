import errno
import os
import re


def input_audit_path(input_base_folder):
    """ Audit an input folder to check it
    has the right path formats
    * no files present
    * only folders with a 2 digit version number
    """
    result = []

    # Check base name is correct

    # Check subfolders only of format dd
    files_and_dirs_in_folder = os.listdir(input_base_folder)
    if len(files_and_dirs_in_folder) == 0:
        tup = ("ERR0003", input_base_folder, "Base folder contains no folders")
        result.append(tup)

    # Check there are no files in the inputs folder
    for item in files_and_dirs_in_folder:
        # if it's not a directory (i.e. it's a file
        if not os.path.isdir(item):
            tup = ("ERR0001", item, "Unexpected file in input folder")
            result.append(tup)
        else:
            # Else if it is a directory, check it has correct format
            pattern = re.compile("^[0-9]{3}$")

            # Test the folder has an acceptable name
            matchResult = re.match(pattern, item)
            if matchResult is None:
                tup = (
                    "ERR0002",
                    item,
                    "Incorrectly formatted input version folder")
                result.append(tup)

            # Check each version folder only has a formatted or raw subfolder, no files
            # and not other subfolders
            version_subfolders = os.listdir(item)
            if len(version_subfolders) == 0:
                tup = (
                    "ERR0004",
                    version_subfolders,
                    "Version folder contains no raw or formatted subfolder")
                result.append(tup)

            else:
                for version_subfolder in version_subfolders:
                    # if there is a file, then error
                    if not os.path.isdir(version_subfolder):
                        tup = (
                            "ERR0006",
                            version_subfolder,
                            "Unexpected file in version folder")
                        result.append(tup)
                    else:
                        if version_subfolder != "formatted" and version_subfolder != "raw":
                            tup = (
                                "ERR0007",
                                version_subfolder,
                                "Unexpected folder in version folder")
                            result.append(tup)

    return result
