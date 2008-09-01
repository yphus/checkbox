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
from gettext import gettext as _

from checkbox.plugin import Plugin
from checkbox.iterator import PREV


class ReportPrompt(Plugin):

    def register(self, manager):
        super(ReportPrompt, self).register(manager)
        self._manager.reactor.call_on("prompt-report", self.prompt_report)

    def prompt_report(self, interface):
        if interface.direction != PREV:
            interface.show_wait(_("Building report..."),
                self._manager.reactor.fire, "report")


factory = ReportPrompt
