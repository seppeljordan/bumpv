# bumpv

A more modern and streamlined fork of [bumpversion](https://github.com/peritus/bumpversion)

Version-bump your software with a single command!

A small command line tool to simplify releasing software by updating all
version strings in your source code by the correct increment. Also
creates commits and tags:

  - version formats are highly configurable
  - works without any VCS, but happily reads tag information from and
    writes commits and tags to Git and Mercurial if available
  - just handles text files, so it's not specific to any programming
    language

[![image](https://travis-ci.org/kylie-a/bumpv.png?branch=master)](https://travis-ci.org/peritus/bumpv)

# Installation

You can download and install the latest version of this software from
the Python package index (PyPI) as follows:

    pip install --upgrade bumpv

# Usage

`bumpv` can be used as a CLI tool or as installed library as part of a larger CI/CD system.

## CLI

```bash
bumpv bump [major|minor|patch] [-d | --allow-dirty] 
```

# Configuration

All options can optionally be specified in a config file called
`.bumpv.cfg` so that once you know how `bumpv` needs to be configured
for one particular software package, you can run it without specifying
options later. You should add that file to VCS so others can also bump
versions.

Options on the command line take precedence over those from the config
file, which take precedence over those derived from the environment and
then from the defaults.

Example `.bumpv.cfg`:

    [bumpv]
    current_version = 0.2.9
    commit = True
    tag = True
    
    [bumpv:file:setup.py]

If no `.bumpv.cfg` exists, `bumpv` will also look into `setup.cfg` for
configuration.

# Global configuration

General configuration is grouped in a `[bumpv]` section.

  - `current_version =`  
    **no default value** (required)
    
    The current version of the software package before bumping.
    
    Also available as `--current-version` (e.g. `bumpv
    --current-version 0.5.1 patch setup.py`)

  - `new_version =`  
    **no default value** (optional)
    
    The version of the software package after the increment. If not
    given will be automatically determined.
    
    Also available as `--new-version` (e.g. \`to go from 0.5.1 directly
    to 0.6.8\`: `bumpv --current-version 0.5.1 --new-version 0.6.8 patch
    setup.py`).

  - `tag = (True | False)`  
    **default:** False (<span class="title-ref">Don't create a
    tag</span>)
    
    Whether to create a tag, that is the new version, prefixed with the
    character "`v`". If you are using git, don't forget to `git-push`
    with the `--tags` flag.
    
    Also available on the command line as `(--tag | --no-tag)`.

  - `tag_name =`  
    **default:** `v{new_version}`
    
    The name of the tag that will be created. Only valid when using
    `--tag` / `tag = True`.
    
    This is templated using the [Python Format String
    Syntax](http://docs.python.org/2/library/string.html#format-string-syntax).
    Available in the template context are `current_version` and
    `new_version` as well as all environment variables (prefixed with
    `$`). You can also use the variables `now` or `utcnow` to get a
    current timestamp. Both accept datetime formatting (when used like
    as in `{now:%d.%m.%Y}`).
    
    Also available as `--tag-name` (e.g. `bumpv --message 'Jenkins Build
    {$BUILD_NUMBER}: {new_version}' patch`).

  - `commit = (True | False)`  
    **default:** `False` (<span class="title-ref">Don't create a
    commit</span>)
    
    Whether to create a commit using git or Mercurial.
    
    Also available as `(--commit | --no-commit)`.

  - `message =`  
    **default:** `Bump version: {current_version} → {new_version}`
    
    The commit message to use when creating a commit. Only valid when
    using `--commit` / `commit = True`.
    
    This is templated using the [Python Format String
    Syntax](http://docs.python.org/2/library/string.html#format-string-syntax).
    Available in the template context are `current_version` and
    `new_version` as well as all environment variables (prefixed with
    `$`). You can also use the variables `now` or `utcnow` to get a
    current timestamp. Both accept datetime formatting (when used like
    as in `{now:%d.%m.%Y}`).
    
    Also available as `--message` (e.g.: `bumpv --message
    '[{now:%Y-%m-%d}] Jenkins Build {$BUILD_NUMBER}: {new_version}'
    patch`)


# Part specific configuration

A version string consists of one or more parts, e.g. the version `1.0.2`
has three parts, separated by a dot (`.`) character. In the default
configuration these parts are named
<span class="title-ref">major</span>,
<span class="title-ref">minor</span>,
<span class="title-ref">patch</span>, however you can customize that
using the `parse`/`serialize` option.

By default all parts considered numeric, that is their initial value is
`0` and they are increased as integers. Also, the value `0` is
considered to be optional if it's not needed for serialization, i.e. the
version `1.4.0` is equal to `1.4` if `{major}.{minor}` is given as a
`serialize` value.

For advanced versioning schemes, non-numeric parts may be desirable
(e.g. to identify [alpha or beta
versions](http://en.wikipedia.org/wiki/Software_release_life_cycle#Stages_of_development),
to indicate the stage of development, the flavor of the software package
or a release name). To do so, you can use a `[bumpv:part:…]` section
containing the part's name (e.g. a part named `release_name` is
configured in a section called `[bumpv:part:release_name]`.

The following options are valid inside a part configuration:

  - `values =`  
    **default**: numeric (i.e. `0`, `1`, `2`, …)
    
    Explicit list of all values that will be iterated when bumping that
    specific part.
    
    Example:
    
        [bumpv:part:release_name]
        values =
          witty-warthog
          ridiculous-rat
          marvelous-mantis

  - `optional_value =`  
    **default**: The first entry in `values =`.
    
    If the value of the part matches this value it is considered
    optional, i.e. it's representation in a `--serialize` possibility is
    not required.
    
    Example:
    
        [bumpv]
        current_version = 1.alpha
        parse = (?P<num>\d+)\.(?P<release>.*)
        serialize =
          {num}.{release}
          {num}
        
        [bumpv:part:release]
        optional_value = gamma
        values =
          alpha
          beta
          gamma
    
    Here, `bumpv release` would bump `1.alpha` to `1.beta`. Executing
    `bumpv release` again would bump `1.beta` to `1`, because
    <span class="title-ref">release</span> being `gamma` is configured
    optional.

  - `first_value =`  
    **default**: The first entry in `values =`.
    
    When the part is reset, the value will be set to the value specified
    here.

# File specific configuration

`[bumpv:file:…]`

  - `parse =`  
    **default:** `(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)`
    
    Regular expression (using [Python regular expression
    syntax](http://docs.python.org/2/library/re.html#regular-expression-syntax))
    on how to find and parse the version string.
    
    Is required to parse all strings produced by `serialize =`. Named
    matching groups ("`(?P<name>...)`") provide values to as the `part`
    argument.
    
    Also available as `--parse`

  - `serialize =`  
    **default:** `{major}.{minor}.{patch}`
    
    Template specifying how to serialize the version parts back to a
    version string.
    
    This is templated using the [Python Format String
    Syntax](http://docs.python.org/2/library/string.html#format-string-syntax).
    Available in the template context are parsed values of the named
    groups specified in `parse =` as well as all environment variables
    (prefixed with `$`).
    
    Can be specified multiple times, bumpv will try the serialization
    formats beginning with the first and choose the last one where all
    values can be represented like this:
    
        serialize =
          {major}.{minor}
          {major}
    
    Given the example above, the new version *1.9* it will be serialized
    as `1.9`, but the version *2.0* will be serialized as `2`.
    
    Also available as `--serialize`. Multiple values on the command line
    are given like `--serialize {major}.{minor} --serialize {major}`

  - `search =`  
    **default:** `{current_version}`
    
    Template string how to search for the string to be replaced in the
    file. Useful if the remotest possibility exists that the current
    version number might be multiple times in the file and you mean to
    only bump one of the occurences. Can be multiple lines, templated
    using [Python Format String
    Syntax](http://docs.python.org/2/library/string.html#format-string-syntax).

  - `replace =`  
    **default:** `{new_version}`
    
    Template to create the string that will replace the current version
    number in the file.
    
    Given this `requirements.txt`:
    
        Django>=1.5.6,<1.6
        MyProject==1.5.6
    
    using this `.bumpv.cfg` will ensure only the line containing
    `MyProject` will be changed:
    
        [bumpv]
        current_version = 1.5.6
        
        [bumpv:file:requirements.txt]
        search = MyProject=={current_version}
        replace = MyProject=={new_version}
    
    Can be multiple lines, templated using [Python Format String
    Syntax](http://docs.python.org/2/library/string.html#format-string-syntax).

# Options

Most of the configuration values above can also be given as an option.
Additionally, the following options are available:

  - `--dry-run, -n`
    Don't touch any files, just pretend. Best used with `--verbose`.

  - `--allow-dirty`
    Normally, bumpv will abort if the working directory is dirty to
    protect yourself from releasing unversioned files and/or overwriting
    unsaved changes. Use this option to override this check.

  - `--verbose`
    Print useful information to stderr

  - `--list`
    List machine readable information to stdout for consumption by other
    programs.
    
    Example output:
    
        current_version=0.0.18
        new_version=0.0.19

  - `-h, --help`
    Print help and exit

# License

bumpv is licensed under the MIT License - see the LICENSE.rst file for details
