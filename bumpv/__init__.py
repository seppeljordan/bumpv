import sys

from .cli import bumpv
from .client import BumpClient, exceptions
from .client.config import Configuration
from .client.versioning import Version

__VERSION__ = '0.1.0'

py_ver = sys.version.split('\n')[0].split(' ')[0]
DESCRIPTION = f"bumpv: v{__VERSION__} (using Python v{py_ver})"
