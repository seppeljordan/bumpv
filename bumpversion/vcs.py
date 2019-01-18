import os
import subprocess
from tempfile import NamedTemporaryFile

from .exceptions import WorkingDirectoryIsDirtyException
from .utils import get_logger


logger = get_logger()


def get_vcs(defaults):
    for vcs in VCS:
        if vcs.is_usable():
            try:
                vcs.assert_nondirty()
            except WorkingDirectoryIsDirtyException as e:
                if not defaults['allow_dirty']:
                    logger.warn(f"{e.message}\n\nUse --allow-dirty to override this if you know what you're doing.")
                    raise
            return vcs


class BaseVCS(object):
    _TEST_USABLE_COMMAND = []
    _COMMIT_COMMAND = []

    @classmethod
    def commit(cls, message):
        with NamedTemporaryFile('wb', delete=False) as f:
            f.write(message.encode('utf-8'))

        subprocess.check_output(
            cls._COMMIT_COMMAND + [f.name],
            env=dict(list(os.environ.items()) + [(b'HGENCODING', b'utf-8')])
        )
        os.unlink(f.name)

    @classmethod
    def is_usable(cls):
        try:
            return subprocess.call(
                cls._TEST_USABLE_COMMAND,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE
            ) == 0
        except OSError as e:
            if e.errno == 2:
                # mercurial is not installed then, ok.
                return False
            raise


class Git(BaseVCS):
    _TEST_USABLE_COMMAND = ["git", "rev-parse", "--git-dir"]
    _COMMIT_COMMAND = ["git", "commit", "-F"]

    @classmethod
    def assert_nondirty(cls):
        lines = [
            line.strip() for line in
            subprocess.check_output(
                ["git", "status", "--porcelain"]).splitlines()
            if not line.strip().startswith(b"??")
        ]

        if lines:
            raise WorkingDirectoryIsDirtyException(
                "Git working directory is not clean:\n{}".format(
                    b"\n".join(lines)))

    @classmethod
    def latest_tag_info(cls):
        try:
            # git-describe doesn't update the git-index, so we do that
            subprocess.check_output(["git", "update-index", "--refresh"])

            # get info about the latest tag in git
            describe_out = subprocess.check_output([
                "git",
                "describe",
                "--dirty",
                "--tags",
                "--long",
                "--abbrev=40",
                "--match=v*",
            ], stderr=subprocess.STDOUT
            ).decode().split("-")
        except subprocess.CalledProcessError:
            # logger.warn("Error when running git describe")
            return {}

        info = {}

        if describe_out[-1].strip() == "dirty":
            info["dirty"] = True
            describe_out.pop()

        info["commit_sha"] = describe_out.pop().lstrip("g")
        info["distance_to_latest_tag"] = int(describe_out.pop())
        info["current_version"] = "-".join(describe_out).lstrip("v")

        return info

    @classmethod
    def add_path(cls, path):
        subprocess.check_output(["git", "add", "--update", path])

    @classmethod
    def tag(cls, name):
        subprocess.check_output(["git", "tag", name])


class Mercurial(BaseVCS):
    _TEST_USABLE_COMMAND = ["hg", "root"]
    _COMMIT_COMMAND = ["hg", "commit", "--logfile"]

    @classmethod
    def latest_tag_info(cls):
        return {}

    @classmethod
    def assert_nondirty(cls):
        lines = [
            line.strip() for line in
            subprocess.check_output(
                ["hg", "status", "-mard"]).splitlines()
            if not line.strip().startswith(b"??")
        ]

        if lines:
            raise WorkingDirectoryIsDirtyException(
                "Mercurial working directory is not clean:\n{}".format(
                    b"\n".join(lines)))

    @classmethod
    def add_path(cls, path):
        pass

    @classmethod
    def tag(cls, name):
        subprocess.check_output(["hg", "tag", name])


VCS = [Git, Mercurial]
