import click


@click.group()
@click.pass_context
def cloudflare(ctx):
    pass


@cloudflare.group('zone')
@click.pass_context
def cloudflare_zone():
    pass


@cloudflare_zone.command('add')
@click.option('--jumpstart', '-j', default=True)
@click.option('--organization', '-o', default='')
@click.argument('url')
@click.pass_obj
def cloudflare_zone_add(ctx, url, jumpstart, organization):
    pass


@cloudflare.group('record')
def cloudflare_record():
    pass


@cloudflare_record.command('add')
@click.option('--ttl', '-t')
@click.argument('domain')
@click.argument('name')
@click.argument('type')
@click.argument('content')
@click.pass_obj
def cloudflare_record_add(ctx, domain, name, type, content, ttl):
    pass


@cloudflare_record.command('edit')
@click.option('--ttl', '-t')
@click.argument('domain')
@click.argument('name')
@click.argument('type')
@click.argument('content')
@click.pass_obj
def cloudflare_record_edit(ctx, domain):
    pass
