import sys

from .bumpversion import main
from .utils import get_description

__VERSION__ = '0.5.4-dev'

py_ver = sys.version.split('\n')[0].split(' ')[0]
DESCRIPTION = f"bumpversion: v{__VERSION__} (using Python v{py_ver})"
