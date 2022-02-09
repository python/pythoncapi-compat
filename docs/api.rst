+++++++++++++++++++++++
pythoncapi_compat.h API
+++++++++++++++++++++++

The ``pythoncapi_compat.h`` header file provides implementations of recent
functions for old Python versions.

Supported Python versions:

* Python 2.7, Python 3.5 - 3.11
* PyPy 2.7, 3.6 and 3.7

C++ is supported on Python 3.6 and newer.

A C99 subset is required, like ``static inline`` functions: see `PEP 7
<https://www.python.org/dev/peps/pep-0007/>`_.  ISO C90 is partially supported
for Python 2.7 and Visual Studio 2008 (avoid mixed declarations and code, ``gcc
-Werror=declaration-after-statement``).

Some functions related to frame objects and ``PyThreadState`` are not available
on PyPy.

Latest version of the header file:
`pythoncapi_compat.h <https://raw.githubusercontent.com/pythoncapi/pythoncapi_compat/master/pythoncapi_compat.h>`_.


Python 3.11
-----------

::

    // Not available on PyPy
    void PyThreadState_EnterTracing(PyThreadState *tstate);
    // Not available on PyPy
    void PyThreadState_LeaveTracing(PyThreadState *tstate);

Python 3.10
-----------

::

    PyObject* Py_NewRef(PyObject *obj);
    PyObject* Py_XNewRef(PyObject *obj);
    int Py_Is(PyObject *x, PyObject *y);
    int Py_IsNone(PyObject *x);
    int Py_IsTrue(PyObject *x);
    int Py_IsFalse(PyObject *x);

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
    // Not available on PyPy
    PyFrameObject* PyFrame_GetBack(PyFrameObject *frame);

PyThreadState
^^^^^^^^^^^^^

::

    // Not available on PyPy
    PyFrameObject* PyThreadState_GetFrame(PyThreadState *tstate);
    PyInterpreterState* PyThreadState_GetInterpreter(PyThreadState *tstate);
    // Availability: Python 3.7. Not available on PyPy.
    uint64_t PyThreadState_GetID(PyThreadState *tstate);

PyInterpreterState
^^^^^^^^^^^^^^^^^^

::

    PyInterpreterState* PyInterpreterState_Get(void);

GC protocol
^^^^^^^^^^^

::

    // Not available on PyPy.
    int PyObject_GC_IsTracked(PyObject* obj);
    // Availability: Python 3.4. Not available on PyPy.
    int PyObject_GC_IsFinalized(PyObject *obj);

Module helper
^^^^^^^^^^^^^

::

    int PyModule_AddType(PyObject *module, PyTypeObject *type);

Python 3.5.2
------------

::

    Py_SETREF(op, op2)
    Py_XSETREF(op, op2)

Python 3.4
----------

::

    Py_UNUSED(name)

Borrow variant
--------------

To ease migration of C extensions to the new C API, a variant is provided
to return borrowed references rather than strong references::

    // Similar to "Py_DECREF(ob); return ob;"
    PyObject* _Py_StealRef(PyObject *ob);

    // Similar to "Py_XDECREF(ob); return ob;"
    PyObject* _Py_XStealRef(PyObject *ob);

    // PyThreadState_GetFrame(). Not available on PyPy.
    PyFrameObject* _PyThreadState_GetFrameBorrow(PyThreadState *tstate)

    // PyFrame_GetCode()
    PyCodeObject* _PyFrame_GetCodeBorrow(PyFrameObject *frame)

    // PyFrame_GetBack(). Not available on PyPy.
    PyFrameObject* _PyFrame_GetBackBorrow(PyFrameObject *frame)

For example, ``tstate->frame`` can be replaced with
``_PyThreadState_GetFrameBorrow(tstate)`` to avoid accessing directly
``PyThreadState.frame`` member.

These functions are only available in ``pythoncapi_compat.h`` and are not
part of the Python C API.
