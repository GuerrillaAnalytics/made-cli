import click
import re
import os
from pathlib import Path
import configparser


class ProjectException(Exception):
    pass


def check_project_name(project_name):
    """Check project name matches a pattern."""
    pattern = re.compile("^ds[0-9]{3}(_([a-zA-Z0-9])*)?")

    if re.match(pattern, project_name) is None:
        raise ProjectException("Invalid format project name: " + project_name)

    return project_name


def is_project_initialised(folder_location):
    """Check a folder does not exist and can be created"""

    cfg = os.path.join(folder_location, "made.config")
    # Folder exists and config exists
    if not Path(cfg).exists():
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


def project_init_wp(configParser):
    """Initialise the work product prefix you want to use into
    a configParser"""

    section_name = "work_products"
    option_name = "prefix"
    option_value = "wp"

    # if the option has been set before, grab the value
    if configParser.has_section(section_name):
        if configParser.has_option(section_name, option_name):
            option_value = configParser.get(section_name, option_name)
    else:
        configParser.add_section(section_name)

    option_value = click.prompt("Enter a work_product prefix", default=option_value, type=str)
    configParser.set(section_name, option_name, option_value)


def project_init_pm_folder(project_folder_path):
    """Create a pm folder tree in a given project folder"""

    # Make the pm folder tree
    pm_folder = make_folder_if_doesnt_exist(os.path.join(project_folder_path, "pm"))
    make_folder_if_doesnt_exist(os.path.join(pm_folder, "01_initiate"))
    make_folder_if_doesnt_exist(os.path.join(pm_folder, "02_plan"))
    make_folder_if_doesnt_exist(os.path.join(pm_folder, "03_execute"))
    make_folder_if_doesnt_exist(os.path.join(pm_folder, "04_control"))
    make_folder_if_doesnt_exist(os.path.join(pm_folder, "05_close"))


def project_init(project_folder_path):
    """Creates a project configuration. Assumes current directory
    is root of project"""

    config_file = os.path.join(project_folder_path, "made.config")
    config = configparser.ConfigParser()

    # Create a blank file
    if is_project_initialised(project_folder_path) is False:
        open(config_file, 'a').close()

    project_init_pm_folder(project_folder_path)

    make_folder_if_doesnt_exist(os.path.join(project_folder_path, "wp"))
    make_folder_if_doesnt_exist(os.path.join(project_folder_path, "inputs"))

    project_init_wp(config)
    with open(config_file, 'w') as configfile:
        config.write(configfile)
    pass

    # section_name = "PostgreSQL"
    #
    # # if it has the section, ask if user should reconfigure or remove
    # if config.has_section(section_name):
    #     reconfigure_answer = click.confirm("Do you wish to keep the PostgreSQL configuration?")
    #     if reconfigure_answer is True:
    #         option_name = "port"
    #         question = "Please enter a port number"
    #         if config.has_option(section_name, option_name, ):
    #             option_value = config.get(section_name, option_name)
    #             option_value = click.prompt(question, default=option_value)
    #             config.set(section_name, option_name, option_value)
    #     else:
    #         config.remove_section(section_name)
    # else:
    #     reconfigure_answer = click.confirm("Do you wish to configure PostgreSQL?")
    #     if reconfigure_answer is True:
    #         config.add_section(section_name)
    #
    # with open('cfg', 'wt') as configfile:
    #     config.write(configfile)


def project_create_folder(id, label):
    """Creates a project folder if possible in the current directory"""

    project_name = id.lower() + "_" + label.lower()
    check_project_name(project_name)

    # TODO check id doesn't exist in same directory

    project_location = os.path.join(os.getcwd(), project_name)
    make_folder_if_doesnt_exist(project_location)

    return project_location
