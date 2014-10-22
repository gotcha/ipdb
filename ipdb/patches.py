# Copyright (c) 2007, 2010, 2011, 2012 Godefroid Chapelle
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

# You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.

# Disable IPython history in the debugger:
# The sqlite-based history of newer IPython versions gets
# confused by multithreaded apps like Zope (and Django?),
# causing errors when quitting/reloading:
# "ProgrammingError: SQLite objects created in a thread can only be used in
# that same thread."
#
# It is possible to disable the history in the IPython global configuration
# file, but the IPython debugger does not load the configuration.
# When embedding IPython, it is up to each app doing the embedding to configure
# IPython as needed. But no such possibility exists for the debugger, therefore
# this patch.

try:
    from IPython.core.history import HistoryManager
    HistoryManager.enabled = False
except ImportError:
    pass
