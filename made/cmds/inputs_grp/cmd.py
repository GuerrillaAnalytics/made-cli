import logging
import os

import click

from made import utils
from made.controllers.inputs import inputs_functions
from made.controllers.inputs.inputs_functions import cmd_input_create


@click.group()
@click.pass_context
def input(ctx):
    """Commands for managing input sources"""
    pass


@input.command('create')
# @click.option('--alert', '-a', default=True)
# @click.argument('name')
# @click.argument('url')
@click.pass_obj
def input_create(ctx):
    """Create a new input source"""
    cmd_input_create()

    pass


@input.command('audit')
@click.pass_obj
def input_audit(ctx):
    audit_result = inputs_functions.input_audit_path(os.getcwd())
    utils.pretty_print(audit_result)
    pass


@input.command('new_version')
@click.pass_obj
def input_new_version(ctx):
    """Create a new version of an existing input source"""
    result = inputs_functions.input_new_version()
    logging.getLogger('my logger').debug("Created version " + str(result))
    pass
