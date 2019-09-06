import sys

from .cli import bumpv

__VERSION__ = '0.6.1'

py_ver = sys.version.split('\n')[0].split(' ')[0]
DESCRIPTION = f"bumpv: v{__VERSION__} (using Python v{py_ver})"
