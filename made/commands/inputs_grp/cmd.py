import click
import os
from made.commands.inputs_grp import inputs_functions as input_functions


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
    user_root = os.getcwd()
    user_source_id = click.prompt('Please enter an input ID', type=str)
    user_source_name = click.prompt('Please enter a schema name to load into', type=str)
    user_version = click.prompt('Please enter a version', type=int)
    input_functions.input_create(root_folder=user_root, source_id=user_source_id, source_name=user_source_name,
                                 version=user_version)
    pass


@input.command('delete')
@click.argument('names', nargs=-1, required=True)
@click.pass_obj
def uptimerobot_delete(ctx, names):
    pass
