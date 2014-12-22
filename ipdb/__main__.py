# Copyright (c) 2011, 2012 Godefroid Chapelle
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

from __future__ import print_function
import sys
import os
import traceback

from contextlib import contextmanager

try:
    from pdb import Restart
except ImportError:
    class Restart(Exception):
        pass

import IPython

if IPython.__version__ > '0.10.2':
    from IPython.core.debugger import Pdb, BdbQuit_excepthook
    try:
        get_ipython
    except NameError:
        # Make it more resilient to different versions of IPython and try to
        # find a module.
        possible_modules = ['IPython.terminal.embed',           # Newer IPython
                            'IPython.frontend.terminal.embed']  # Older IPython

        count = len(possible_modules)
        for module in possible_modules:
            try:
                embed = __import__(module, fromlist=["InteractiveShellEmbed"])
                InteractiveShellEmbed = embed.InteractiveShellEmbed
            except ImportError:
                count -= 1
                if count == 0:
                    raise
            else:
                break

        ipshell = InteractiveShellEmbed()
        def_colors = ipshell.colors
    else:
        def_colors = get_ipython.im_self.colors

    from IPython.utils import io

    if 'nose' in sys.modules.keys():
        def update_stdout():
            # setup stdout to ensure output is available with nose
            io.stdout = sys.stdout = sys.__stdout__
    else:
        def update_stdout():
            pass
else:
    from IPython.Debugger import Pdb, BdbQuit_excepthook
    from IPython.Shell import IPShell
    from IPython import ipapi

    ip = ipapi.get()
    if ip is None:
        IPShell(argv=[''])
        ip = ipapi.get()
    def_colors = ip.options.colors

    from IPython.Shell import Term

    if 'nose' in sys.modules.keys():
        def update_stdout():
            # setup stdout to ensure output is available with nose
            Term.cout = sys.stdout = sys.__stdout__
    else:
        def update_stdout():
            pass


def wrap_sys_excepthook():
    # make sure we wrap it only once or we would end up with a cycle
    #  BdbQuit_excepthook.excepthook_ori == BdbQuit_excepthook
    if sys.excepthook != BdbQuit_excepthook:
        BdbQuit_excepthook.excepthook_ori = sys.excepthook
        sys.excepthook = BdbQuit_excepthook


def set_trace(frame=None):
    update_stdout()
    wrap_sys_excepthook()
    if frame is None:
        frame = sys._getframe().f_back
    Pdb(def_colors).set_trace(frame)


def post_mortem(tb):
    update_stdout()
    wrap_sys_excepthook()
    p = Pdb(def_colors)
    p.reset()
    if tb is None:
        return
    p.interaction(None, tb)


def pm():
    post_mortem(sys.last_traceback)


def run(statement, globals=None, locals=None):
    Pdb(def_colors).run(statement, globals, locals)


def runcall(*args, **kwargs):
    return Pdb(def_colors).runcall(*args, **kwargs)


def runeval(expression, globals=None, locals=None):
    return Pdb(def_colors).runeval(expression, globals, locals)


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


def main():
    if not sys.argv[1:] or sys.argv[1] in ("--help", "-h"):
        print("usage: ipdb.py scriptfile [arg] ...")
        sys.exit(2)

    mainpyfile = sys.argv[1]     # Get script filename
    if not os.path.exists(mainpyfile):
        print('Error:', mainpyfile, 'does not exist')
        sys.exit(1)

    del sys.argv[0]         # Hide "pdb.py" from argument list

    # Replace pdb's dir with script's dir in front of module search path.
    sys.path[0] = os.path.dirname(mainpyfile)

    # Note on saving/restoring sys.argv: it's a good idea when sys.argv was
    # modified by the script being debugged. It's a bad idea when it was
    # changed by the user from the command line. There is a "restart" command
    # which allows explicit specification of command line arguments.
    pdb = Pdb(def_colors)
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
