# Copyright (c) 2011-2016 Godefroid Chapelle and ipdb development team
#
# This file is part of ipdb.
# Redistributable under the revised BSD license
# https://opensource.org/licenses/BSD-3-Clause

from __future__ import print_function
import os
import sys

from contextlib import contextmanager


def import_module(possible_modules, needed_module):
    """Make it more resilient to different versions of IPython and try to
    find a module."""
    count = len(possible_modules)
    for module in possible_modules:
        try:
            return __import__(module, fromlist=[needed_module])
        except ImportError:
            count -= 1
            if count == 0:
                raise
try:
    # IPython 5.0 and newer
    from IPython.terminal.debugger import TerminalPdb as Pdb
    from IPython.core.debugger import BdbQuit_excepthook
    from IPython.terminal.interactiveshell import TerminalInteractiveShell
    # Let IPython decide about which debugger class to use
    # This is especially important for tools that fiddle with stdout
    debugger_cls = TerminalInteractiveShell().debugger_cls
except ImportError:
    from IPython.core.debugger import Pdb, BdbQuit_excepthook
    debugger_cls = Pdb

possible_modules = ['IPython.terminal.ipapp',           # Newer IPython
                    'IPython.frontend.terminal.ipapp']  # Older IPython

app = import_module(possible_modules, "TerminalIPythonApp")
TerminalIPythonApp = app.TerminalIPythonApp

possible_modules = ['IPython.terminal.embed',           # Newer IPython
                    'IPython.frontend.terminal.embed']  # Older IPython
embed = import_module(possible_modules, "InteractiveShellEmbed")
InteractiveShellEmbed = embed.InteractiveShellEmbed
try:
    get_ipython
except NameError:
    # Build a terminal app in order to force ipython to load the
    # configuration
    ipapp = TerminalIPythonApp()
    # Avoid output (banner, prints)
    ipapp.interact = False
    ipapp.initialize([])
    def_colors = ipapp.shell.colors
else:
    # If an instance of IPython is already running try to get an instance
    # of the application. If there is no TerminalIPythonApp instanciated
    # the instance method will create a new one without loading the config.
    # i.e: if we are in an embed instance we do not want to load the config.
    ipapp = TerminalIPythonApp.instance()
    shell = get_ipython()
    def_colors = shell.colors

    # Detect if embed shell or not and display a message
    if isinstance(shell, InteractiveShellEmbed):
        shell.write_err(
            "\nYou are currently into an embedded ipython shell,\n"
            "the configuration will not be loaded.\n\n"
        )

def_exec_lines = [line + '\n' for line in ipapp.exec_lines]

def _init_pdb(context=3, commands=[]):
    try:
        p = debugger_cls(def_colors, context=context)
    except TypeError:
        p = debugger_cls(def_colors)
    p.rcLines += def_exec_lines
    p.rcLines.extend(commands)
    return p


def wrap_sys_excepthook():
    # make sure we wrap it only once or we would end up with a cycle
    #  BdbQuit_excepthook.excepthook_ori == BdbQuit_excepthook
    if sys.excepthook != BdbQuit_excepthook:
        BdbQuit_excepthook.excepthook_ori = sys.excepthook
        sys.excepthook = BdbQuit_excepthook


def set_trace(frame=None, context=3):
    wrap_sys_excepthook()
    if frame is None:
        frame = sys._getframe().f_back
    p = _init_pdb(context).set_trace(frame)
    if p and hasattr(p, 'shell'):
        p.shell.restore_sys_module_state()


def post_mortem(tb=None):
    wrap_sys_excepthook()
    p = _init_pdb()
    p.reset()
    if tb is None:
        # sys.exc_info() returns (type, value, traceback) if an exception is
        # being handled, otherwise it returns None
        tb = sys.exc_info()[2]
    if tb:
        p.interaction(None, tb)


def pm():
    post_mortem(sys.last_traceback)


def run(statement, globals=None, locals=None):
    _init_pdb().run(statement, globals, locals)


def runcall(*args, **kwargs):
    return _init_pdb().runcall(*args, **kwargs)


def runeval(expression, globals=None, locals=None):
    return _init_pdb().runeval(expression, globals, locals)


@contextmanager
def launch_ipdb_on_exception():
    try:
        yield
    except Exception:
        e, m, tb = sys.exc_info()
        print(m.__repr__(), file=sys.stderr)
        post_mortem(tb)
    finally:
        pass


_usage = """\
usage: python -m ipdb [-c command] ... pyfile [arg] ...

Debug the Python program given by pyfile.

Initial commands are read from .pdbrc files in your home directory
and in the current directory, if they exist.  Commands supplied with
-c are executed after commands from .pdbrc files.

To let the script run until an exception occurs, use "-c continue".
To let the script run up to a given line X in the debugged file, use
"-c 'until X'"."""


def main():
    import traceback
    import sys
    import getopt

    try:
        from pdb import Restart
    except ImportError:
        class Restart(Exception):
            pass
    
    opts, args = getopt.getopt(sys.argv[1:], 'hc:', ['--help', '--command='])

    if not args:
        print(_usage)
        sys.exit(2)
    
    commands = []
    for opt, optarg in opts:
        if opt in ['-h', '--help']:
            print(_usage)
            sys.exit()
        elif opt in ['-c', '--command']:
            commands.append(optarg)

    mainpyfile = args[0]     # Get script filename
    if not os.path.exists(mainpyfile):
        print('Error:', mainpyfile, 'does not exist')
        sys.exit(1)

    sys.argv = args     # Hide "pdb.py" from argument list

    # Replace pdb's dir with script's dir in front of module search path.
    sys.path[0] = os.path.dirname(mainpyfile)

    # Note on saving/restoring sys.argv: it's a good idea when sys.argv was
    # modified by the script being debugged. It's a bad idea when it was
    # changed by the user from the command line. There is a "restart" command
    # which allows explicit specification of command line arguments.
    pdb = _init_pdb(commands=commands)
    while 1:
        try:
            pdb._runscript(mainpyfile)
            if pdb._user_requested_quit:
                break
            print("The program finished and will be restarted")
        except Restart:
            print("Restarting", mainpyfile, "with arguments:")
            print("\t" + " ".join(sys.argv[1:]))
        except SystemExit:
            # In most cases SystemExit does not warrant a post-mortem session.
            print("The program exited via sys.exit(). Exit status: ", end='')
            print(sys.exc_info()[1])
        except:
            traceback.print_exc()
            print("Uncaught exception. Entering post mortem debugging")
            print("Running 'cont' or 'step' will restart the program")
            t = sys.exc_info()[2]
            pdb.interaction(None, t)
            print("Post mortem debugger finished. The " + mainpyfile +
                  " will be restarted")

if __name__ == '__main__':
    main()
