IPython `pdb`
=============

Use 

::

        from ipdb import set_trace; set_trace()

or

::

        from ipdb import pm; pm()

You then get all IPython features (tab completion, syntax highlighting, better
tracebacks, better introspection) right in `pdb`.

If you install ``ipdb`` with a tool which supports ``setuptools`` entry points,
an ``ipdb`` script is made for you. You can use it to debug your scripts like

::

        $ bin/ipdb mymodule.py

With Python 2.7 only, you can also use

::

        $ python -m ipdb mymodule.py

PDBDebugMode support
--------------------

``ipdb`` support is integrated in Zope 2 ``Products.PDBDebugMode``. 
If ``ipdb`` is available, it is used in place of ``pdb``.

Development
===========

``ipdb`` source code and tracker are at https://github.com/gotcha/ipdb.
