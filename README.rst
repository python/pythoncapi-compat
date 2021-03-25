++++++++++++++++++++++++++
Python C API compatibility
++++++++++++++++++++++++++

.. image:: https://github.com/pythoncapi/pythoncapi_compat/actions/workflows/build.yml/badge.svg
   :alt: Build status of pythoncapi_compat on GitHub Actions
   :target: https://github.com/pythoncapi/pythoncapi_compat/actions

The Python C API compatibility project is made of two parts:

* ``pythoncapi_compat.h``: Header file providing new functions of the Python C
  API to old Python versions.
* ``upgrade_pythoncapi.py``: Script upgrading C extension modules to newer
  Python API without losing support for old Python versions. It relies on
  ``pythoncapi_compat.h``.

``pythoncapi_compat.h`` supports Python 2.7 to Python 3.10. A C99 subset is
required, like ``static inline`` functions: see `PEP 7
<https://www.python.org/dev/peps/pep-0007/>`_. ISO C90 is partially supported
for Python 2.7: avoid mixed declarations and code (GCC
``-Werror=declaration-after-statement`` flag) and support Visual Studio 2008.

``upgrade_pythoncapi.py`` requires Python 3.6 or newer.

Homepage:
https://github.com/pythoncapi/pythoncapi_compat

Latest header file:
https://raw.githubusercontent.com/pythoncapi/pythoncapi_compat/master/pythoncapi_compat.h

This project is distributed under the MIT license.

This project is covered by the `PSF Code of Conduct
<https://www.python.org/psf/codeofconduct/>`_.


Usage
=====

Run upgrade_pythoncapi.py
-------------------------

Upgrade ``mod.c`` file::

    python3 upgrade_pythoncapi.py mod.c

Upgrade all ``.c`` and ``.h`` files of a project::

    python3 upgrade_pythoncapi.py directory/

WARNING: files are modified in-place! If a file is modified, the original file
is saved as ``<filename>.old``.

To see command line options and list available operations, run it with no
arguments::

    python3 upgrade_pythoncapi.py

For example, to only replace ``op->ob_type`` with ``Py_TYPE(op)``, use::

    python3 upgrade_pythoncapi.py -o Py_TYPE mod.c

Or the opposite, to apply all operations but leave ``op->ob_type`` unchanged,
use::

    python3 upgrade_pythoncapi.py -o all,-Py_TYPE mod.c

Copy pythoncapi_compat.h
------------------------

Most upgrade_pythoncapi.py operations add ``#include "pythoncapi_compat.h"``.
You may have to copy the ``pythoncapi_compat.h`` header file to your project.
It can be copied from::

    https://raw.githubusercontent.com/pythoncapi/pythoncapi_compat/master/pythoncapi_compat.h


Upgrade Operations
==================

``upgrade_pythoncapi.py`` implements the following operations:

* ``Py_TYPE``:

  * Replace ``op->ob_type`` with ``Py_TYPE(op)``.

* ``Py_SIZE``:

  * Replace ``op->ob_size`` with ``Py_SIZE(op)``.

* ``Py_REFCNT``:

  * Replace ``op->ob_refcnt`` with ``Py_REFCNT(op)``.

* ``Py_SET_TYPE``:

  * Replace ``obj->ob_type = type;`` with ``Py_SET_TYPE(obj, type);``.
  * Replace ``Py_TYPE(obj) = type;`` with ``Py_SET_TYPE(obj, type);``.

* ``Py_SET_SIZE``:

  * Replace ``obj->ob_size = size;`` with ``Py_SET_SIZE(obj, size);``.
  * Replace ``Py_SIZE(obj) = size;`` with ``Py_SET_SIZE(obj, size);``.

* ``Py_SET_REFCNT``:

  * Replace ``obj->ob_refcnt = refcnt;`` with ``Py_SET_REFCNT(obj, refcnt);``.
  * Replace ``Py_REFCNT(obj) = refcnt;`` with ``Py_SET_REFCNT(obj, refcnt);``.

* ``PyObject_NEW``:

  * Replace ``PyObject_NEW(...)`` with ``PyObject_New(...)``.
  * Replace ``PyObject_NEW_VAR(...)`` with ``PyObject_NewVar(...)``.

* ``PyMem_MALLOC``:

  * Replace ``PyMem_MALLOC(n)`` with ``PyMem_Malloc(n)``.
  * Replace ``PyMem_REALLOC(ptr, n)`` with ``PyMem_Realloc(ptr, n)``.
  * Replace ``PyMem_FREE(ptr)``, ``PyMem_DEL(ptr)`` and ``PyMem_Del(ptr)`` .
    with ``PyMem_Free(n)``.

* ``PyObject_MALLOC``:

  * Replace ``PyObject_MALLOC(n)`` with ``PyObject_Malloc(n)``.
  * Replace ``PyObject_REALLOC(ptr, n)`` with ``PyObject_Realloc(ptr, n)``.
  * Replace ``PyObject_FREE(ptr)``, ``PyObject_DEL(ptr)``
    and ``PyObject_Del(ptr)`` .  with ``PyObject_Free(n)``.

* ``PyFrame_GetBack``:

  * Replace ``frame->f_back`` with ``_PyFrame_GetBackBorrow(frame)``.

* ``PyFrame_GetCode``:

  * Replace ``frame->f_code`` with ``_PyFrame_GetCodeBorrow(frame)``.

* ``PyThreadState_GetInterpreter``:

  * Replace ``tstate->interp`` with ``PyThreadState_GetInterpreter(tstate)``.

* ``PyThreadState_GetFrame``:

  * Replace ``tstate->frame`` with ``_PyThreadState_GetFrameBorrow(tstate)``.


pythoncapi_compat.h functions
=============================

Borrow variant
--------------

To ease migration of C extensions to the new C API, a variant is provided
to return borrowed references rather than strong references::

    // Similar to "Py_INCREF(ob); return ob;"
    PyObject* _Py_StealRef(PyObject *ob);

    // Similar to "Py_XINCREF(ob); return ob;"
    PyObject* _Py_XStealRef(PyObject *ob);

    // PyThreadState_GetFrame()
    PyFrameObject* _PyThreadState_GetFrameBorrow(PyThreadState *tstate)

    // PyFrame_GetCode()
    PyCodeObject* _PyFrame_GetCodeBorrow(PyFrameObject *frame)

    // PyFrame_GetBack()
    PyFrameObject* _PyFrame_GetBackBorrow(PyFrameObject *frame)

For example, ``tstate->frame`` can be replaced with
``_PyThreadState_GetFrameBorrow(tstate)`` to avoid accessing directly
``PyThreadState.frame`` member.

These functions are only available in ``pythoncapi_compat.h`` and are not
part of the Python C API.

Python 3.10
-----------

::

    PyObject* Py_NewRef(PyObject *obj);
    PyObject* Py_XNewRef(PyObject *obj);

    int PyModule_AddObjectRef(PyObject *module, const char *name, PyObject *value);

Python 3.9
----------

PyObject
^^^^^^^^

::

    void Py_SET_REFCNT(PyObject *ob, Py_ssize_t refcnt);
    void Py_SET_TYPE(PyObject *ob, PyTypeObject *type);
    void Py_SET_SIZE(PyVarObject *ob, Py_ssize_t size);
    int Py_IS_TYPE(const PyObject *ob, const PyTypeObject *type);

    PyObject* PyObject_CallNoArgs(PyObject *func);
    PyObject* PyObject_CallOneArg(PyObject *func, PyObject *arg);

PyFrameObject
^^^^^^^^^^^^^

::

    PyCodeObject* PyFrame_GetCode(PyFrameObject *frame);
    PyFrameObject* PyFrame_GetBack(PyFrameObject *frame);

PyThreadState
^^^^^^^^^^^^^

::

    PyFrameObject* PyThreadState_GetFrame(PyThreadState *tstate);
    PyInterpreterState* PyThreadState_GetInterpreter(PyThreadState *tstate);
    // Availability: Python 3.7
    uint64_t PyThreadState_GetID(PyThreadState *tstate);

PyInterpreterState
^^^^^^^^^^^^^^^^^^

::

    PyInterpreterState* PyInterpreterState_Get(void);

GC protocol
^^^^^^^^^^^

::

    int PyObject_GC_IsTracked(PyObject* obj);
    // Availability: Python 3.4
    int PyObject_GC_IsFinalized(PyObject *obj);

Module helper
^^^^^^^^^^^^^

::

    int PyModule_AddType(PyObject *module, PyTypeObject *type);


Run tests
=========

Run tests::

    python3 runtests.py

Only test the current Python version, don't test multiple Python versions
(``-c``, ``--current``)::

    python3 runtests.py --current

Verbose mode (``-v``, ``--verbose``)::

    python3 runtests.py --verbose

See tests in the ``tests/`` subdirectory.


Links
=====

* `PEP 620 -- Hide implementation details from the C API
  <https://www.python.org/dev/peps/pep-0620/>`_
* Make structures opaque

  * `bpo-39573: PyObject <https://bugs.python.org/issue39573>`_
  * `bpo-40170: PyTypeObject <https://bugs.python.org/issue40170>`_
  * `bpo-39947: PyThreadState <https://bugs.python.org/issue39947>`_
  * `bpo-40421: PyFrameObject <https://bugs.python.org/issue40421>`_

* `Python/C API Reference Manual <https://docs.python.org/dev/c-api/>`_
* `HPy: a better API for Python
  <https://hpy.readthedocs.io/>`_
* `Cython: C-extensions for Python
  <https://cython.org/>`_

  * `ModuleSetupCode.c
    <https://github.com/cython/cython/blob/0.29.x/Cython/Utility/ModuleSetupCode.c>`_
    provides functions like ``__Pyx_SET_REFCNT()``
  * Cython doesn't use pythoncapi_compat.h:
    `see Cython issue #3934
    <https://github.com/cython/cython/issues/3934>`_

* `Old 2to3c project <https://github.com/davidmalcolm/2to3c>`_ by David Malcolm
  which uses `Coccinelle <https://coccinelle.gitlabpages.inria.fr/website/>`_
  to ease migration of C extensions from Python 2 to Python 3. See
  also `2to3c: an implementation of Python's 2to3 for C code
  <https://dmalcolm.livejournal.com/3935.html>`_ article (2009).


Changelog
=========

* 2021-02-16: Add ``_Py_StealRef()`` and ``_Py_XStealRef()`` functions.
* 2021-01-27: Fix compatibility with Visual Studio 2008 for Python 2.7.
* 2020-11-30: Creation of the ``upgrade_pythoncapi.py`` script.
* 2020-06-04: Creation of the ``pythoncapi_compat.h`` header file.


Examples of projects using pythoncapi_compat.h
==============================================

* `bitarray <https://github.com/ilanschnell/bitarray/>`_:
  ``bitarray/_bitarray.c`` uses ``Py_SET_SIZE()``
  (`pythoncapi_compat.h copy
  <https://github.com/ilanschnell/bitarray/blob/master/bitarray/pythoncapi_compat.h>`__)
* `immutables <https://github.com/MagicStack/immutables/>`_:
  ``immutables/_map.c`` uses ``Py_SET_SIZE()``
  (`pythoncapi_compat.h copy
  <https://github.com/MagicStack/immutables/blob/master/immutables/pythoncapi_compat.h>`__)
* `Mercurial (hg) <https://www.mercurial-scm.org/>`_ uses ``Py_SET_TYPE()``
  (`commit
  <https://www.mercurial-scm.org/repo/hg/rev/e92ca942ddca>`__,
  `pythoncapi_compat.h copy
  <https://www.mercurial-scm.org/repo/hg/file/tip/mercurial/pythoncapi_compat.h>`__)
* `python-zstandard <https://github.com/indygreg/python-zstandard/>`_
  uses ``Py_SET_TYPE()`` and ``Py_SET_SIZE()``
  (`commit <https://github.com/indygreg/python-zstandard/commit/e5a3baf61b65f3075f250f504ddad9f8612bfedf>`__):
  Mercurial extension.
