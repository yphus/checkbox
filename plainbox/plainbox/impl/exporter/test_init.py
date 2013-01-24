# This file is part of Checkbox.
#
# Copyright 2012 Canonical Ltd.
# Written by:
#   Zygmunt Krynicki <zygmunt.krynicki@canonical.com>
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

"""
plainbox.impl.exporter.test_init
================================

Test definitions for plainbox.impl.exporter module
"""

from unittest import TestCase

from plainbox.impl.exporter import SessionStateExporterBase
from plainbox.impl.exporter import classproperty
from plainbox.impl.session import SessionState
from plainbox.impl.job import JobDefinition
from plainbox.impl.result import JobResult, IOLogRecord
from plainbox.impl.testing_utils import make_job, make_job_result


class ClassPropertyTests(TestCase):

    def get_C(self):

        class C:
            attr = "data"

            @classproperty
            def prop(cls):
                return cls.attr

        return C

    def test_classproperty_on_cls(self):
        cls = self.get_C()
        self.assertEqual(cls.prop, cls.attr)

    def test_classproperty_on_obj(self):
        cls = self.get_C()
        obj = cls()
        self.assertEqual(obj.prop, obj.attr)


class SessionStateExporterBaseTests(TestCase):

    class TestSessionStateExporter(SessionStateExporterBase):

        def dump(self, data, stream):
            """
            Dummy implementation of a method required by the base class.
            """

    def make_test_session(self):
        # Create a small session with two jobs and two results
        job_a = make_job('job_a')
        job_b = make_job('job_b')
        session = SessionState([job_a, job_b])
        session.update_job_state_map()
        session.update_desired_job_list([job_a, job_b])
        result_a = make_job_result(job_a, 'pass')
        result_b = make_job_result(job_b, 'fail')
        session.update_job_result(job_a, result_a)
        session.update_job_result(job_b, result_b)
        return session

    def test_defaults(self):
        # Test all defaults, with all options unset
        exporter = self.TestSessionStateExporter()
        session = self.make_test_session()
        data = exporter.get_session_data_subset(session)
        expected_data = {
            'result_map': {
                'job_a': {
                    'outcome': 'pass'
                },
                'job_b': {
                    'outcome': 'fail'
                }
            }
        }
        self.assertEqual(data, expected_data)

    def make_realistic_test_session(self):
        # Create a more realistic session with two jobs but with richer set
        # of data in the actual jobs and results.
        job_a = JobDefinition({
            'plugin': 'shell',
            'name': 'job_a',
            'command': 'echo testing && true',
            'requires': 'job_b.ready == "yes"'
        })
        job_b = JobDefinition({
            'plugin': 'resource',
            'name': 'job_b',
            'command': 'echo ready: yes'
        })
        session = SessionState([job_a, job_b])
        session.update_job_state_map()
        session.update_desired_job_list([job_a, job_b])
        result_a = JobResult({
            'job': job_a,
            'outcome': 'pass',
            'return_code': 0,
            'io_log': (
                IOLogRecord(0, 'stdout', 'testing\n'),
            )
        })
        result_b = JobResult({
            'job': job_b,
            'outcome': 'pass',
            'return_code': 0,
            'io_log': (
                IOLogRecord(0, 'stdout', 'ready: yes\n'),
            )
        })
        session.update_job_result(job_a, result_a)
        session.update_job_result(job_b, result_b)
        return session

    def test_all_at_once(self):
        # Test every option set, all at once
        # Currently this sets both OPTION_WITH_IO_LOG and
        # one of the two mutually exclusive options:
        #   - OPTION_SQUASH_IO_LOG
        #   - OPTION_FLATTEN_IO_LOG
        # The implementation favours SQUASH_IO_LOG
        # and thus the code below tests that option
        exporter = self.TestSessionStateExporter(
            self.TestSessionStateExporter.supported_option_list)
        session = self.make_realistic_test_session()
        data = exporter.get_session_data_subset(session)
        expected_data = {
            'job_list': ['job_a', 'job_b'],
            'run_list': ['job_b', 'job_a'],
            'desired_job_list': ['job_a', 'job_b'],
            'resource_map': {
                'job_b': [{
                    'ready': 'yes'
                }]
            },
            'result_map': {
                'job_a': {
                    'outcome': 'pass',
                    'plugin': 'shell',
                    'command': 'echo testing && true',
                    'io_log': ['testing'],
                    'requires': 'job_b.ready == "yes"'
                },
                'job_b': {
                    'outcome': 'pass',
                    'plugin': 'resource',
                    'command': 'echo ready: yes',
                    'io_log': ['ready: yes'],
                }
            }
        }
        # This is just to make debugging easier
        self.assertEqual(expected_data.keys(), data.keys())
        for key in data.keys():
            self.assertEqual(expected_data[key], data[key],
                             msg="wrong data in %r" % key)
        # This is to make sure we didn't miss anything by being too smart
        self.assertEqual(data, expected_data)

    def test_io_log_processors(self):
        # Test all of the io_log processors that are built into
        # the base SessionStateExporter class
        cls = self.TestSessionStateExporter
        io_log = (
            IOLogRecord(0, 'stdout', 'foo\n'),
            IOLogRecord(1, 'stderr', 'bar\n'),
            IOLogRecord(2, 'stdout', 'quxx\n')
        )
        self.assertEqual(
            cls._squash_io_log(io_log), ['foo', 'bar', 'quxx'])
        self.assertEqual(
            cls._flatten_io_log(io_log), 'foo\nbar\nquxx\n')
        self.assertEqual(
            cls._io_log(io_log), [
                (0, 'stdout', 'foo'),
                (1, 'stderr', 'bar'),
                (2, 'stdout', 'quxx')])
