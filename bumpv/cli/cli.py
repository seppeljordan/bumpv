# -*- coding: utf-8 -*-

"""Console script for deploy_py."""
import sys

import click

from ..client import BumpClient
from ..client.config import Configuration
from ..client.vcs import (
    WorkingDirectoryIsDirtyException,
)

DEFAULTS = {
    "verbose": "0",
    "list": "False",
    "allow_dirty": "False",
}


@click.group()
def bumpv(args=None):
    return 0


@bumpv.command()
@click.argument('part')
@click.option("-v", '--verbose', count=True, default=0, required=False)
@click.option("-l", '--list', "show_list", is_flag=True)
@click.option("-d", '--allow-dirty', is_flag=True)
@click.option("-o", '--output', default="yaml")
@click.option('--dry-run', is_flag=True)
def bump(part, verbose, show_list, allow_dirty, output, dry_run):
    config = Configuration()
    try:
        client = BumpClient(config, verbose=verbose, show_list=show_list, allow_dirty=allow_dirty)
    except WorkingDirectoryIsDirtyException:
        sys.exit(1)

    client.bump(part, dry_run)

    output_func = getattr(client, output)

    print(output_func())


if __name__ == "__main__":
    sys.exit(bumpv())  # pragma: no cover
