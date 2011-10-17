IPython `pdb`
=============

Use 

::

        from ipdb import set_trace; set_trace()

or

::

        from ipdb import pm; pm()

You then get all IPython_ features (tab completion, syntax highlighting, better
tracebacks, better introspection) right in `pdb`.

.. _IPython: http://ipython.org

If you install ``ipdb`` with a tool which supports ``setuptools`` entry points,
an ``ipdb`` script is made for you. You can use it to debug your scripts like

::

        $ bin/ipdb mymodule.py

With Python 2.7 only, you can also use

::

        $ python -m ipdb mymodule.py

Development
-----------

``ipdb`` source code and tracker are at https://github.com/gotcha/ipdb.

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

.. _ipdbplugin: http://pypi.python.org/pypi/iw.debug
.. _nose: http://readthedocs.org/docs/nose
