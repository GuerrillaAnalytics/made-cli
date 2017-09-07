import click
from made.commands.project_grp import project_functions as project_functions
import os


@click.group()
@click.pass_context
def project(ctx):
    pass


@project.command('init', help="Initialise a project")
@click.argument('folder', default=".", required=False)
# @click.option('--organization', '-o', default='')
# @click.argument('url')
@click.pass_obj
def project_init(ctx, folder):
    if folder == ".":
        folder = os.getcwd()
    project_functions.project_init(project_folder_path=folder)
    pass


@project.group('create', help="create various project structures")
def project_create():
    pass


@project_create.command('folder', help="create project folder with the correct format name")
# @click.option('--ttl', '-t')
@click.argument('id')
@click.argument('label')
@click.pass_obj
def project_create_folder(ctx, id, label):
    project_functions.project_create_folder(id, label)
    pass


@project.group('audit', help="audit project structures")
def project_audit():
    pass


@project_audit.command('name', help="audit project folder name")
@click.pass_obj
def project_audit_name(ctx):

    if project_functions.is_project_initialised(os.getcwd()):
        if not project_functions.project_audit_name():
            click.echo("Project folder name does not match the correct pattern")
    else:
        click.echo("You are not in an initialised project folder")
    pass