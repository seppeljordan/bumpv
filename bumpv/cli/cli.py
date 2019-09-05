# -*- coding: utf-8 -*-

"""Console script for deploy_py."""
import argparse
import json
import sys

import click
import yaml

from ..client import BumpClient
from ..client.config import Configuration


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
@click.option("-o", '--output', is_flag=True)
def bump(part, verbose, show_list, allow_dirty, output):
    config = Configuration()
    client = BumpClient(config, verbose=verbose, show_list=show_list, allow_dirty=allow_dirty)
    client.bump(part)


if __name__ == "__main__":
    sys.exit(bumpv())  # pragma: no cover
