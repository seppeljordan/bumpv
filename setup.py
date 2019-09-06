import re
from setuptools import setup, find_packages

description = 'Version-bump your software with a single command!'

long_description = re.sub(
  "\`(.*)\<#.*\>\`\_",
  r"\1",
  str(open('README.md', 'rb').read()).replace(description, '')
)

setup(
    name='bumpv',
    version='0.1.0',
    url='https://github.com/kylie-a/bumpv',
    author='Kylie Auld',
    author_email='kylie.a@protonmail.com',
    license='MIT',
    packages=find_packages(),
    description=description,
    long_description=long_description,
    install_requires=[
        "Click==7.0",
        "pyaml==19.4.1",
    ],
    entry_points={
        'console_scripts': [
            'bumpv = bumpv:bumpv',
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
