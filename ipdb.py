import sys
from IPython.Debugger import Pdb
from IPython.Shell import IPShell

shell = IPShell(argv=[''])

def set_trace():
    Pdb('Linux').set_trace(sys._getframe().f_back)
