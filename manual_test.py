def output(arg):
    print "MANUAL: arg=", arg


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
