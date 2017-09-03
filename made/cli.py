"""
Based on
https://stackoverflow.com/questions/34643620/
how-can-i-split-my-click-commands-each-with-a-set-of-sub-commands-into-multipl

"""
import click
import sys
import os.path


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from made.commands.project_grp.cmd import project
from made.commands.uptime_grp.cmd import uptimerobot


@click.group()
@click.version_option()
def cli():
    pass


cli.add_command(project)
cli.add_command(uptimerobot)


if __name__ == '__main__':
    cli()
