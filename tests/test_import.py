# Copyright (c) 2012-2016 Marc Abramowitz and ipdb development team
#
# This file is part of ipdb.
# Redistributable under the revised BSD license
# https://opensource.org/licenses/BSD-3-Clause

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
