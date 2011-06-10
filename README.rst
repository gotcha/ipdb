IPython `pdb`
=============

Use 

::

        from ipdb import set_trace; set_trace()

or

::

        from ipdb import pm; pm()

You then get all IPython features (tab completion, nice tracebacks)
right in `pdb`.

With Python 2.7 only, you can also use

::

        $> python -m ipdb mymodule.py

PDBDebugMode support
--------------------

``ipdb`` support is integrated in Zope 2 ``Products.PDBDebugMode``. 
If ``ipdb`` is available, it is used in place of ``pdb``.

Development
===========

``ipdb`` source code and tracker are at https://github.com/gotcha/ipdb.
