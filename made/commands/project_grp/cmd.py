import click
# from made.commands.project_grp import project_functions


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


@project.group('create')
def project_create():
    pass


@project_create.command('folder')
# @click.option('--ttl', '-t')
@click.argument('id')
@click.argument('label')
@click.pass_obj
def project_create_folder(ctx, id, label):
    project_create(id, label)
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
