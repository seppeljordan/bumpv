# -*- coding: utf-8 -*-

"""Console script for deploy_py."""
import sys

import click

from ..client import BumpClient
from ..client import exceptions


@click.group()
def bumpv(args=None):
    return 0


@bumpv.command()
@click.argument('part', type=click.Choice(["major", "minor", "patch"]))
@click.option("-v", '--verbose', count=True, default=0, required=False, help="Use to increase verbosity of logging. Ex: -vv")
@click.option("-d", '--allow-dirty', is_flag=True, help="Allow bumping the version while the working tree is dirty")
@click.option("-o", '--output', default="yaml", type=click.Choice(["yaml", "json"]), help="Choose output format. Default is 'yaml'")
@click.option('--dry-run', is_flag=True, help="see what would happen without touching any files. Best used with -vv")
def bump(part, verbose, allow_dirty, output, dry_run):
    try:
        client = BumpClient(verbosity=verbose, allow_dirty=allow_dirty)
    except exceptions.WorkingDirectoryIsDirtyException:
        sys.exit(1)

    try:
        client.bump(part, dry_run)
    except exceptions.InvalidTargetFile as err:
        click.echo(f"error attempting to bump the version: {err}")
        sys.exit(1)
    except exceptions.VCSCommandError as err:
        click.echo(f"error attempting to run VCS command:\n\n\t{' '.join(err.command)}\n")
        click.echo("Error message from VCS:\n")
        click.echo(err.message)
        sys.exit(1)

    output_func = getattr(client, output)

    print(output_func())


if __name__ == "__main__":
    sys.exit(bumpv())  # pragma: no cover
