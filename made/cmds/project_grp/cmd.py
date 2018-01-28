import logging
import os

import click

from made.controllers.projects import project_cmd_functions
from made.controllers.projects.project_cmd_functions \
    import project_configure_project_name


@click.group()
@click.pass_context
def project(ctx):
    pass


@project.command('configure',
                 help="Initialise a project configuration in a folder")
@click.argument('folder', default=".", required=False)
@click.pass_obj
def project_configure(ctx, folder):

    logging.getLogger('my logger'). \
        debug('Configuring project in: ' + folder)

    project_configure_project_name(folder)
    project_cmd_functions.project_configure(folder)

    # project_functions.project_create_folder_structures(project_folder_path=folder)
    pass


@project.group('create', help="create various project structures")
def project_create():
    pass


@project_create.command(
    'folder', help="create project folder with the correct format name")
# @click.option('--ttl', '-t')
@click.argument('id')
@click.argument('label')
@click.pass_obj
def project_create_folder(ctx, id, label):
    project_cmd_functions.project_create_folder(id, label)
    pass


@project.group('audit', help="audit project structures")
def project_audit():
    """
    Click command group for all audit activities
    """
    pass


@project_audit.command('name', help="audit project folder name")
@click.pass_obj
def project_audit_name(ctx):
    if project_cmd_functions.is_project_initialised(os.getcwd()):
        if not project_cmd_functions.project_audit_name(
                project_folder=os.getcwd()):
            click.echo("Project folder name does not match "
                       "the correct pattern")
    else:
        click.echo("You are not in an initialised project folder")
    pass


@project_audit.command('tree', help="audit project folder tree")
@click.pass_obj
def project_audit_tree(ctx):
    pass
