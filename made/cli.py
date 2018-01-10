"""
Based on
https://stackoverflow.com/questions/34643620/
how-can-i-split-my-click-commands-each-with-a-set-of-sub-commands-into-multipl

"""
import sys
import os.path
import logging

# bizarre fix to PYTHONPATH problems
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import click
import sys
import os.path

from made.commands.project_grp import project_functions
import made.controllers.config

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from made.commands.project_grp.cmd import project
from made.commands.inputs_grp.cmd import input


@click.group()
@click.version_option()
def cli():
    pass


cli.add_command(project)
cli.add_command(input)


if __name__ == '__main__':

    # set up logging
    logger = logging.getLogger("my logger")
    logger.setLevel(logging.DEBUG)
    # Format for our loglines
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
    # Setup console logging
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    # Setup file logging as well
    # fh = logging.FileHandler(LOG_FILENAME)
    # fh.setLevel(logging.DEBUG)
    # fh.setFormatter(formatter)
    # logger.addHandler(fh)

    # Check if project is configured
    configuration = made.controllers.config.Config(os.getcwd())
    if not configuration.has_config_file():
        click.echo(click.style('A project has not been configured in this folder', fg='yellow'))
        while True:
            if click.confirm('Do you want to configure a project here?', abort=True):
                logging.getLogger("my logger").debug("Configuring project based on confirmation prompt")
                project_functions.project_configure(os.getcwd())
                break

    else:
        logging.getLogger("my logger").debug("Project already configured here")
        logging.getLogger("my logger").debug("Using this configuration and continuing with command")
        cli()
