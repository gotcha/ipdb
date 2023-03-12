# Copyright (c) 2012-2016 Marc Abramowitz and ipdb development team
#
# This file is part of ipdb.
# Redistributable under the revised BSD license
# https://opensource.org/licenses/BSD-3-Clause

import sys
import unittest
import os

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from getopt import GetoptError
from ipdb.__main__ import main


@patch("ipdb.__main__._get_debugger_cls")
class OptsTest(unittest.TestCase):
    def set_argv(self, *argv):
        argv_patch = patch("ipdb.__main__.sys.argv", argv)
        argv_patch.start()
        self.addCleanup(argv_patch.stop)

    @unittest.skipIf(
        sys.version_info[0] == 3 and sys.version_info[1] >= 11,
        ">3.11 requires different test",
    )
    @patch("ipdb.__main__.sys.version_info", (3, 7))
    def test_debug_module_script(self, get_debugger_cls):
        module_name = "my_buggy_module"
        self.set_argv("ipdb", "-m", module_name)

        main()

        debugger = get_debugger_cls.return_value.return_value
        debugger._runmodule.assert_called_once_with(module_name)

    @unittest.skipIf(
        sys.version_info[0] == 3 and sys.version_info[1] >= 11,
        ">3.11 requires different test",
    )
    @patch("ipdb.__main__.os.path.exists")
    def test_debug_script(self, exists, get_debugger_cls):
        script_name = "my_buggy_script"
        self.set_argv("ipdb", script_name)

        main()

        debugger = get_debugger_cls.return_value.return_value
        debugger._runscript.assert_called_once_with(script_name)

    @unittest.skipIf(
        sys.version_info[0] != 3 or sys.version_info[1] < 11,
        "<3.11 requires different test",
    )
    def test_debug_module_script_3_11(self, get_debugger_cls):
        module_name = "my_buggy_module_3_11"
        self.set_argv("ipdb", "-m", module_name)

        main()

        debugger = get_debugger_cls.return_value.return_value
        debugger._run.assert_called_once_with(module_name)

    @unittest.skipIf(
        sys.version_info[0] != 3 or sys.version_info[1] < 11,
        "<3.11 requires different test",
    )
    @patch("ipdb.__main__.os.path.exists")
    def test_debug_script_3_11(self, exists, get_debugger_cls):
        script_name = "my_buggy_script_3_11"
        self.set_argv("ipdb", script_name)

        main()

        debugger = get_debugger_cls.return_value.return_value
        debugger._run.assert_called_once_with(os.path.join(os.getcwd(), script_name))

    def test_option_m_fallback_on_py36(self, get_debugger_cls):
        self.set_argv("ipdb", "-m", "my.module")
        with patch("ipdb.__main__.sys.version_info", (3, 6)):
            with self.assertRaises(GetoptError):
                main()

        with patch("ipdb.__main__.sys.version_info", (3, 7)):
            self.set_argv("ipdb", "-m", "my.module")
            try:
                main()
            except GetoptError:
                self.fail("GetoptError raised unexpectedly.")
