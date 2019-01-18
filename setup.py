import re
from setuptools import setup

description = 'Version-bump your software with a single command!'

long_description = re.sub(
  "\`(.*)\<#.*\>\`\_",
  r"\1",
  str(open('README.rst', 'rb').read()).replace(description, '')
)

setup(
    name='bumpversion',
    version='0.5.4-dev',
    url='https://github.com/kylie-a/bumpversion',
    author='Kylie Auld',
    author_email='kylie.a@protonmail.com',
    license='MIT',
    packages=['bumpversion'],
    description=description,
    long_description=long_description,
    entry_points={
        'console_scripts': [
            'bumpversion = bumpversion:main',
        ]
    },
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
    ),
)
