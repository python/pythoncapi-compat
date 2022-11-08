+++++++++++++++++++++++
pythoncapi_compat.h API
+++++++++++++++++++++++

The ``pythoncapi_compat.h`` header file provides implementations of recent
functions for old Python versions.

Supported Python versions:

* Python 2.7, Python 3.4 - 3.11
* PyPy 2.7, 3.6 and 3.7

C++03 and C++11 are supported on Python 3.6 and newer.

A C99 subset is required, like ``static inline`` functions: see `PEP 7
<https://www.python.org/dev/peps/pep-0007/>`_.  ISO C90 is partially supported
for Python 2.7 and Visual Studio 2008 (avoid mixed declarations and code, ``gcc
-Werror=declaration-after-statement``).

Some functions related to frame objects and ``PyThreadState`` are not available
on PyPy.

Latest version of the header file:
`pythoncapi_compat.h <https://raw.githubusercontent.com/python/pythoncapi-compat/master/pythoncapi_compat.h>`_.


Python 3.12
-----------

.. c:function:: PyObject* PyFrame_GetVar(PyFrameObject *frame, PyObject *name)

   See `PyFrame_GetVar() documentation <https://docs.python.org/dev/c-api/frame.html#c.PyFrame_GetVar>`__.

   Not available on PyPy.

.. c:function:: PyObject* PyFrame_GetVarString(PyFrameObject *frame, const char *name)

   See `PyFrame_GetVarString() documentation <https://docs.python.org/dev/c-api/frame.html#c.PyFrame_GetVarString>`__.

   Not available on PyPy.


Python 3.11
-----------

.. c:function:: PyObject* PyCode_GetCellvars(PyCodeObject *code)

   See `PyCode_GetCellvars() documentation <https://docs.python.org/dev/c-api/code.html#c.PyCode_GetCellvars>`__.

   Not available on PyPy.

.. c:function:: PyObject* PyCode_GetCode(PyCodeObject *code)

   See `PyCode_GetCode() documentation <https://docs.python.org/dev/c-api/code.html#c.PyCode_GetCode>`__.

   Not available on PyPy.

.. c:function:: PyObject* PyCode_GetFreevars(PyCodeObject *code)

   See `PyCode_GetFreevars() documentation <https://docs.python.org/dev/c-api/code.html#c.PyCode_GetFreevars>`__.

   Not available on PyPy.

.. c:function:: PyObject* PyCode_GetVarnames(PyCodeObject *code)

   See `PyCode_GetVarnames() documentation <https://docs.python.org/dev/c-api/code.html#c.PyCode_GetVarnames>`__.

   Not available on PyPy.

.. c:function:: PyObject* PyFrame_GetBuiltins(PyFrameObject *frame)

   See `PyFrame_GetBuiltins() documentation <https://docs.python.org/dev/c-api/frame.html#c.PyFrame_GetBuiltins>`__.

   Not available on PyPy.

.. c:function:: PyObject* PyFrame_GetGlobals(PyFrameObject *frame)

   See `PyFrame_GetGlobals() documentation <https://docs.python.org/dev/c-api/frame.html#c.PyFrame_GetGlobals>`__.

   Not available on PyPy.

.. c:function:: int PyFrame_GetLasti(PyFrameObject *frame)

   See `PyFrame_GetLasti() documentation <https://docs.python.org/dev/c-api/frame.html#c.PyFrame_GetLasti>`__.

   Not available on PyPy.

.. c:function:: PyObject* PyFrame_GetLocals(PyFrameObject *frame)

   See `PyFrame_GetLocals() documentation <https://docs.python.org/dev/c-api/frame.html#c.PyFrame_GetLocals>`__.

   Not available on PyPy.

.. c:function:: void PyThreadState_EnterTracing(PyThreadState *tstate)

   See `PyThreadState_EnterTracing() documentation <https://docs.python.org/dev/c-api/init.html#c.PyThreadState_EnterTracing>`__.

   Not available on PyPy.

.. c:function:: void PyThreadState_LeaveTracing(PyThreadState *tstate)

   See `PyThreadState_LeaveTracing() documentation <https://docs.python.org/dev/c-api/init.html#c.PyThreadState_LeaveTracing>`__.

   Not available on PyPy

.. c:function:: int PyFloat_Pack2(double x, unsigned char *p, int le)

   Pack a C double as the IEEE 754 binary16 half-precision format.

   Availability: Python 3.6 and newer. Not available on PyPy

.. c:function:: int PyFloat_Pack4(double x, unsigned char *p, int le)

   Pack a C double as the IEEE 754 binary32 single precision format.

   Not available on PyPy

.. c:function:: int PyFloat_Pack8(double x, unsigned char *p, int le)

   Pack a C double as the IEEE 754 binary64 double precision format.

   Not available on PyPy

.. c:function:: double PyFloat_Unpack2(const unsigned char *p, int le)

   Unpack the IEEE 754 binary16 half-precision format as a C double.

   Availability: Python 3.6 and newer. Not available on PyPy

.. c:function:: double PyFloat_Unpack4(const unsigned char *p, int le)

   Unpack the IEEE 754 binary32 single precision format as a C double.

   Not available on PyPy

.. c:function:: double PyFloat_Unpack8(const unsigned char *p, int le)

   Unpack the IEEE 754 binary64 double precision format as a C double.

   Not available on PyPy

Python 3.10
-----------

.. c:function:: PyObject* Py_NewRef(PyObject *obj)

   See `Py_NewRef() documentation <https://docs.python.org/dev/c-api/refcounting.html#c.Py_NewRef>`__.

.. c:function:: PyObject* Py_XNewRef(PyObject *obj)

   See `Py_XNewRef() documentation <https://docs.python.org/dev/c-api/refcounting.html#c.Py_XNewRef>`__.

.. c:function:: int Py_Is(PyObject *x, PyObject *y)

   See `Py_Is() documentation <https://docs.python.org/dev/c-api/structures.html#c.Py_Is>`__.

.. c:function:: int Py_IsNone(PyObject *x)

   See `Py_IsNone() documentation <https://docs.python.org/dev/c-api/structures.html#c.Py_IsNone>`__.

.. c:function:: int Py_IsTrue(PyObject *x)

   See `Py_IsTrue() documentation <https://docs.python.org/dev/c-api/structures.html#c.Py_IsTrue>`__.

.. c:function:: int Py_IsFalse(PyObject *x)

   See `Py_IsFalse() documentation <https://docs.python.org/dev/c-api/structures.html#c.Py_IsFalse>`__.

.. c:function:: int PyModule_AddObjectRef(PyObject *module, const char *name, PyObject *value)

   See `PyModule_AddObjectRef() documentation <https://docs.python.org/dev/c-api/module.html#c.PyModule_AddObjectRef>`__.

Python 3.9
----------

PyObject
^^^^^^^^

.. c:function:: void Py_SET_REFCNT(PyObject *ob, Py_ssize_t refcnt)

   See `Py_SET_REFCNT() documentation <https://docs.python.org/dev/c-api/structures.html#c.Py_SET_REFCNT>`__.

.. c:function:: void Py_SET_TYPE(PyObject *ob, PyTypeObject *type)

   See `Py_SET_TYPE() documentation <https://docs.python.org/dev/c-api/structures.html#c.Py_SET_TYPE>`__.

.. c:function:: void Py_SET_SIZE(PyVarObject *ob, Py_ssize_t size)

   See `Py_SET_SIZE() documentation <https://docs.python.org/dev/c-api/structures.html#c.Py_SET_SIZE>`__.

.. c:function:: int Py_IS_TYPE(const PyObject *ob, const PyTypeObject *type)

   See `Py_IS_TYPE() documentation <https://docs.python.org/dev/c-api/structures.html#c.Py_IS_TYPE>`__.

.. c:function:: PyObject* PyObject_CallNoArgs(PyObject *func)

   See `PyObject_CallNoArgs() documentation <https://docs.python.org/dev/c-api/call.html#c.PyObject_CallNoArgs>`__.

.. c:function:: PyObject* PyObject_CallOneArg(PyObject *func, PyObject *arg)

   See `PyObject_CallOneArg() documentation <https://docs.python.org/dev/c-api/call.html#c.PyObject_CallOneArg>`__.


PyFrameObject
^^^^^^^^^^^^^

.. c:function:: PyCodeObject* PyFrame_GetCode(PyFrameObject *frame)

   See `PyFrame_GetCode() documentation <https://docs.python.org/dev/c-api/reflection.html#c.PyFrame_GetCode>`__.

.. c:function:: PyFrameObject* PyFrame_GetBack(PyFrameObject *frame)

   See `PyFrame_GetBack() documentation <https://docs.python.org/dev/c-api/reflection.html#c.PyFrame_GetBack>`__.

   Not available on PyPy


PyThreadState
^^^^^^^^^^^^^

.. c:function:: PyFrameObject* PyThreadState_GetFrame(PyThreadState *tstate)

   See `PyThreadState_GetFrame() documentation <https://docs.python.org/dev/c-api/init.html#c.PyThreadState_GetFrame>`__.

   Not available on PyPy

.. c:function:: PyInterpreterState* PyThreadState_GetInterpreter(PyThreadState *tstate)

   See `PyThreadState_GetInterpreter() documentation <https://docs.python.org/dev/c-api/init.html#c.PyThreadState_GetInterpreter>`__.

.. c:function:: uint64_t PyThreadState_GetID(PyThreadState *tstate)

   See `PyThreadState_GetID() documentation <https://docs.python.org/dev/c-api/init.html#c.PyThreadState_GetID>`__.

   Availability: Python 3.7. Not available on PyPy.

PyInterpreterState
^^^^^^^^^^^^^^^^^^

.. c:function:: PyInterpreterState* PyInterpreterState_Get(void)

   See `PyInterpreterState_Get() documentation <https://docs.python.org/dev/c-api/init.html#c.PyInterpreterState_Get>`__.


GC protocol
^^^^^^^^^^^

.. c:function:: int PyObject_GC_IsTracked(PyObject* obj)

   See `PyObject_GC_IsTracked() documentation <https://docs.python.org/dev/c-api/gcsupport.html#c.PyObject_GC_IsTracked>`__.

   Not available on PyPy.

.. c:function:: int PyObject_GC_IsFinalized(PyObject *obj)

   See `PyObject_GC_IsFinalized() documentation <https://docs.python.org/dev/c-api/gcsupport.html#c.PyObject_GC_IsFinalized>`__.

   Availability: Python 3.4. Not available on PyPy.

Module helper
^^^^^^^^^^^^^

.. c:function:: int PyModule_AddType(PyObject *module, PyTypeObject *type)

   See `PyModule_AddType() documentation <https://docs.python.org/dev/c-api/module.html#c.PyModule_AddType>`__.

Python 3.5.2
------------

.. c:macro:: Py_SETREF(op, op2)

.. c:macro:: Py_XSETREF(op, op2)

Python 3.4
----------

.. c:macro:: Py_UNUSED(name)

   See `Py_UNUSED() documentation <https://docs.python.org/dev/c-api/intro.html#c.Py_UNUSED>`__.

Borrow variant
--------------

To ease migration of C extensions to the new C API, a variant is provided
to return borrowed references rather than strong references.

These functions are only available in ``pythoncapi_compat.h`` and are not
part of the Python C API.

.. c:function:: PyObject* _Py_StealRef(PyObject *ob)

   Similar to ``Py_DECREF(ob); return ob;``.

.. c:function:: PyObject* _Py_XStealRef(PyObject *ob)

   Similar to ``Py_XDECREF(ob); return ob;``.

.. c:function:: PyFrameObject* _PyThreadState_GetFrameBorrow(PyThreadState *tstate)

   :c:func:`PyThreadState_GetFrame` variant. Not available on PyPy.

.. c:function:: PyCodeObject* _PyFrame_GetCodeBorrow(PyFrameObject *frame)

   :c:func:`PyFrame_GetCode` variant.

.. c:function:: PyFrameObject* _PyFrame_GetBackBorrow(PyFrameObject *frame)

   :c:func:`PyFrame_GetBack` variant Not available on PyPy.

For example, ``tstate->frame`` can be replaced with
``_PyThreadState_GetFrameBorrow(tstate)`` to avoid accessing directly
``PyThreadState.frame`` member.
