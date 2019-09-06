# Changes

**unreleased** 

**v0.6.3**

**v0.5.3**

  - Fix bug where `--new-version` value was not used when config was
    present (thanks @cscetbon @ecordell
    ([\#60](https://github.com/peritus/bumpv/pull/60))
  - Preserve case of keys config file (thanks theskumar
    [\#75](https://github.com/peritus/bumpv/pull/75))
  - Windows CRLF improvements (thanks @thebjorn)

**v0.5.1**

  - Document file specific options `search =` and `replace =`
    (introduced in 0.5.0)
  - Fix parsing individual labels from `serialize =` config even if
    there are characters after the last label (thanks @mskrajnowski
    [\#56](https://github.com/peritus/bumpv/pull/56)).
  - Fix: Don't crash in git repositories that have tags that contain
    hyphens ([\#51](https://github.com/peritus/bumpv/pull/51))
    ([\#52](https://github.com/peritus/bumpv/pull/52)).
  - Fix: Log actual content of the config file, not what ConfigParser
    prints after reading it.
  - Fix: Support multiline values in `search =`
  - also load configuration from `setup.cfg` (thanks @t-8ch
    [\#57](https://github.com/peritus/bumpv/pull/57)).

**v0.5.0**

This is a major one, containing two larger features, that require some
changes in the configuration format. This release is fully backwards
compatible to *v0.4.1*, however deprecates two uses that will be removed
in a future version.

  - New feature: [Part specific configuration](#part-specific-configuration)
  - New feature: [File specific configuration](#file-specific-configuration)
  - New feature: parse option can now span multiple line (allows to
    comment complex regular expressions. See [re.VERBOSE in the Python
    documentation](https://docs.python.org/library/re.html#re.VERBOSE)
    for details, [this
    testcase](https://github.com/peritus/bumpv/blob/165e5d8bd308e9b7a1a6d17dba8aec9603f2d063/tests.py#L1202-L1211)
    as an example.)
  - New feature: `--allow-dirty`
    ([\#42](https://github.com/peritus/bumpv/pull/42)).
  - Fix: Save the files in binary mode to avoid mutating newlines
    (thanks @jaraco [\#45](https://github.com/peritus/bumpv/pull/45)).
  - License: bumpv is now licensed under the MIT License
    ([\#47](https://github.com/peritus/bumpv/issues/47))
  - Deprecate multiple files on the command line (use a [configuration
    file](#configuration) instead, or invoke `bumpv` multiple times)
  - Deprecate 'files =' configuration (use [file specific
    configuration](#file-specific-configuration) instead)

**v0.4.1**

  - Add --list option
    ([\#39](https://github.com/peritus/bumpv/issues/39))
  - Use temporary files for handing over commit/tag messages to git/hg
    ([\#36](https://github.com/peritus/bumpv/issues/36))
  - Fix: don't encode stdout as utf-8 on py3
    ([\#40](https://github.com/peritus/bumpv/issues/40))
  - Fix: logging of content of config file was wrong

**v0.4.0**

  - Add --verbose option
    ([\#21](https://github.com/peritus/bumpv/issues/21)
    [\#30](https://github.com/peritus/bumpv/issues/30))
  - Allow option --serialize multiple times

**v0.3.8**

  - Fix: --parse/--serialize didn't work from cfg
    ([\#34](https://github.com/peritus/bumpv/issues/34))

**v0.3.7**

  - Don't fail if git or hg is not installed (thanks @keimlink)
  - "files" option is now optional
    ([\#16](https://github.com/peritus/bumpv/issues/16))
  - Fix bug related to dirty work dir
    ([\#28](https://github.com/peritus/bumpv/issues/28))

**v0.3.6**

  - Fix --tag default (thanks @keimlink)

**v0.3.5**

  - add {now} and {utcnow} to context
  - use correct file encoding writing to config file. NOTE: If you are
    using Python2 and want to use UTF-8 encoded characters in your
    config file, you need to update ConfigParser like using 'pip install
    -U configparser'
  - leave current\_version in config even if available from vcs tags
    (was confusing)
  - print own version number in usage
  - allow bumping parts that contain non-numerics
  - various fixes regarding file encoding

**v0.3.4**

  - bugfix: tag\_name and message in .bumpv.cfg didn't have an effect
    ([\#9](https://github.com/peritus/bumpv/issues/9))

**v0.3.3**

  - add --tag-name option
  - now works on Python 3.2, 3.3 and PyPy

**v0.3.2**

  - bugfix: Read only tags from <span class="title-ref">git
    describe</span> that look like versions

**v0.3.1**

  - bugfix: `--help` in git workdir raising AssertionError
  - bugfix: fail earlier if one of files does not exist
  - bugfix: `commit = True` / `tag = True` in .bumpv.cfg had no effect


**v0.3.0**

  - **BREAKING CHANGE** The `--bump` argument was removed, this is now
    the first positional argument. If you used `bumpv --bump major`
    before, you can use `bumpv major` now. If you used `bumpv` without
    arguments before, you now need to specify the part (previous default
    was `patch`) as in `bumpv patch`).

**v0.2.2**

  - add --no-commit, --no-tag

**v0.2.1**

  - If available, use git to learn about current version

**v0.2.0**

  - Mercurial support

**v0.1.1**

  - Only create a tag when it's requested (thanks @gvangool)

**v0.1.0**

  - Initial public version
