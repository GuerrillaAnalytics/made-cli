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


def check_project_location(folder_location):
    """Check a folder does not exist and can be created"""
    if not os.path.exists(folder_location):
        raise OSError("Project folder location does not exist " + folder_location)


def make_folder_if_doesnt_exist(parent_path, folder_name):
    """Utility function to create a folder if it doesn't already exist"""
    folder = os.path.join(parent_path, folder_name)
    if not os.path.exists(folder):
        click.echo("creating folder " + folder_name)
        os.makedirs(folder)

    return folder


def build_project_config(cfg, existing):
    """Creates a project configuration"""

    config = configparser.ConfigParser()
    config.read(cfg)

    section_name = "PostgreSQL"

    # if it has the section, ask if user should reconfigure or remove
    if config.has_section(section_name):
        reconfigure_answer = click.confirm("Do you wish to keep the PostgreSQL configuration?")
        if reconfigure_answer is True:
            option_name = "port"
            question = "Please enter a port number"
            if config.has_option(section_name, option_name, ):
                option_value = config.get(section_name, option_name)
                option_value = click.prompt(question, default=option_value)
                config.set(section_name, option_name, option_value)
        else:
            config.remove_section(section_name)
    else:
        reconfigure_answer = click.confirm("Do you wish to configure PostgreSQL?")
        if reconfigure_answer is True:
            config.add_section(section_name)

    with open('cfg', 'wt') as configfile:
        config.write(configfile)


def create_folder(id, label):
    """Creates a project folder if possible in the current directory"""
    project_name = id.lower() + "_" + label.lower()
    check_project_name(project_name)

    # TODO check id doesn't exist in same directory

    make_folder_if_doesnt_exist(os.getcwd(), project_name)


def initialise_project(name, location):
    """Command for initialising a project"""

    # Check the project name is correct
    try:
        check_project_name(name)
    except ProjectException as e:
        click.echo(click.style(e.args[0], fg='red'))

    # Check the project location exists
    try:
        check_project_location(location)
    except OSError as e:
        click.echo(click.style(e.args[0], fg='red'))

    project_path = os.path.join(location, name)

    # if the project folder does not exist, create it
    if not os.path.exists(project_path):
        os.makedirs(project_path)

    cfg = os.path.join(location, name, "guerrilla.config")
    # Folder exists and config exists
    if Path(cfg).exists():
        print("Found existing config")
        click.confirm('A config file already exists in the folder. Do you want to continue?', abort=True)
        build_project_config(cfg, existing=True)
    else:
        # Folder exists with no config
        Path(cfg).touch()
        build_project_config(cfg, existing=False)

    # Make the pm folder tree
    pm_folder = make_folder_if_doesnt_exist(project_path, "pm")

    make_folder_if_doesnt_exist(pm_folder, "01_initiate")
    make_folder_if_doesnt_exist(pm_folder, "02_plan")
    make_folder_if_doesnt_exist(pm_folder, "03_execute")
    make_folder_if_doesnt_exist(pm_folder, "04_control")
    make_folder_if_doesnt_exist(pm_folder, "05_close")

    make_folder_if_doesnt_exist(project_path, "wp")
    pass
