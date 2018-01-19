import string
import os
import re
import click

from made.controllers.config import Config
import logging

class ProjectException(Exception):
    pass


def validate_project_name(project_name):
    """ Validates a project name to certain rules"""

    if " " in project_name:
        return False

    # create a set of invalid characters
    invalidChars = set(string.punctuation.replace("_", ""))
    invalidChars.add('£')

    # chekc if the name contains any of the invalid characters
    if any(char in invalidChars for char in project_name):
        return False

    return True


def is_project_initialised(folder_location):
    """Check a folder does not exist and can be created"""

    cfg = os.path.join(folder_location, "made.config")
    # Folder exists and config exists
    if not os.path.isdir(cfg):
        click.echo(click.style("This project folder has not been initialised"))
        return False
    else:
        return True


def make_folder_if_doesnt_exist(folder):
    """Utility function to create a folder if it doesn't already exist"""
    if not os.path.exists(folder):
        os.makedirs(folder)
    else:
        click.echo(click.style("The folder %s already exists" % folder, fg='yellow'))
    return folder


def project_init_pm_folder(project_folder_path):
    """Create a pm folder tree in a given project folder"""

    # Make the pm folder tree
    pm_folder = make_folder_if_doesnt_exist(os.path.join(project_folder_path, "pm"))
    make_folder_if_doesnt_exist(os.path.join(pm_folder, "01_initiate"))
    make_folder_if_doesnt_exist(os.path.join(pm_folder, "02_plan"))
    make_folder_if_doesnt_exist(os.path.join(pm_folder, "03_execute"))
    make_folder_if_doesnt_exist(os.path.join(pm_folder, "04_control"))
    make_folder_if_doesnt_exist(os.path.join(pm_folder, "05_close"))


def project_create_folder_structures(project_folder_path):
    """Creates a project structure.
    Assumes current directory
    is root of project"""

    # create the pm folder structure
    project_init_pm_folder(project_folder_path)

    # create other folder structures
    make_folder_if_doesnt_exist(os.path.join(project_folder_path, "wp"))
    make_folder_if_doesnt_exist(os.path.join(project_folder_path, "workspaces"))

    pass


def project_create_folder(id, label):
    """Creates a project folder if possible in the current directory"""

    project_name = id.lower() + "_" + label.lower()
    project_audit_name(project_folder=project_name)

    # TODO check id doesn't exist in same directory

    project_location = os.path.join(os.getcwd(), project_name)
    make_folder_if_doesnt_exist(project_location)

    return project_location


def project_audit_name(project_folder):
    """ Audit the project folder name"""

    project_folder = os.path.basename(project_folder)
    print("Project folder: " + project_folder)
    pattern = re.compile("^ds[0-9]{3}_[[a-z0-9]*]?$")

    # Test the folder has an acceptable name
    matchResult = re.match(pattern, project_folder)
    if matchResult is None:
        return False
    else:
        print("Matched: " + str(matchResult.group(0)))
        return True


def project_audit_tree(project_folder):
    """Check that a project tree has correct structure"""
    pass


def project_configure(folder):
    """ Create a minimum configuration for a project"""

    if folder == ".":
        folder = os.getcwd()

    # create new configuration class for this project
    configuration = Config(folder)

    # project level configurations
    while True:
        project_name = \
            click.prompt('Please enter a project name',type = str, default='ds_xxx')

        # TODO validate that the project name is the right format
        is_valid = validate_project_name(project_name)
        if is_valid:
            configuration.add_option_project_name(project_name)
            break

        logging.getLogger('my logger').info(('Not a valid project name'))

    # Enter a work product prefix
    while True:
        work_product_prefix = \
            click.prompt('Please enter a work product prefix', type=str, default=configuration.get_option_wp_prefix())

        if " " in work_product_prefix:
            continue

        configuration.add_option_wp_prefix(work_product_prefix)
        break

    # Input folder types
    while True:
        input_root = \
            click.prompt("Enter the input folder root [s3/file]", type=click.Choice(["s3","file"]), default="s3")
        logging.getLogger('my logger').debug("Input root was set to: " + input_root)

        if " " in input_root:
                continue

        configuration.add_option_inputs_root(input_root)

        # if S3, grab the bucket name
        if input_root == 's3':
            while True:
                bucket_name=configuration.get_S3bucket_name()
                bucket_name=click.prompt("Enter s3 bucket name", type =str,default=bucket_name)
                logging.getLogger('my logger').debug("S3 bucket name was set to: " + bucket_name)

                # TODO validate bucket name format

                configuration.add_option_inputs_S3bucket(bucket_name)

                break
        else:
            logging.getLogger('my logger').debug('Prompting for file root option')
        break

    # save the configuration
    configuration.write()