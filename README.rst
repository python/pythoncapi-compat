++++++++++++++++++++++++++
Python C API compatibility
++++++++++++++++++++++++++

.. image:: https://travis-ci.com/pythoncapi/pythoncapi_compat.svg?branch=master
   :alt: Build status of pyperf on Travis CI
   :target: https://travis-ci.com/github/pythoncapi/pythoncapi_compat

Header file providing new functions of the Python C API to Python 3.6.

Python 3.6 to Python 3.10 are supported. It requires a subset of C99 like
``static inline`` functions:
see `PEP 7 <https://www.python.org/dev/peps/pep-0007/>`_.

Homepage:
https://github.com/pythoncapi/pythoncapi_compat

Latest header file:
https://raw.githubusercontent.com/pythoncapi/pythoncapi_compat/master/pythoncapi_compat.h

This project is distributed under the MIT license.

This project is covered by the `PSF Code of Conduct
<https://www.python.org/psf/codeofconduct/>`_.


Usage
=====

Copy the header file in your project and include it using::

    #include "pythoncapi_compat.h"


Functions
=========

Borrow variant
--------------

To ease migration of C extensions to the new C API, a variant is provided
to return borrowed references rather than strong references::

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

Python 3.9
----------

::

    // PyObject
    void Py_SET_REFCNT(PyObject *ob, Py_ssize_t refcnt)
    void Py_SET_TYPE(PyObject *ob, PyTypeObject *type)
    void Py_SET_SIZE(PyVarObject *ob, Py_ssize_t size)
    int Py_IS_TYPE(const PyObject *ob, const PyTypeObject *type)

    PyObject* PyObject_CallNoArgs(PyObject *func)
    PyObject* PyObject_CallOneArg(PyObject *func, PyObject *arg)

    // PyFrameObject
    PyCodeObject* PyFrame_GetCode(PyFrameObject *frame)
    PyFrameObject* PyFrame_GetBack(PyFrameObject *frame)

    // PyThreadState
    PyFrameObject* PyThreadState_GetFrame(PyThreadState *tstate)
    PyInterpreterState* PyThreadState_GetInterpreter(PyThreadState *tstate)
    // Availability: Python 3.7+
    uint64_t PyThreadState_GetID(PyThreadState *tstate)

    // PyInterpreterState
    PyInterpreterState* PyInterpreterState_Get(void)

    // GC protocol
    int PyObject_GC_IsTracked(PyObject* obj)
    int PyObject_GC_IsFinalized(PyObject *obj)

    // Module helper
    int PyModule_AddType(PyObject *module, PyTypeObject *type)


Run tests
=========

Run the command::

    python3 tests/test_matrix.py
    # add -v option for verbose mode

To test one specific Python executable::

    python3.6 tests/run_tests.py
    # add -v option for verbose mode


Changelog
=========

* 2020-06-04: Creation of the project.
