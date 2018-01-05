import click
from made.commands.project_grp import project_functions as project_functions
import os
from made.utils.config import Config


@click.group()
@click.pass_context
def project(ctx):
    pass


@project.command('init', help="Initialise a project configuration")
@click.argument('folder', default=".", required=False)
# @click.option('--organization', '-o', default='')
# @click.argument('url')
@click.pass_obj
def project_init(ctx, folder):
    if folder == ".":
        folder = os.getcwd()

    # create new configuration class for this project
    configuration = Config(folder)
    configuration.has_config_file()

    # Enter a project root folder
    while True:

        project_root = \
            click.prompt('Please enter project root', type=str, default=configuration.get_option_project_root())
        if " " in project_root:
            continue

        # TODO validate the path
        if project_root == "":
            project_root = configuration.get_option_project_root()

            configuration.add_option_project_root(project_root)
        break

    # Enter a work product prefix
    while True:
        work_product_prefix = \
            click.prompt('Please enter a work product prefix', type=str, default=configuration.get_option_wp_prefix())

        if " " in work_product_prefix:
            continue

        configuration.add_option_wp_prefix(work_product_prefix)
        break

    # save the configuration
    configuration.write()

    project_functions.project_create_folder_structures(project_folder_path=folder)
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
        if not project_functions.project_audit_name(project_folder=os.getcwd()):
            click.echo("Project folder name does not match the correct pattern")
    else:
        click.echo("You are not in an initialised project folder")
    pass


@project_audit.command('tree', help="audit project folder tree")
@click.pass_obj
def project_audit_tree(ctx):
    pass