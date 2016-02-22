# Copyright (c) 2011-2015 Godefroid Chapelle
# 
# This file is part of ipdb.
# Redistributable under the MIT License
# https://opensource.org/licenses/MIT

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
