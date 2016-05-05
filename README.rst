IPython `pdb`
=============

.. image:: https://travis-ci.org/gotcha/ipdb.png?branch=master
  :target: https://travis-ci.org/gotcha/ipdb

Use
---

ipdb exports functions to access the IPython_ debugger, which features
tab completion, syntax highlighting, better tracebacks, better introspection
with the same interface as the `pdb` module.

Example usage:

.. code-block:: python

        import ipdb
        ipdb.set_trace()
        ipdb.set_trace(context=5)  # will show five lines of code
                                   # instead of the default three lines
        ipdb.pm()
        ipdb.run('x[0] = 3')
        result = ipdb.runcall(function, arg0, arg1, kwarg='foo')
        result = ipdb.runeval('f(1,2) - 3')

The post-mortem function, ``ipdb.pm()``, is equivalent to the magic function
``%debug``.

.. _IPython: http://ipython.org

If you install ``ipdb`` with a tool which supports ``setuptools`` entry points,
an ``ipdb`` script is made for you. You can use it to debug your python 2 scripts like

::

        $ bin/ipdb mymodule.py

And for python 3

::

        $ bin/ipdb3 mymodule.py

Alternatively with Python 2.7 only, you can also use

::

        $ python -m ipdb mymodule.py

You can also enclose code with the ``with`` statement to launch ipdb if an exception is raised:

.. code-block:: python

        from ipdb import launch_ipdb_on_exception

        with launch_ipdb_on_exception():
            [...]

.. warning::
   Context managers were introduced in Python 2.5.
   Adding a context manager implies dropping Python 2.4 support.
   Use ``ipdb==0.6`` with 2.4.

.. warning::
   Using ``from future import print_function`` for Python 3 compat implies dropping Python 2.5 support.
   Use ``ipdb<=0.8`` with 2.5.

Issues with ``stdout``
----------------------

Some tools, like ``nose`` fiddle with ``stdout``.

Until ``ipdb==0.9.4``, we tried to guess when we should also
fiddle with ``stdout`` to support those tools.
However, all strategies tried until 0.9.4 have proven brittle.

If you use ``nose`` or another tool that fiddles with ``stdout``, you should
explicitely ask for ``stdout`` fiddling by using ``ipdb`` like this

.. code-block:: python

        import ipdb
        ipdb.sset_trace()
        ipdb.spm()

        from ipdb import slaunch_ipdb_on_exception
        with slaunch_ipdb_on_exception():
            [...]


Development
-----------

``ipdb`` source code and tracker are at https://github.com/gotcha/ipdb.

Pull requests should take care of updating the changelog ``HISTORY.txt``.

Third-party support
-------------------

Products.PDBDebugMode
+++++++++++++++++++++

Zope2 Products.PDBDebugMode_ uses ``ipdb``, if available, in place of ``pdb``.

.. _Products.PDBDebugMode: http://pypi.python.org/pypi/Products.PDBDebugMode

iw.debug
++++++++

iw.debug_ allows you to trigger an ``ipdb`` debugger on any published object
of a Zope2 application.

.. _iw.debug: http://pypi.python.org/pypi/iw.debug

ipdbplugin
++++++++++

ipdbplugin_ is a nose_ test runner plugin that also uses the IPython debugger
instead of ``pdb``. (It does not depend on ``ipdb`` anymore).

.. _ipdbplugin: http://pypi.python.org/pypi/ipdbplugin
.. _nose: http://readthedocs.org/docs/nose
