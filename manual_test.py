# Copyright (c) 2011-2016 Godefroid Chapelle and ipdb development team
#
# This file is part of ipdb.
# Redistributable under the revised BSD license
# https://opensource.org/licenses/BSD-3-Clause


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
