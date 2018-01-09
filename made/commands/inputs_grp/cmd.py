import os

import click

from made.controllers.inputs import inputs_functions
from made import utils
from made.controllers.config import Config


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

    config = Config(os.getcwd())

    while True:
        user_source_id = click.prompt('Please enter an input ID', type=str)
        if " " in user_source_id:
            continue
        break

    # source name
    while True:
        user_source_name = click.prompt('Please enter a schema name to load into', type=str)
        if len(user_source_name.strip()) == 0:
            continue
        if " " in user_source_name.strip():
            continue
        break

    # version of input
    while True:
        user_version = click.prompt('Please enter a version', type=int, default=1)
        if user_version <= 0:
            continue
        break

    config.get
    #    inputs_functions.input_create(root_folder=user_root, source_id=user_source_id, source_name=user_source_name,
    #                              version=user_version)
    pass


@input.command('audit')
@click.pass_obj
def input_audit(ctx):
    audit_result = inputs_functions.input_audit_path(os.getcwd())
    utils.pretty_print(audit_result)
    pass
