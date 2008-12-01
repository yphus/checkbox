#
# Copyright (c) 2008 Canonical
#
# Written by Marc Tardif <marc@interunion.ca>
#
# This file is part of Checkbox.
#
# Checkbox is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Checkbox is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Checkbox.  If not, see <http://www.gnu.org/licenses/>.
#
import os
import re

from checkbox.lib.cache import cache
from checkbox.lib.conversion import string_to_type

from checkbox.registries.command import CommandRegistry
from checkbox.registries.data import DataRegistry
from checkbox.registries.directory import DirectoryRegistry


class SourceRegistry(DataRegistry):

    def items(self):
        items = []
        lines = []

        id = depth = None
        for line in self.split("\n"):
            if not line:
                continue

            match = re.match(r"(\s+(\/)?)(.+)", line)
            if not match:
                lines[-1] += line
                continue

            space = len(match.group(1).rstrip("/"))
            if depth is None:
                depth = space

            if space > depth:
                lines.append(line)
            elif match.group(2) is not None:
                if id is not None:
                    value = SourceRegistry(None, "\n".join(lines))
                    lines = []

                    items.append((id, value))

                id = match.group(3).split("/")[-1].rstrip(":")
            else:
                (key, value) = match.group(3).split(" = ", 1)
                if value == "(no value set)":
                    value = None
                else:
                    match = re.match(r"\[([^\]]*)\]", value)
                    if match:
                        list_string = match.group(1)
                        if len(list_string):
                            value = list_string.split(",")
                        else:
                            value = []
                    else:
                        value = string_to_type(value)

                items.append((key, value))

        if lines:
            value = SourceRegistry(None, "\n".join(lines))
            items.append((id, value))

        return items


class UserRegistry(CommandRegistry):

    def __init__(self, config, command, user):
        super(UserRegistry, self).__init__(config, command)
        self._command_template = command
        self._user = user

    def __str__(self):
        self._command = self._command_template.replace("$user", self._user)
        return super(UserRegistry, self).__str__()

    def items(self):
        items = []

        key = None
        lines = []
        for line in self.split("\n"):
            if line.startswith(" /"):
                if lines:
                    value = SourceRegistry(None, "\n".join(lines))
                    items.append((key, value))
                key = line.strip().lstrip("/").rstrip(":")
            else:
                lines.append(line)

        if lines:
            value = SourceRegistry(None, "\n".join(lines))
            items.append((key, value))

        return items


class GconfRegistry(DirectoryRegistry):
    """Registry for gconf information.

    Each item contained in this registry consists of the udi as key and
    the corresponding device registry as value.
    """

    required_attributes = ["command", "source"]

    @cache
    def __str__(self):
        users = []
        for user in os.listdir(self._directory):
            if user == "." or user == "..":
                continue

            source = self._config.source.replace("$user", user)
            if not os.path.isdir(source):
                continue

            users.append(user)

        return "\n".join(users)

    @cache
    def items(self):
        items = []
        for user in self.split("\n"):
            value = UserRegistry(self._config, self._config.command, user)
            items.append((user, value))

        return items


factory = GconfRegistry
