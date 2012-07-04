# Copyright (c) 2011 Godefroid Chapelle
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

def output(arg):
    print("MANUAL: arg=%s" % arg)


def main():
    for abc in range(10):
        import ipdb; ipdb.set_trace()
        output(abc)


# code to test with nose
import unittest


class IpdbUsageTests(unittest.TestCase):

    def testMain(self):
        main()

if __name__ == "__main__":
    main()
