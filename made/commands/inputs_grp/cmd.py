import os

import click

from made.commands.project_grp import project_functions
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
        if " " in user_source_id:
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


    pass


@input.command('audit')
@click.pass_obj
def input_audit(ctx):
    audit_result = inputs_functions.input_audit_path(os.getcwd())
    utils.pretty_print(audit_result)
    pass
