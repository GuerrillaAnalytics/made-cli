import logging
import os
import re

import click

from made.controllers.config import Config
from made.controllers.inputs import input_manager_factory


def validate_source_label(source_label):
    """Check that a source label has correct format"""
    pattern = re.compile("^[a-z0-9_]*$")
    match_result = re.match(pattern, source_label)
    if match_result is None:
        return False
    else:
        logging.getLogger('my logger').debug(
            "Matched: " + str(match_result.group(0)))
        return True


def input_audit_path(input_base_folder):
    """Audit an input folder to check it
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
            match_result = re.match(pattern, item)
            if match_result is None:
                tup = (
                    "ERR0002",
                    item,
                    "Incorrectly formatted input version folder")
                result.append(tup)

            # Check each version folder only has a formatted or
            # raw subfolder, no files
            # and not other subfolders
            version_subfolders = os.listdir(item)
            if len(version_subfolders) == 0:
                tup = (
                    "ERR0004",
                    version_subfolders,
                    "Version folder contains no "
                    "raw or formatted subfolder")
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
                        if version_subfolder != "formatted" \
                                and version_subfolder != "raw":
                            tup = (
                                "ERR0007",
                                version_subfolder,
                                "Unexpected folder in version folder")
                            result.append(tup)

    return result


def validate_input_version(input_version):
    """Check that an input id is a number without spaces"""
    if ' ' in input_version:
        return False

    # create a set of invalid characters
    return str(input_version).isdigit()


def format_input_version(input_version):
    """Format an input version to have leading zeroes"""
    return str(input_version).zfill(2)


def cmd_input_create():
    """
    Gather the parameters needed to create an input folder
    """
    while True:
        user_source_id = click.prompt('Please enter an input ID', type=str)
        if not validate_input_version(user_source_id):
            logging.getLogger('my logger').debug(
                "Input ID has invalid format " + user_source_id)
            continue

        break

    # source name
    while True:
        user_source_name = click.prompt('Please enter a schema name', type=str)
        if len(user_source_name.strip()) == 0:
            continue
        if " " in user_source_name.strip():
            continue
        break

    config = Config(os.getcwd())
    input_manager = input_manager_factory.InputManagerFactory.create(config)
    input_manager.create_new_source(user_source_id, user_source_name)


def input_new_version():
    while True:
        input_source = click.prompt('Choose an existing input:', type=int)
        logging.getLogger('my logger').debug('Source: ' + input_source)
        config = Config(os.getcwd())
        input_manager = input_manager_factory.InputManagerFactory.create(config)
        # inputs = input_manager.list_inputs()
        logging.getLogger('my logger').error('Not implemented yet')
    return None
