import os
import re

from ConfigParser import ConfigParser


class IncludeDict(dict):

    def __init__(self, parser):
        super(IncludeDict, self).__init__()
        self._parser = parser

        for (key, value) in os.environ.items():
            super(IncludeDict, self).__setitem__(key.lower(), value)

    def __setitem__(self, key, value):
        if key == "includes":
            for path in re.split(r"\s+", value):
                path = self._parser._interpolate("DEFAULT", None, path, self)
                if not os.path.exists(path):
                    raise Exception, "No such configuration file: %s" % path
                self._parser.read(path)

        # Environment has precedence over configuration
        elif key.upper() not in os.environ.keys():
            super(IncludeDict, self).__setitem__(key, value)


class ConfigSection(object):

    def __init__(self, parent, name, attributes={}):
        self.parent = parent
        self.name = name
        self.attributes = attributes

    def _get_value(self, name):
        return self.attributes.get(name)

    def __getattr__(self, name):
        if name in self.attributes:
            return self._get_value(name)

        raise AttributeError, name


class ConfigDefaults(ConfigSection):

    def _get_value(self, name):
        return os.environ.get(name.upper()) \
            or os.environ.get(name.lower()) \
            or super(ConfigDefaults, self)._get_value(name)

    def __getattr__(self, name):
        if name in self.attributes:
            return self._get_value(name)

        raise AttributeError, name


class Config(object):

    def __init__(self, path):
        self.path = path
        self.sections = {}

        self._parser = ConfigParser()
        self._parser._defaults = IncludeDict(self._parser)

        if not os.path.exists(path):
            raise Exception, "No such configuration file: %s" % path
        self._parser.read(path)

    def get_defaults(self):
        attributes = self._parser.defaults()
        return ConfigDefaults(self, 'DEFAULT', attributes)

    def get_section(self, section_name):
        if section_name in self._parser.sections():
            attributes = dict(self._parser.items(section_name))
            return ConfigSection(self, section_name, attributes)

        return None

    def get_section_names(self):
        return self._parser.sections()
