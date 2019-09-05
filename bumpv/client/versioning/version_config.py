import re
import sre_constants
from string import Formatter

from ..exceptions import (
    IncompleteVersionRepresenationException,
    MissingValueForSerializationException,
)
from ..versioning import VersionPart


class VersionConfig(object):

    """
    Holds a complete representation of a version string
    """

    def __init__(self, parse, serialize, search, replace, part_configs=None):

        try:
            self.parse_regex = re.compile(parse, re.VERBOSE)
        except sre_constants.error as e:
            logger.error("--parse '{}' is not a valid regex".format(parse))
            raise e

        self.serialize_formats = serialize

        if not part_configs:
            part_configs = {}

        self.part_configs = part_configs
        self.search = search
        self.replace = replace

    @staticmethod
    def _labels_for_format(serialize_format):
        return (
            label
            for _, label, _, _ in Formatter().parse(serialize_format)
            if label
        )

    def order(self):
        # currently, order depends on the first given serialization format
        # this seems like a good idea because this should be the most complete format
        return self._labels_for_format(self.serialize_formats[0])

    def parse(self, version_string):

        regexp_one_line = "".join([l.split("#")[0].strip() for l in self.parse_regex.pattern.splitlines()])

        logger.info("Parsing version '{}' using regexp '{}'".format(version_string, regexp_one_line))

        match = self.parse_regex.search(version_string)

        _parsed = {}
        if not match:
            logger.warn("Evaluating 'parse' option: '{}' does not parse current version '{}'".format(
                self.parse_regex.pattern, version_string))
            return

        for key, value in match.groupdict().items():
            _parsed[key] = VersionPart(value, self.part_configs.get(key))

        v = Version(_parsed, version_string)

        logger.info("Parsed the following values: %s" % kv_string(v._values))

        return v

    def _serialize(self, version, serialize_format, context, raise_if_incomplete=False):
        """
        Attempts to serialize a version with the given serialization format.

        Raises MissingValueForSerializationException if not serializable
        """
        values = context.copy()
        for k in version:
            values[k] = version[k]

        # TODO dump complete context on debug level

        try:
            # test whether all parts required in the format have values
            serialized = serialize_format.format(**values)

        except KeyError as e:
            missing_key = getattr(
                e,
                'message',  # Python 2
                e.args[0]  # Python 3
            )
            raise MissingValueForSerializationException(
                "Did not find key {} in {} when serializing version number".format(
                    repr(missing_key), repr(version)))

        keys_needing_representation = set()
        found_required = False

        for k in self.order():
            v = values[k]

            if not isinstance(v, VersionPart):
                # values coming from environment variables don't need
                # representation
                continue

            if not v.is_optional():
                found_required = True
                keys_needing_representation.add(k)
            elif not found_required:
                keys_needing_representation.add(k)

        required_by_format = set(self._labels_for_format(serialize_format))

        # try whether all parsed keys are represented
        if raise_if_incomplete:
            if not (keys_needing_representation <= required_by_format):
                raise IncompleteVersionRepresenationException(
                    "Could not represent '{}' in format '{}'".format(
                        "', '".join(keys_needing_representation ^ required_by_format),
                        serialize_format,
                    ))

        return serialized

    def _choose_serialize_format(self, version, context):

        chosen = None

        # logger.info("Available serialization formats: '{}'".format("', '".join(self.serialize_formats)))

        for serialize_format in self.serialize_formats:
            try:
                self._serialize(version, serialize_format, context, raise_if_incomplete=True)
                chosen = serialize_format
                # logger.info("Found '{}' to be a usable serialization format".format(chosen))
            except IncompleteVersionRepresenationException:
                # logger.info(e.message)
                if not chosen:
                    chosen = serialize_format
            except MissingValueForSerializationException as e:
                logger.info(e.message)
                raise e

        if not chosen:
            raise KeyError("Did not find suitable serialization format")

        # logger.info("Selected serialization format '{}'".format(chosen))

        return chosen

    def serialize(self, version, context):
        serialized = self._serialize(version, self._choose_serialize_format(version, context), context)
        # logger.info("Serialized to '{}'".format(serialized))
        return serialized
