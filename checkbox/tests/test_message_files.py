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
import os
import unittest
from checkbox.lib.path import path_expand_recursive
from checkbox.lib.template_i18n import TemplateI18n


class MessageFileFormatTest(unittest.TestCase):

    def read_jobs(self):
        messages = []
        if os.environ.get("CHECKBOX_PACKAGING", 0):
            jobs_path = "./build/share/checkbox/jobs"
        else:
            jobs_path = "./jobs"

        for filename in path_expand_recursive(jobs_path):
            basename = os.path.basename(filename)
            if not basename.startswith(".") and not basename.endswith("~"):
                template = TemplateI18n()
                messages += template.load_filename(filename)

        return messages

    def setUp(self):
        self.messages = self.read_jobs()

    def test_job_files_valid(self):
        self.assertTrue(self.messages)
        self.assertTrue(len(self.messages) > 0)

    def test_all_messages_have_name(self):
        for message in self.messages:
            self.assertIn("name", message)

    def test_all_messages_have_command_or_description(self):
        for message in self.messages:
            self.assertTrue("command" in message or "description" in message)

    def test_shell_jobs_have_description(self):
        for message in self.messages:
            if message['plugin'] == 'shell':
                self.assertTrue("description" in message, message['name'])

    def test_shell_jobs_with_root_have_needed_environ(self):
        import re
        shell_variables_regex = r'\$\{?([A-Z_]+)\}?'
        environ_variables_regex = r'([A-Z_]+)'
        for message in self.messages:
            if 'command' in message and 'user' in message:
                shell_variables = []
                environ_variables = []
                for key in ['command', 'command_extended']:
                    if key in message:
                        shell_variables += re.findall(shell_variables_regex,
                                                      message[key])
                if 'environ' in message:
                    environ_variables = re.findall(environ_variables_regex, 
                                                   message['environ'])
                self.assertEquals(set(environ_variables),
                                  set(shell_variables),
                                  message['name'])

    def test_jobs_comply_with_schema(self):
        globals = {}
        exec(open("plugins/jobs_info.py").read(), globals)
        job_schema = globals["job_schema"]
        for message in self.messages:
            long_ext = "_extended"
            for long_key in list(message.keys()):
                if long_key.endswith(long_ext):
                    short_key = long_key.replace(long_ext, "")
                    message[short_key] = message.pop(long_key)
            job_schema.coerce(message)

    def test_verify_interact_jobs_have_command(self):
        for message in self.messages:
            if message['plugin'] in ('user-verify', 'user-interact'):
                self.assertTrue("command" in message)
