# Copyright (c) 2012 Marc Abramowitz
#
# This file is part of ipdb.
# GNU package is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# GNU package is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.

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
