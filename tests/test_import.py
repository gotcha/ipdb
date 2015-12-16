# Copyright (c) 2012 Marc Abramowitz
#
# This file is part of ipdb.
# Redistributable under the MIT License
# https://opensource.org/licenses/MIT

import unittest


class ImportTest(unittest.TestCase):

    def test_import(self):
        from ipdb import set_trace, post_mortem, pm, run, runcall, runeval
        set_trace  # please pyflakes
        post_mortem  # please pyflakes
        pm  # please pyflakes
        run  # please pyflakes
        runcall  # please pyflakes
        runeval  # please pyflakes
