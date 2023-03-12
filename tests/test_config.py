# Copyright (c) 2012-2016 Marc Abramowitz and ipdb development team
#
# This file is part of ipdb.
# Redistributable under the revised BSD license
# https://opensource.org/licenses/BSD-3-Clause

try:
    import configparser
except:
    import ConfigParser as configparser
import unittest
import os
import tempfile
import shutil

from ipdb.__main__ import (
    get_config,
    get_context_from_config,
)


class ModifiedEnvironment(object):
    """
    I am a context manager that sets up environment variables for a test case.
    """

    def __init__(self, **kwargs):
        self.prev = {}
        self.excur = kwargs
        for k in kwargs:
            self.prev[k] = os.getenv(k)

    def __enter__(self):
        self.update_environment(self.excur)

    def __exit__(self, type, value, traceback):
        self.update_environment(self.prev)

    def update_environment(self, d):
        for k in d:
            if d[k] is None:
                if k in os.environ:
                    del os.environ[k]
            else:
                os.environ[k] = d[k]


def write_lines_to_file(path, lines):
    """
    Write `lines` to file at `path`.

    :param path: Filesystem path to write.
    :param lines: Sequence of text lines, without line endings.
    :return: None.
    """
    f = open(path, "w")
    f.writelines([x + "\n" for x in lines])
    f.close()


def set_config_files_fixture(testcase):
    """
    Set a data fixture of configuration files for `testcase`.
    """
    testcase.tmpd = tempfile.mkdtemp()
    testcase.addCleanup(shutil.rmtree, testcase.tmpd)
    # Set CWD to known empty directory so we don't pick up some other .ipdb
    # file from the CWD tests are actually run from.
    save_cwd = os.getcwd()
    testcase.addCleanup(os.chdir, save_cwd)
    cwd_dir = os.path.join(testcase.tmpd, "cwd")
    os.mkdir(cwd_dir)
    os.chdir(cwd_dir)
    # This represents the $HOME config file, and doubles for the current
    # working directory config file if we set CWD to testcase.tmpd
    testcase.default_filename = os.path.join(testcase.tmpd, ".ipdb")
    testcase.default_context = 10
    write_lines_to_file(
        testcase.default_filename,
        [
            "# this is a test config file for ipdb",
            "context = {}".format(str(testcase.default_context)),
        ],
    )
    testcase.env_filename = os.path.join(testcase.tmpd, "ipdb.env")
    testcase.env_context = 20
    write_lines_to_file(
        testcase.env_filename,
        [
            "# this is a test config file for ipdb",
            "context = {}".format(str(testcase.env_context)),
        ],
    )
    testcase.setup_filename = os.path.join(cwd_dir, "setup.cfg")
    testcase.setup_context = 25
    write_lines_to_file(
        testcase.setup_filename,
        [
            "[ipdb]",
            "context = {}".format(str(testcase.setup_context)),
        ],
    )
    testcase.pyproject_filename = os.path.join(cwd_dir, "pyproject.toml")
    testcase.pyproject_context = 30
    write_lines_to_file(
        testcase.pyproject_filename,
        [
            "[tool.ipdb]",
            "context = {}".format(str(testcase.pyproject_context)),
        ],
    )


class ConfigTest(unittest.TestCase):
    """
    All variations of config file parsing works as expected.
    """

    def setUp(self):
        """
        Set fixtures for this test case.
        """
        set_config_files_fixture(self)

    def test_noenv_nodef_nosetup_pyproject(self):
        """
        Setup: $IPDB_CONFIG unset, $HOME/.ipdb does not exist,
            setup.cfg does not exist, pyproject.toml exists
        Result: load pyproject.toml
        """
        os.unlink(self.env_filename)
        os.unlink(self.default_filename)
        os.remove(self.setup_filename)
        with ModifiedEnvironment(IPDB_CONFIG=None, HOME=self.tmpd):
            cfg = get_config()
            self.assertEqual(["ipdb"], cfg.sections())
            self.assertEqual(self.pyproject_context, cfg.getint("ipdb", "context"))
            self.assertRaises(configparser.NoOptionError, cfg.get, "ipdb", "version")

    def test_env_nodef_setup_pyproject(self):
        """
        Setup: $IPDB_CONFIG is set, $HOME/.ipdb does not exist,
            setup.cfg exists, pyproject.toml exists
        Result: load $IPDB_CONFIG
        """
        os.unlink(self.default_filename)
        with ModifiedEnvironment(IPDB_CONFIG=self.env_filename, HOME=self.tmpd):
            cfg = get_config()
            self.assertEqual(["ipdb"], cfg.sections())
            self.assertEqual(self.env_context, cfg.getint("ipdb", "context"))
            self.assertRaises(configparser.NoOptionError, cfg.get, "ipdb", "version")

    def test_env_def_setup_pyproject(self):
        """
        Setup: $IPDB_CONFIG is set, $HOME/.ipdb exists,
            setup.cfg exists, pyproject.toml exists
        Result: load $IPDB_CONFIG
        """
        with ModifiedEnvironment(IPDB_CONFIG=self.env_filename, HOME=self.tmpd):
            cfg = get_config()
            self.assertEqual(["ipdb"], cfg.sections())
            self.assertEqual(self.env_context, cfg.getint("ipdb", "context"))
            self.assertRaises(configparser.NoOptionError, cfg.get, "ipdb", "version")

    def test_noenv_nodef_setup_pyproject(self):
        """
        Setup: $IPDB_CONFIG unset, $HOME/.ipdb does not exist,
            setup.cfg exists, pyproject.toml exists
        Result: load pyproject.toml
        """
        os.unlink(self.env_filename)
        os.unlink(self.default_filename)
        with ModifiedEnvironment(IPDB_CONFIG=None, HOME=self.tmpd):
            cfg = get_config()
            self.assertEqual(["ipdb"], cfg.sections())
            self.assertEqual(self.pyproject_context, cfg.getint("ipdb", "context"))
            self.assertRaises(configparser.NoOptionError, cfg.get, "ipdb", "version")

    def test_noenv_def_setup_pyproject(self):
        """
        Setup: $IPDB_CONFIG unset, $HOME/.ipdb exists,
            setup.cfg exists, pyproject.toml exists
        Result: load .ipdb
        """
        os.unlink(self.env_filename)
        with ModifiedEnvironment(IPDB_CONFIG=None, HOME=self.tmpd):
            cfg = get_config()
            self.assertEqual(["ipdb"], cfg.sections())
            self.assertEqual(self.default_context, cfg.getint("ipdb", "context"))
            self.assertRaises(configparser.NoOptionError, cfg.get, "ipdb", "version")

    def test_env_nodef_nosetup(self):
        """
        Setup: $IPDB_CONFIG is set, $HOME/.ipdb does not exist,
            setup.cfg does not exist, pyproject.toml does not exist
        Result: load $IPDB_CONFIG
        """
        os.unlink(self.default_filename)
        os.unlink(self.pyproject_filename)
        os.remove(self.setup_filename)
        with ModifiedEnvironment(IPDB_CONFIG=self.env_filename, HOME=self.tmpd):
            cfg = get_config()
            self.assertEqual(["ipdb"], cfg.sections())
            self.assertEqual(self.env_context, cfg.getint("ipdb", "context"))
            self.assertRaises(
                configparser.NoOptionError, cfg.getboolean, "ipdb", "version"
            )

    def test_noenv_def_nosetup(self):
        """
        Setup: $IPDB_CONFIG unset, $HOME/.ipdb exists,
            setup.cfg does not exist, pyproject.toml does not exist
        Result: load $HOME/.ipdb
        """
        os.unlink(self.env_filename)
        os.unlink(self.pyproject_filename)
        os.remove(self.setup_filename)
        with ModifiedEnvironment(IPDB_CONFIG=None, HOME=self.tmpd):
            cfg = get_config()
            self.assertEqual(["ipdb"], cfg.sections())
            self.assertEqual(self.default_context, cfg.getint("ipdb", "context"))
            self.assertRaises(configparser.NoOptionError, cfg.get, "ipdb", "version")

    def test_noenv_nodef_nosetup(self):
        """
        Setup: $IPDB_CONFIG unset, $HOME/.ipdb does not
            exist, setup.cfg does not exist, pyproject.toml does not exist
        Result: load nothing
        """
        os.unlink(self.env_filename)
        os.unlink(self.default_filename)
        os.unlink(self.pyproject_filename)
        os.remove(self.setup_filename)
        with ModifiedEnvironment(IPDB_CONFIG=None, HOME=self.tmpd):
            cfg = get_config()
            self.assertEqual([], cfg.sections())

    def test_env_cwd(self):
        """
        Setup: $IPDB_CONFIG is set, .ipdb in local dir,
            setup.cfg does not exist, pyproject.toml does not exist
        Result: load .ipdb
        """
        os.chdir(self.tmpd)  # setUp is already set to restore us to our pre-testing cwd
        os.unlink(self.pyproject_filename)
        os.remove(self.setup_filename)
        with ModifiedEnvironment(IPDB_CONFIG=self.env_filename, HOME=self.tmpd):
            cfg = get_config()
            self.assertEqual(["ipdb"], cfg.sections())
            self.assertEqual(self.env_context, cfg.getint("ipdb", "context"))
            self.assertRaises(configparser.NoOptionError, cfg.get, "ipdb", "version")

    def test_env_def_nosetup(self):
        """
        Setup: $IPDB_CONFIG is set, $HOME/.ipdb exists,
            setup.cfg does not exist, pyproject.toml does not exist
        Result: load $IPDB_CONFIG
        """
        os.unlink(self.pyproject_filename)
        os.remove(self.setup_filename)
        with ModifiedEnvironment(IPDB_CONFIG=self.env_filename, HOME=self.tmpd):
            cfg = get_config()
            self.assertEqual(["ipdb"], cfg.sections())
            self.assertEqual(self.env_context, cfg.getint("ipdb", "context"))
            self.assertRaises(configparser.NoOptionError, cfg.get, "ipdb", "version")

    def test_noenv_def_setup(self):
        """
        Setup: $IPDB_CONFIG unset, $HOME/.ipdb exists,
            setup.cfg exists, pyproject.toml does not exist
        Result: load $HOME/.ipdb
        """
        os.unlink(self.env_filename)
        os.unlink(self.pyproject_filename)
        with ModifiedEnvironment(IPDB_CONFIG=None, HOME=self.tmpd):
            cfg = get_config()
            self.assertEqual(["ipdb"], cfg.sections())
            self.assertEqual(self.default_context, cfg.getint("ipdb", "context"))
            self.assertRaises(
                configparser.NoOptionError, cfg.getboolean, "ipdb", "version"
            )

    def test_noenv_nodef_setup(self):
        """
        Setup: $IPDB_CONFIG unset, $HOME/.ipdb does not exist,
            setup.cfg exists, pyproject.toml does not exist
        Result: load setup
        """
        os.unlink(self.env_filename)
        os.unlink(self.default_filename)
        os.unlink(self.pyproject_filename)
        with ModifiedEnvironment(IPDB_CONFIG=None, HOME=self.tmpd):
            cfg = get_config()
            self.assertEqual(["ipdb"], cfg.sections())
            self.assertEqual(self.setup_context, cfg.getint("ipdb", "context"))
            self.assertRaises(configparser.NoOptionError, cfg.get, "ipdb", "version")

    def test_env_def_setup(self):
        """
        Setup: $IPDB_CONFIG is set, $HOME/.ipdb exists,
            setup.cfg exists, pyproject.toml does not exist
        Result: load $IPDB_CONFIG
        """
        os.unlink(self.pyproject_filename)
        with ModifiedEnvironment(IPDB_CONFIG=self.env_filename, HOME=self.tmpd):
            cfg = get_config()
            self.assertEqual(["ipdb"], cfg.sections())
            self.assertEqual(self.env_context, cfg.getint("ipdb", "context"))
            self.assertRaises(configparser.NoOptionError, cfg.get, "ipdb", "version")

    def test_env_nodef_setup(self):
        """
        Setup: $IPDB_CONFIG is set, $HOME/.ipdb does not
            exist, setup.cfg exists, pyproject.toml does not exist
        Result: load $IPDB_CONFIG
        """
        os.unlink(self.default_filename)
        os.unlink(self.pyproject_filename)
        with ModifiedEnvironment(IPDB_CONFIG=self.env_filename, HOME=self.tmpd):
            cfg = get_config()
            self.assertEqual(["ipdb"], cfg.sections())
            self.assertEqual(self.env_context, cfg.getint("ipdb", "context"))
            self.assertRaises(
                configparser.NoOptionError, cfg.getboolean, "ipdb", "version"
            )

    def test_noenv_def_setup(self):
        """
        Setup: $IPDB_CONFIG unset, $HOME/.ipdb exists,
            setup.cfg exists, pyproject.toml does not exist
        Result: load $HOME/.ipdb
        """
        os.unlink(self.env_filename)
        os.unlink(self.pyproject_filename)
        with ModifiedEnvironment(IPDB_CONFIG=None, HOME=self.tmpd):
            cfg = get_config()
            self.assertEqual(["ipdb"], cfg.sections())
            self.assertEqual(self.default_context, cfg.getint("ipdb", "context"))
            self.assertRaises(configparser.NoOptionError, cfg.get, "ipdb", "version")


class get_context_from_config_TestCase(unittest.TestCase):
    """
    Test cases for function `get_context_from_config`.
    """

    def setUp(self):
        """
        Set fixtures for this test case.
        """
        set_config_files_fixture(self)

    def test_noenv_nodef_invalid_setup(self):
        """
        Setup: $IPDB_CONFIG unset, $HOME/.ipdb does not exist,
            setup.cfg does not exist, pyproject.toml content is invalid.
        Result: Propagate exception from `get_config`.
        """
        os.unlink(self.env_filename)
        os.unlink(self.default_filename)
        os.unlink(self.setup_filename)
        write_lines_to_file(
            self.pyproject_filename,
            [
                "[ipdb]",
                "spam = abc",
            ],
        )

        try:
            from tomllib import TOMLDecodeError
        except ImportError:
            try:
                from tomli import TOMLDecodeError
            except ImportError:
                from toml.decoder import TomlDecodeError as TOMLDecodeError

        with ModifiedEnvironment(IPDB_CONFIG=None, HOME=self.tmpd):
            try:
                get_context_from_config()
            except TOMLDecodeError:
                pass
            else:
                self.fail("Expected TomlDecodeError from invalid config file")
