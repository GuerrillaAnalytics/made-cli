import click


@click.group()
@click.pass_context
def uptimerobot(ctx):
    pass


@uptimerobot.command('add')
@click.option('--alert', '-a', default=True)
@click.argument('name')
@click.argument('url')
@click.pass_obj
def uptimerobot_add(ctx, name, url, alert):
    pass


@uptimerobot.command('delete')
@click.argument('names', nargs=-1, required=True)
@click.pass_obj
def uptimerobot_delete(ctx, names):
    pass
