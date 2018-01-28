import os
import logging
import click

from made.commands.inputs_grp.input_functions import validate_input_version
from made.controllers.config import Config
from made.controllers.inputs import input_manager_factory
from made.controllers.inputs import inputs_functions
from made import utils


@click.group()
@click.pass_context
def input(ctx):
    pass


@input.command('create')
# @click.option('--alert', '-a', default=True)
# @click.argument('name')
# @click.argument('url')
@click.pass_obj
def input_create(ctx):

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
    pass


@input.command('audit')
@click.pass_obj
def input_audit(ctx):
    audit_result = inputs_functions.input_audit_path(os.getcwd())
    utils.pretty_print(audit_result)
    pass
