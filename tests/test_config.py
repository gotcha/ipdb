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
from ipdb.__main__ import get_config


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


class ConfigTest(unittest.TestCase):
    """
    All variations of config file parsing works as expected.
    """

    def _write_file(self, path, lines):
        f = open(path, "w")
        f.writelines([x + "\n" for x in lines])
        f.close()

    def setUp(self):
        """
        Create all temporary config files for testing
        """
        self.tmpd = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmpd)
        # Set CWD to known empty directory so we don't pick up some other .ipdb
        # file from the CWD tests are actually run from.
        save_cwd = os.getcwd()
        self.addCleanup(os.chdir, save_cwd)
        cwd_dir = os.path.join(self.tmpd, "cwd")
        os.mkdir(cwd_dir)
        os.chdir(cwd_dir)
        # This represents the $HOME config file, and doubles for the current
        # working directory config file if we set CWD to self.tmpd
        self.default_filename = os.path.join(self.tmpd, ".ipdb")
        self.default_context = 10
        self._write_file(
            self.default_filename,
            [
                "# this is a test config file for ipdb",
                "context = {}".format(str(self.default_context)),
            ],
        )
        self.env_filename = os.path.join(self.tmpd, "ipdb.env")
        self.env_context = 20
        self._write_file(
            self.env_filename,
            [
                "# this is a test config file for ipdb",
                "context = {}".format(str(self.env_context)),
            ],
        )
        self.setup_filename = os.path.join(cwd_dir, "setup.cfg")
        self.setup_context = 25
        self._write_file(
            self.setup_filename,
            [
                "[ipdb]",
                "context = {}".format(str(self.setup_context)),
            ],
        )
        self.pyproject_filename = os.path.join(cwd_dir, "pyproject.toml")
        self.pyproject_context = 30
        self._write_file(
            self.pyproject_filename,
            [
                "[tool.ipdb]",
                "context = {}".format(str(self.pyproject_context)),
            ],
        )

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
            self.assertEqual(["tool.ipdb"], cfg.sections())
            self.assertEqual(self.pyproject_context, cfg.getint("tool.ipdb", "context"))
            self.assertRaises(configparser.NoOptionError, cfg.get, "tool.ipdb", "version")

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
            self.assertEqual(["tool.ipdb"], cfg.sections())
            self.assertEqual(self.pyproject_context, cfg.getint("tool.ipdb", "context"))
            self.assertRaises(configparser.NoOptionError, cfg.get, "tool.ipdb", "version")

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
        with ModifiedEnvironment(IPDB_CONFIG=self.env_filename,
                                 HOME=self.tmpd):
            cfg = get_config()
            self.assertEqual(["ipdb"], cfg.sections())
            self.assertEqual(self.env_context, cfg.getint("ipdb", "context"))
            self.assertRaises(configparser.NoOptionError, cfg.getboolean, "ipdb", "version")

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
        with ModifiedEnvironment(IPDB_CONFIG=self.env_filename,
                                 HOME=self.tmpd):
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
        with ModifiedEnvironment(IPDB_CONFIG=self.env_filename,
                                 HOME=self.tmpd):
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
            self.assertRaises(configparser.NoOptionError, cfg.getboolean, "ipdb", "version")

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
        with ModifiedEnvironment(IPDB_CONFIG=self.env_filename,
                                 HOME=self.tmpd):
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
        with ModifiedEnvironment(IPDB_CONFIG=self.env_filename,
                                 HOME=self.tmpd):
            cfg = get_config()
            self.assertEqual(["ipdb"], cfg.sections())
            self.assertEqual(self.env_context, cfg.getint("ipdb", "context"))
            self.assertRaises(configparser.NoOptionError, cfg.getboolean, "ipdb", "version")

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
