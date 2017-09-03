import click
from made.commands.project_grp import project_functions as project_functions


@click.group()
@click.pass_context
def project(ctx):
    pass


@project.command('temp')
@click.option('--jumpstart', '-j', default=True)
@click.option('--organization', '-o', default='')
@click.argument('url')
@click.pass_obj
def cloudflare_zone_add(ctx, url, jumpstart, organization):
    pass


@project.group('create', help="create various project structures")
def project_create():
    pass


@project_create.command('folder', help = "create project folder with the correct format name")
# @click.option('--ttl', '-t')
@click.argument('id')
@click.argument('label')
@click.pass_obj
def project_create_folder(ctx, id, label):
    project_functions.project_create_folder(id, label)
    pass


@project_create.command('edit')
@click.option('--ttl', '-t')
@click.argument('domain')
@click.argument('name')
@click.argument('type')
@click.argument('content')
@click.pass_obj
def cloudflare_record_edit(ctx, domain):
    pass
