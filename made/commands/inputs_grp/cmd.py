import click
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
    input_functions.input_create("inp23", "spreadies", "tab", 1)
    pass


@input.command('delete')
@click.argument('names', nargs=-1, required=True)
@click.pass_obj
def uptimerobot_delete(ctx, names):
    pass
