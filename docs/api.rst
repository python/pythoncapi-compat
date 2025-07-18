+++++++++++++++++++++++
pythoncapi_compat.h API
+++++++++++++++++++++++

The ``pythoncapi_compat.h`` header file provides implementations of recent
functions for old Python versions.

Supported Python versions:

* Python 3.6 - 3.14
* PyPy 2.7 and PyPy 3.6 - 3.10

Python 2.7 and Python 3.5 are no longer officially supported since GitHub
Actions doesn't support them anymore: only best effort support is provided.

C++03 and C++11 are supported on Python 3.6 and newer.

A C11 subset (without optional features) is required, like ``static inline``
functions: see `PEP 7 <https://www.python.org/dev/peps/pep-0007/>`_. ISO C90
is partially supported for Python 2.7.

Some functions related to frame objects and ``PyThreadState`` are not available
on PyPy.

Latest version of the header file:
`pythoncapi_compat.h <https://raw.githubusercontent.com/python/pythoncapi-compat/main/pythoncapi_compat.h>`_.


Python 3.15
-----------

.. c:function:: PyObject* PySys_GetAttr(const char *name)

   See `PySys_GetAttr() documentation  <https://docs.python.org/dev/c-api/sys.html#c.PySys_GetAttr>`__.

.. c:function:: PyObject* PySys_GetAttrString(const char *name)

   See `PySys_GetAttrString() documentation  <https://docs.python.org/dev/c-api/sys.html#c.PySys_GetAttrString>`__.

.. c:function:: PyObject* PySys_GetOptionalAttr(const char *name)

   See `PySys_GetOptionalAttr() documentation  <https://docs.python.org/dev/c-api/sys.html#c.PySys_GetOptionalAttr>`__.

.. c:function:: PyObject* PySys_GetOptionalAttrString(const char *name)

   See `PySys_GetOptionalAttrString() documentation  <https://docs.python.org/dev/c-api/sys.html#c.PySys_GetOptionalAttrString>`__.

Python 3.14
-----------

.. c:struct:: PyLongLayout

   See `PyLongLayout documentation <https://docs.python.org/dev/c-api/long.html#c.PyLongLayout>`__.

.. c:function:: const PyLongLayout* PyLong_GetNativeLayout(void)

   See `PyLong_GetNativeLayout() documentation  <https://docs.python.org/dev/c-api/long.html#c.PyLong_GetNativeLayout>`__.

.. c:struct:: PyLongExport

   See `PyLongExport documentation <https://docs.python.org/dev/c-api/long.html#c.PyLongExport>`__.

.. c:function:: int PyLong_Export(PyObject *obj, PyLongExport *export_long)

   See `PyLong_Export() documentation  <https://docs.python.org/dev/c-api/long.html#c.PyLong_Export>`__.

.. c:function:: void PyLong_FreeExport(PyLongExport *export_long)

   See `PyLong_FreeExport() documentation  <https://docs.python.org/dev/c-api/long.html#c.PyLong_FreeExport>`__.

.. c:struct:: PyLongWriter

   See `PyLongWriter documentation <https://docs.python.org/dev/c-api/long.html#c.PyLongWriter>`__.

.. c:function:: PyLongWriter* PyLongWriter_Create(int negative, Py_ssize_t ndigits, void **digits)

   See `PyLongWriter_Create() documentation  <https://docs.python.org/dev/c-api/long.html#c.PyLongWriter_Create>`__.

.. c:function:: PyObject* PyLongWriter_Finish(PyLongWriter *writer)

   See `PyLongWriter_Finish() documentation  <https://docs.python.org/dev/c-api/long.html#c.PyLongWriter_Finish>`__.

.. c:function:: void PyLongWriter_Discard(PyLongWriter *writer)

   See `PyLongWriter_Discard() documentation  <https://docs.python.org/dev/c-api/long.html#c.PyLongWriter_Discard>`__.

.. c:function:: int PyLong_IsPositive(PyObject *obj)

   See `PyLong_IsPositive() documentation  <https://docs.python.org/dev/c-api/long.html#c.PyLong_IsPositive>`__.

.. c:function:: int PyLong_IsNegative(PyObject *obj)

   See `PyLong_IsNegative() documentation  <https://docs.python.org/dev/c-api/long.html#c.PyLong_IsNegative>`__.

.. c:function:: int PyLong_IsZero(PyObject *obj)

   See `PyLong_IsZero() documentation  <https://docs.python.org/dev/c-api/long.html#c.PyLong_IsZero>`__.

.. c:function:: int PyLong_GetSign(PyObject *obj, int *sign)

   See `PyLong_GetSign() documentation <https://docs.python.org/dev/c-api/long.html#c.PyLong_GetSign>`__.

.. c:function:: PyObject* PyIter_NextItem(PyObject *sep, PyObject *iterable)

   See `PyIter_NextItem() documentation <https://docs.python.org/dev/c-api/iter.html#c.PyIter_NextItem>`__.

.. c:function:: PyObject* PyBytes_Join(PyObject *sep, PyObject *iterable)

   See `PyBytes_Join() documentation <https://docs.python.org/dev/c-api/bytes.html#c.PyBytes_Join>`__.

.. c:function:: Py_hash_t Py_HashBuffer(const void *ptr, Py_ssize_t len)

   See `Py_HashBuffer() documentation <https://docs.python.org/dev/c-api/hash.html#c.Py_HashBuffer>`__.

.. c:function:: int PyUnicode_Equal(PyObject *str1, PyObject *str2)

   See `PyUnicode_Equal() documentation <https://docs.python.org/dev/c-api/unicode.html#c.PyUnicode_Equal>`__.

.. c:function:: PyUnicodeWriter* PyUnicodeWriter_Create(Py_ssize_t length)

   See `PyUnicodeWriter_Create() documentation <https://docs.python.org/dev/c-api/unicode.html#c.PyUnicodeWriter_Create>`__.

.. c:function:: PyObject* PyUnicodeWriter_Finish(PyUnicodeWriter *writer)

   See `PyUnicodeWriter_Finish() documentation <https://docs.python.org/dev/c-api/unicode.html#c.PyUnicodeWriter_Finish>`__.

.. c:function:: void PyUnicodeWriter_Discard(PyUnicodeWriter *writer)

   See `PyUnicodeWriter_Discard() documentation <https://docs.python.org/dev/c-api/unicode.html#c.PyUnicodeWriter_Discard>`__.

.. c:function:: int PyUnicodeWriter_WriteChar(PyUnicodeWriter *writer, Py_UCS4 ch)

   See `PyUnicodeWriter_WriteChar() documentation <https://docs.python.org/dev/c-api/unicode.html#c.PyUnicodeWriter_WriteChar>`__.

.. c:function:: int PyUnicodeWriter_WriteUTF8(PyUnicodeWriter *writer, const char *str, Py_ssize_t size)

   See `PyUnicodeWriter_WriteUTF8() documentation <https://docs.python.org/dev/c-api/unicode.html#c.PyUnicodeWriter_WriteUTF8>`__.

.. c:function:: int PyUnicodeWriter_WriteASCII(PyUnicodeWriter *writer, const char *str, Py_ssize_t size)

   See `PyUnicodeWriter_WriteASCII() documentation <https://docs.python.org/dev/c-api/unicode.html#c.PyUnicodeWriter_WriteASCII>`__.

.. c:function:: int PyUnicodeWriter_WriteWideChar(PyUnicodeWriter *writer, const wchar_t *str, Py_ssize_t size)

   See `PyUnicodeWriter_WriteWideChar() documentation <https://docs.python.org/dev/c-api/unicode.html#c.PyUnicodeWriter_WriteWideChar>`__.

.. c:function:: int PyUnicodeWriter_WriteStr(PyUnicodeWriter *writer, PyObject *obj)

   See `PyUnicodeWriter_WriteStr() documentation <https://docs.python.org/dev/c-api/unicode.html#c.PyUnicodeWriter_WriteStr>`__.

.. c:function:: int PyUnicodeWriter_WriteRepr(PyUnicodeWriter *writer, PyObject *obj)

   See `PyUnicodeWriter_WriteRepr() documentation <https://docs.python.org/dev/c-api/unicode.html#c.PyUnicodeWriter_WriteRepr>`__.

.. c:function:: int PyUnicodeWriter_WriteSubstring(PyUnicodeWriter *writer, PyObject *str, Py_ssize_t start, Py_ssize_t end)

   See `PyUnicodeWriter_WriteSubstring() documentation <https://docs.python.org/dev/c-api/unicode.html#c.PyUnicodeWriter_WriteSubstring>`__.

.. c:function:: int PyUnicodeWriter_Format(PyUnicodeWriter *writer, const char *format, ...)

   See `PyUnicodeWriter_Format() documentation <https://docs.python.org/dev/c-api/unicode.html#c.PyUnicodeWriter_Format>`__.

.. c:function:: int PyLong_AsInt32(PyObject *obj, int32_t *pvalue)

   See `PyLong_AsInt32() documentation <https://docs.python.org/dev/c-api/long.html#c.PyLong_AsInt32>`__.

.. c:function:: int PyLong_AsInt64(PyObject *obj, int64_t *pvalue)

   See `PyLong_AsInt64() documentation <https://docs.python.org/dev/c-api/long.html#c.PyLong_AsInt64>`__.

.. c:function:: int PyLong_AsUInt32(PyObject *obj, uint32_t *pvalue)

   See `PyLong_AsUInt32() documentation <https://docs.python.org/dev/c-api/long.html#c.PyLong_AsUInt32>`__.

.. c:function:: int PyLong_AsUInt64(PyObject *obj, uint64_t *pvalue)

   See `PyLong_AsUInt64() documentation <https://docs.python.org/dev/c-api/long.html#c.PyLong_AsUInt64>`__.

.. c:function:: PyObject* PyLong_FromInt32(int32_t value)

   See `PyLong_FromInt32() documentation <https://docs.python.org/dev/c-api/long.html#c.PyLong_FromInt32>`__.

.. c:function:: PyObject* PyLong_FromInt64(int64_t value)

   See `PyLong_FromInt64() documentation <https://docs.python.org/dev/c-api/long.html#c.PyLong_FromInt64>`__.

.. c:function:: PyObject* PyLong_FromUInt32(uint32_t value)

   See `PyLong_FromUInt32() documentation <https://docs.python.org/dev/c-api/long.html#c.PyLong_FromUInt32>`__.

.. c:function:: PyObject* PyLong_FromUInt64(uint64_t value)

   See `PyLong_FromUInt64() documentation <https://docs.python.org/dev/c-api/long.html#c.PyLong_FromUInt64>`__.

.. c:function:: FILE* Py_fopen(PyObject *path, const char *mode)

   See `Py_fopen() documentation <https://docs.python.org/dev/c-api/sys.html#c.Py_fopen>`__.

.. c:function:: int Py_fclose(FILE *file)

   See `Py_fclose() documentation <https://docs.python.org/dev/c-api/sys.html#c.Py_fclose>`__.

.. c:function:: PyObject* PyConfig_Get(const char *name)

   See `PyConfig_Get() documentation <https://docs.python.org/dev/c-api/init_config.html#c.PyConfig_Get>`__.

.. c:function:: int PyConfig_GetInt(const char *name, int *value)

   See `PyConfig_GetInt() documentation <https://docs.python.org/dev/c-api/init_config.html#c.PyConfig_GetInt>`__.


Not supported:

* ``PyConfig_Names()``
* ``PyConfig_Set()``
* ``PyInitConfig_AddModule()``
* ``PyInitConfig_Create()``
* ``PyInitConfig_Free()``
* ``PyInitConfig_FreeStrList()``
* ``PyInitConfig_GetError()``
* ``PyInitConfig_GetExitCode()``
* ``PyInitConfig_GetInt()``
* ``PyInitConfig_GetStr()``
* ``PyInitConfig_GetStrList()``
* ``PyInitConfig_HasOption()``
* ``PyInitConfig_SetInt()``
* ``PyInitConfig_SetStr()``
* ``PyInitConfig_SetStrList()``
* ``PyType_GetBaseByToken()``
* ``PyUnicodeWriter_DecodeUTF8Stateful()``
* ``Py_InitializeFromInitConfig()``


Python 3.13
-----------

.. c:function:: int PyDict_GetItemRef(PyObject *p, PyObject *key, PyObject **result)

   See `PyDict_GetItemRef() documentation <https://docs.python.org/dev/c-api/dict.html#c.PyDict_GetItemRef>`__.

.. c:function:: int PyDict_GetItemStringRef(PyObject *p, const char *key, PyObject **result)

   See `PyDict_GetItemStringRef() documentation <https://docs.python.org/dev/c-api/dict.html#c.PyDict_GetItemStringRef>`__.

.. c:function:: PyObject* PyImport_AddModuleRef(const char *name)

   See `PyImport_AddModuleRef() documentation <https://docs.python.org/dev/c-api/import.html#c.PyImport_AddModuleRef>`__.

.. c:function:: int PyObject_GetOptionalAttr(PyObject *obj, PyObject *attr_name, PyObject **result)

   See `PyObject_GetOptionalAttr() documentation <https://docs.python.org/dev/c-api/object.html#c.PyObject_GetOptionalAttr>`__.

.. c:function:: int PyObject_GetOptionalAttrString(PyObject *obj, const char *attr_name, PyObject **result)

   See `PyObject_GetOptionalAttrString() documentation <https://docs.python.org/dev/c-api/object.html#c.PyObject_GetOptionalAttrString>`__.

.. c:function:: int PyObject_HasAttrWithError(PyObject *obj, PyObject *attr_name)

   See `PyObject_HasAttrWithError() documentation <https://docs.python.org/dev/c-api/object.html#c.PyObject_HasAttrWithError>`__.

.. c:function:: int PyObject_HasAttrStringWithError(PyObject *obj, const char *attr_name)

   See `PyObject_HasAttrStringWithError() documentation <https://docs.python.org/dev/c-api/object.html#c.PyObject_HasAttrStringWithError>`__.

.. c:function:: int PyMapping_GetOptionalItem(PyObject *obj, PyObject *key, PyObject **result)

   See `PyMapping_GetOptionalItem() documentation <https://docs.python.org/dev/c-api/mapping.html#c.PyMapping_GetOptionalItem>`__.

.. c:function:: int PyMapping_GetOptionalItemString(PyObject *obj, const char *key, PyObject **result)

   See `PyMapping_GetOptionalItemString() documentation <https://docs.python.org/dev/c-api/mapping.html#c.PyMapping_GetOptionalItemString>`__.

.. c:function:: int PyMapping_HasKeyWithError(PyObject *obj, PyObject *key)

   See `PyMapping_HasKeyWithError() documentation <https://docs.python.org/dev/c-api/mapping.html#c.PyMapping_HasKeyWithError>`__.

.. c:function:: int PyMapping_HasKeyStringWithError(PyObject *obj, const char *key)

   See `PyMapping_HasKeyStringWithError() documentation <https://docs.python.org/dev/c-api/mapping.html#c.PyMapping_HasKeyStringWithError>`__.

.. c:function:: int PyModule_Add(PyObject *module, const char *name, PyObject *value)

   See `PyModule_Add() documentation <https://docs.python.org/dev/c-api/module.html#c.PyModule_Add>`__.

.. c:function:: int PyWeakref_GetRef(PyObject *ref, PyObject **pobj)

   See `PyWeakref_GetRef() documentation <https://docs.python.org/dev/c-api/weakref.html#c.PyWeakref_GetRef>`__.

.. c:function:: int Py_IsFinalizing()

   Return non-zero if the Python interpreter is shutting down, return 0
   otherwise.

   Availability: Python 3.3 and newer, PyPy 7.3 and newer.

   See `Py_IsFinalizing() documentation <https://docs.python.org/dev/c-api/init.html#c.Py_IsFinalizing>`__.

.. c:function:: int PyDict_ContainsString(PyObject *p, const char *key)

   See `PyDict_ContainsString() documentation <https://docs.python.org/dev/c-api/dict.html#c.PyDict_ContainsString>`__.

.. c:function:: int PyLong_AsInt(PyObject *obj)

   See `PyLong_AsInt() documentation <https://docs.python.org/dev/c-api/long.html#c.PyLong_AsInt>`__.

.. c:function:: int PyObject_VisitManagedDict(PyObject *obj, visitproc visit, void *arg)

   See `PyObject_VisitManagedDict() documentation <https://docs.python.org/dev/c-api/object.html#c.PyObject_VisitManagedDict>`__.

.. c:function:: void PyObject_ClearManagedDict(PyObject *obj)

   See `PyObject_ClearManagedDict() documentation <https://docs.python.org/dev/c-api/object.html#c.PyObject_ClearManagedDict>`__.

.. c:function:: PyThreadState* PyThreadState_GetUnchecked(void)

   See `PyThreadState_GetUnchecked() documentation <https://docs.python.org/dev/c-api/init.html#c.PyThreadState_GetUnchecked>`__.

   Available on Python 3.5.2 and newer.

.. c:function:: int PyUnicode_EqualToUTF8(PyObject *unicode, const char *str)

   See `PyUnicode_EqualToUTF8() documentation <https://docs.python.org/dev/c-api/unicode.html#c.PyUnicode_EqualToUTF8>`__.

.. c:function:: int PyUnicode_EqualToUTF8AndSize(PyObject *unicode, const char *str, Py_ssize_t size)

   See `PyUnicode_EqualToUTF8AndSize() documentation <https://docs.python.org/dev/c-api/unicode.html#c.PyUnicode_EqualToUTF8AndSize>`__.

.. c:function:: int PyList_Extend(PyObject *list, PyObject *iterable)

   See `PyList_Extend() documentation <https://docs.python.org/dev/c-api/list.html#c.PyList_Extend>`__.

.. c:function:: int PyList_Clear(PyObject *list)

   See `PyList_Clear() documentation <https://docs.python.org/dev/c-api/list.html#c.PyList_Clear>`__.

.. c:function:: int PyDict_Pop(PyObject *dict, PyObject *key, PyObject **result)

   See `PyDict_Pop() documentation <https://docs.python.org/dev/c-api/dict.html#c.PyDict_Pop>`__.

.. c:function:: int PyDict_PopString(PyObject *dict, const char *key, PyObject **result)

   See `PyDict_PopString() documentation <https://docs.python.org/dev/c-api/dict.html#c.PyDict_PopString>`__.

.. c:function:: Py_hash_t Py_HashPointer(const void *ptr)

   See `Py_HashPointer() documentation <https://docs.python.org/dev/c-api/hash.html#c.Py_HashPointer>`__.

.. c:type:: PyTime_t

   A timestamp or duration in nanoseconds, represented as a signed 64-bit
   integer.

.. c:var:: PyTime_t PyTime_MIN

   Minimum value of :c:type:`PyTime_t`.

.. c:var:: PyTime_t PyTime_MAX

   Maximum value of :c:type:`PyTime_t`.

.. c:function:: double PyTime_AsSecondsDouble(PyTime_t t)

   See `PyTime_AsSecondsDouble() documentation <https://docs.python.org/dev/c-api/time.html#c.PyTime_AsSecondsDouble>`__.

.. c:function:: int PyTime_Monotonic(PyTime_t *result)

   See `PyTime_Monotonic() documentation <https://docs.python.org/dev/c-api/time.html#c.PyTime_Monotonic>`__.

.. c:function:: int PyTime_Time(PyTime_t *result)

   See `PyTime_Time() documentation <https://docs.python.org/dev/c-api/time.html#c.PyTime_Time>`__.

.. c:function:: int PyTime_PerfCounter(PyTime_t *result)

   See `PyTime_PerfCounter() documentation <https://docs.python.org/dev/c-api/time.html#c.PyTime_PerfCounter>`__.

.. c:function:: PyObject* PyList_GetItemRef(PyObject *op, Py_ssize_t index)

   See `PyList_GetItemRef() documentation <https://docs.python.org/dev/c-api/list.html#c.PyList_GetItemRef>`__.

.. c:function:: int PyDict_SetDefaultRef(PyObject *d, PyObject *key, PyObject *default_value, PyObject **result)

   See `PyDict_SetDefaultRef() documentation <https://docs.python.org/dev/c-api/dict.html#c.PyDict_SetDefaultRef>`__.


Not supported:

* ``PyErr_FormatUnraisable()``.
* ``PyLong_AsNativeBytes()``
* ``PyLong_FromNativeBytes()``
* ``PyLong_FromUnsignedNativeBytes()``
* ``PyObject_GenericHash()``.
* ``PySys_Audit()``.
* ``PySys_AuditTuple()``.
* ``PyType_GetFullyQualifiedName()``
* ``PyType_GetModuleName()``

Python 3.12
-----------

.. c:function:: PyObject* PyFrame_GetVar(PyFrameObject *frame, PyObject *name)

   See `PyFrame_GetVar() documentation <https://docs.python.org/dev/c-api/frame.html#c.PyFrame_GetVar>`__.

   Not available on PyPy.

.. c:function:: PyObject* PyFrame_GetVarString(PyFrameObject *frame, const char *name)

   See `PyFrame_GetVarString() documentation <https://docs.python.org/dev/c-api/frame.html#c.PyFrame_GetVarString>`__.

   Not available on PyPy.

.. c:function:: PyObject* Py_GetConstant(unsigned int constant_id)

   See `Py_GetConstant() documentation <https://docs.python.org/dev/c-api/object.html#c.Py_GetConstant>`__.

.. c:function:: PyObject* Py_GetConstantBorrowed(unsigned int constant_id)

   See `Py_GetConstantBorrowed() documentation <https://docs.python.org/dev/c-api/object.html#c.Py_GetConstantBorrowed>`__.


Not supported:

* ``PyDict_AddWatcher()``, ``PyDict_Watch()``.
* ``PyCode_AddWatcher()``, ``PyCode_ClearWatcher()``.
* ``PyErr_GetRaisedException()``, ``PyErr_SetRaisedException()``.
* ``_PyErr_ChainExceptions1()``.
* ``PyErr_DisplayException()``.
* ``_Py_IsImmortal()``.
* ``Py_NewInterpreterFromConfig()``.
* ``PyException_GetArgs()``, ``PyException_SetArgs()``.
* ``PyEval_SetProfileAllThreads()``, ``PyEval_SetTraceAllThreads()``.
* ``PyFunction_SetVectorcall()``.
* ``PyType_FromMetaclass()``: implementation too big to be backported.
* ``PyVectorcall_Call()``.

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

Not supported:

* ``PyType_GetModuleByDef()``.
* ``PyType_GetName()``.
* ``PyType_GetQualName()``.
* ``Py_Version`` constant.
* ``PyErr_GetHandledException()``, ``PyErr_SetHandledException()``.
* ``PyFrame_GetGenerator()``.

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

Not supported:

* ``PyCodec_Unregister()``.
* ``PyDateTime_DATE_GET_TZINFO()``, ``PyDateTime_TIME_GET_TZINFO()``.
* ``PyErr_SetInterruptEx()``.
* ``PyGC_Enable()``, ``PyGC_Disable()`` and ``PyGC_IsEnabled()``.
* ``PyIter_Send()``.
* ``PySet_CheckExact()``.
* ``Py_TPFLAGS_DISALLOW_INSTANTIATION`` constant.
* ``Py_TPFLAGS_IMMUTABLETYPE`` constant.

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

.. c:function:: PyObject* PyObject_Vectorcall(PyObject *callable, PyObject *const *args, size_t nargsf, PyObject *kwnames)

   See `PyObject_Vectorcall() documentation <https://docs.python.org/dev/c-api/call.html#c.PyObject_Vectorcall>`__.

.. c:function:: Py_ssize_t PyVectorcall_NARGS(size_t nargsf)

   See `PyVectorcall_NARGS() documentation <https://docs.python.org/dev/c-api/call.html#c.PyVectorcall_NARGS>`__.

.. c:macro:: PY_VECTORCALL_ARGUMENTS_OFFSET

   See `PY_VECTORCALL_ARGUMENTS_OFFSET documentation <https://docs.python.org/dev/c-api/call.html#PY_VECTORCALL_ARGUMENTS_OFFSET>`__.

Not supported:

* ``PyVectorcall_CallMethod()``.
* ``PyType_FromModuleAndSpec()``



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

Python 3.8
----------

Not supported:

* ``PyCode_NewWithPosOnlyArgs()``.

Python 3.7
----------

Not supported:

* ``PyImport_GetModule()``.
* ``PyInterpreterState_GetID()``.
* ``PySlice_Unpack()``, ``PySlice_AdjustIndices()``.
* ``PyTimeZone_FromOffset()``, ``PyTimeZone_FromOffsetAndName()``.
* ``Py_RETURN_RICHCOMPARE()``.
* ``Py_UNREACHABLE`` macro.

Python 3.6
----------

Not supported:

* ``PyErr_ResourceWarning()``.
* ``PyErr_SetImportErrorSubclass()``.
* ``PyOS_FSPath()``.
* ``Py_FinalizeEx()``.

Python 3.5.2
------------

.. c:macro:: Py_SETREF(op, op2)

.. c:macro:: Py_XSETREF(op, op2)

Not supported:

* ``PyCodec_NameReplaceErrors()``.
* ``PyErr_FormatV()``.
* ``PyExc_RecursionError``.
* ``PyModule_FromDefAndSpec()``, ``PyModule_FromDefAndSpec2()``,
  and ``PyModule_ExecDef()``.
* ``PyNumber_MatrixMultiply()`` and ``PyNumber_InPlaceMatrixMultiply()``.

Python 3.4
----------

.. c:macro:: Py_UNUSED(name)

   See `Py_UNUSED() documentation <https://docs.python.org/dev/c-api/intro.html#c.Py_UNUSED>`__.

Python 3.2
----------

Not supported:

* ``Py_VA_COPY``.
* ``PySys_SetArgvEx()``.
* ``PyLong_AsLongLongAndOverflow()``.
* ``PyErr_NewExceptionWithDoc()``.

Python 3.1
----------

Not supported:

* ``PyOS_string_to_double()``.
* ``PyCapsule`` API.

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
