#
# This file is part of Checkbox.
#
# Copyright 2012 Canonical Ltd.
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
from io import StringIO

from unittest import TestCase

from checkbox.parsers.cputable import CputableParser


class CputableResult:

    def __init__(self):
        self.cpus = []

    def addCpu(self, cpu):
        self.cpus.append(cpu)

    def getByDebianName(self, name):
        for cpu in self.cpus:
            if cpu["debian_name"] == name:
                return cpu

        return None

    def getByGnuName(self, name):
        for cpu in self.cpus:
            if cpu["gnu_name"] == name:
                return cpu

        return None


class TestCputableParser(TestCase):

    def getParser(self, string):
        stream = StringIO(string)
        return CputableParser(stream)

    def getResult(self, string):
        parser = self.getParser(string)
        result = CputableResult()
        parser.run(result)
        return result

    def test_empty(self):
        result = self.getResult("")
        self.assertEquals(result.cpus, [])

    def test_i386(self):
        result = self.getResult("""
# <Debian name>	<GNU name>	<config.guess regex>	<Bits>	<Endianness>
i386		i686		(i[3456]86|pentium)	32	little
""")
        debian_cpu = result.getByDebianName("i386")
        self.assertNotEquals(debian_cpu, None)
        gnu_cpu = result.getByGnuName("i686")
        self.assertNotEquals(gnu_cpu, None)
        self.assertEquals(debian_cpu, gnu_cpu)
