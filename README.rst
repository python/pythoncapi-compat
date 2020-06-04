++++++++++++++++++++++++++
Python C API compatibility
++++++++++++++++++++++++++

Header file providing new functions of the Python C API for old Python versions.

Python 3.6 to Python 3.10 are supported. It requires a subset of C99 like
``static inline`` functions:
see `PEP 7 <https://www.python.org/dev/peps/pep-0007/>`_.

Homepage: https://github.com/pythoncapi/pythoncapi_compat

This project is distributed under the MIT license.

This project is covered by the `PSF Code of Conduct
<https://www.python.org/psf/codeofconduct/>`_.


Usage
=====

Copy the header file in your project and include it using::

    #include "pythoncapi_compat.h"


Functions
=========

Python 3.9
----------

::

    // PyObject
    void Py_SET_REFCNT(PyObject *ob, Py_ssize_t refcnt)
    void Py_SET_TYPE(PyObject *ob, PyTypeObject *type)
    void Py_SET_SIZE(PyVarObject *ob, Py_ssize_t size)

    PyObject* PyObject_CallNoArgs(PyObject *func)

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

To test one specific Python executable::

    python3.6 tests/run_tests.py
