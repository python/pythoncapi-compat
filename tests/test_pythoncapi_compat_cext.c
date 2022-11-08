// Always enable assertions
#undef NDEBUG

#include "pythoncapi_compat.h"

#ifdef NDEBUG
#  error "assertions must be enabled"
#endif

#ifdef Py_LIMITED_API
#  error "Py_LIMITED_API is not supported"
#endif

#if PY_VERSION_HEX >= 0x03000000
#  define PYTHON3 1
#endif

#if defined(_MSC_VER) && defined(__cplusplus)
#  define MODULE_NAME test_pythoncapi_compat_cppext
#elif defined(__cplusplus) && __cplusplus >= 201103
#  define MODULE_NAME test_pythoncapi_compat_cpp11ext
#elif defined(__cplusplus)
#  define MODULE_NAME test_pythoncapi_compat_cpp03ext
#else
#  define MODULE_NAME test_pythoncapi_compat_cext
#endif

#define _STR(NAME) #NAME
#define STR(NAME) _STR(NAME)
#define _CONCAT(a, b) a ## b
#define CONCAT(a, b) _CONCAT(a, b)

#define MODULE_NAME_STR STR(MODULE_NAME)

// Ignore reference count checks on PyPy
#if !defined(PYPY_VERSION)
#  define CHECK_REFCNT
#endif

#ifdef CHECK_REFCNT
#  define ASSERT_REFCNT(expr) assert(expr)
#else
#  define ASSERT_REFCNT(expr)
#endif

static PyObject *
test_object(PyObject *Py_UNUSED(module), PyObject* Py_UNUSED(ignored))
{
    PyObject *obj = PyList_New(0);
    if (obj == _Py_NULL) {
        return _Py_NULL;
    }
    Py_ssize_t refcnt = Py_REFCNT(obj);

    // Py_NewRef()
    PyObject *ref = Py_NewRef(obj);
    assert(ref == obj);
    assert(Py_REFCNT(obj) == (refcnt + 1));
    Py_DECREF(ref);

    // Py_XNewRef()
    PyObject *xref = Py_XNewRef(obj);
    assert(xref == obj);
    assert(Py_REFCNT(obj) == (refcnt + 1));
    Py_DECREF(xref);

    assert(Py_XNewRef(_Py_NULL) == _Py_NULL);

    // Py_SETREF()
    PyObject *setref = Py_NewRef(obj);
    PyObject *none = Py_None;
    assert(Py_REFCNT(obj) == (refcnt + 1));

    Py_SETREF(setref, none);
    assert(setref == none);
    assert(Py_REFCNT(obj) == refcnt);
    Py_INCREF(setref);

    Py_SETREF(setref, _Py_NULL);
    assert(setref == _Py_NULL);

    // Py_XSETREF()
    PyObject *xsetref = _Py_NULL;

    Py_INCREF(obj);
    assert(Py_REFCNT(obj) == (refcnt + 1));
    Py_XSETREF(xsetref, obj);
    assert(xsetref == obj);

    Py_XSETREF(xsetref, _Py_NULL);
    assert(Py_REFCNT(obj) == refcnt);
    assert(xsetref == _Py_NULL);

    // Py_SET_REFCNT
    Py_SET_REFCNT(obj, Py_REFCNT(obj));
    // Py_SET_TYPE
    Py_SET_TYPE(obj, Py_TYPE(obj));
    // Py_SET_SIZE
    Py_SET_SIZE(obj, Py_SIZE(obj));
    // Py_IS_TYPE()
    int is_type = Py_IS_TYPE(obj, Py_TYPE(obj));
    assert(is_type);

    assert(Py_REFCNT(obj) == refcnt);
    Py_DECREF(obj);
    Py_RETURN_NONE;
}


static PyObject *
test_py_is(PyObject *Py_UNUSED(module), PyObject* Py_UNUSED(ignored))
{
    PyObject *o_none = Py_None;
    PyObject *o_true = Py_True;
    PyObject *o_false = Py_False;
    PyObject *obj = PyList_New(0);
    if (obj == _Py_NULL) {
        return _Py_NULL;
    }

    /* test Py_Is() */
    assert(Py_Is(obj, obj));
    assert(!Py_Is(obj, o_none));

    /* test Py_IsNone() */
    assert(Py_IsNone(o_none));
    assert(!Py_IsNone(obj));

    /* test Py_IsTrue() */
    assert(Py_IsTrue(o_true));
    assert(!Py_IsTrue(o_false));
    assert(!Py_IsTrue(obj));

    /* testPy_IsFalse() */
    assert(Py_IsFalse(o_false));
    assert(!Py_IsFalse(o_true));
    assert(!Py_IsFalse(obj));

    Py_DECREF(obj);
    Py_RETURN_NONE;
}


#if !defined(PYPY_VERSION)
static void
test_frame_getvar(PyFrameObject *frame)
{
    // Make the assumption that test_frame_getvar() is only called by
    // _run_tests() of test_pythoncapi_compat.py and so that the "name"
    // variable exists.

    // test PyFrame_GetVar() and PyFrame_GetVarString()
    PyObject *attr = PyUnicode_FromString("name");
    assert(attr != NULL);
    PyObject *name1 = PyFrame_GetVar(frame, attr);
    Py_DECREF(attr);
    assert(name1 != NULL);
    Py_DECREF(name1);

    PyObject *name2 = PyFrame_GetVarString(frame, "name");
    assert(name2 != NULL);
    Py_DECREF(name2);

    // test PyFrame_GetVar() and PyFrame_GetVarString() NameError
    PyObject *attr3 = PyUnicode_FromString("dontexist");
    assert(attr3 != NULL);
    PyObject *name3 = PyFrame_GetVar(frame, attr3);
    Py_DECREF(attr3);
    assert(name3 == NULL);
    assert(PyErr_ExceptionMatches(PyExc_NameError));
    PyErr_Clear();

    PyObject *name4 = PyFrame_GetVarString(frame, "dontexist");
    assert(name4 == NULL);
    assert(PyErr_ExceptionMatches(PyExc_NameError));
    PyErr_Clear();
}


static PyObject *
test_frame(PyObject *Py_UNUSED(module), PyObject* Py_UNUSED(ignored))
{
    PyThreadState *tstate = PyThreadState_Get();

    // test PyThreadState_GetFrame()
    PyFrameObject *frame = PyThreadState_GetFrame(tstate);
    if (frame == _Py_NULL) {
        PyErr_SetString(PyExc_AssertionError, "PyThreadState_GetFrame failed");
        return _Py_NULL;
    }

    // test _PyThreadState_GetFrameBorrow()
    Py_ssize_t frame_refcnt = Py_REFCNT(frame);
    PyFrameObject *frame2 = _PyThreadState_GetFrameBorrow(tstate);
    assert(frame2 == frame);
    assert(Py_REFCNT(frame) == frame_refcnt);

    // test PyFrame_GetCode()
    PyCodeObject *code = PyFrame_GetCode(frame);
    assert(code != _Py_NULL);
    assert(PyCode_Check(code));

    // test _PyFrame_GetCodeBorrow()
    Py_ssize_t code_refcnt = Py_REFCNT(code);
    PyCodeObject *code2 = _PyFrame_GetCodeBorrow(frame);
    assert(code2 == code);
    assert(Py_REFCNT(code) == code_refcnt);
    Py_DECREF(code);

    // PyFrame_GetBack()
    PyFrameObject* back = PyFrame_GetBack(frame);
    if (back != _Py_NULL) {
        assert(PyFrame_Check(back));
    }

    // test _PyFrame_GetBackBorrow()
    if (back != _Py_NULL) {
        Py_ssize_t back_refcnt = Py_REFCNT(back);
        PyFrameObject *back2 = _PyFrame_GetBackBorrow(frame);
        assert(back2 == back);
        assert(Py_REFCNT(back) == back_refcnt);
    }
    else {
        PyFrameObject *back2 = _PyFrame_GetBackBorrow(frame);
        assert(back2 == back);
    }
    Py_XDECREF(back);

    // test PyFrame_GetLocals()
    PyObject *locals = PyFrame_GetLocals(frame);
    assert(locals != _Py_NULL);
    assert(PyDict_Check(locals));

    // test PyFrame_GetGlobals()
    PyObject *globals = PyFrame_GetGlobals(frame);
    assert(globals != _Py_NULL);
    assert(PyDict_Check(globals));

    // test PyFrame_GetBuiltins()
    PyObject *builtins = PyFrame_GetBuiltins(frame);
    assert(builtins != _Py_NULL);
    assert(PyDict_Check(builtins));

    assert(locals != globals);
    assert(globals != builtins);
    assert(builtins != locals);

    Py_DECREF(locals);
    Py_DECREF(globals);
    Py_DECREF(builtins);

    // test PyFrame_GetLasti()
    int lasti = PyFrame_GetLasti(frame);
    assert(lasti >= 0);

    // test PyFrame_GetVar() and PyFrame_GetVarString()
    test_frame_getvar(frame);

    // done
    Py_DECREF(frame);
    Py_RETURN_NONE;
}
#endif


static PyObject *
test_thread_state(PyObject *Py_UNUSED(module), PyObject* Py_UNUSED(ignored))
{
    PyThreadState *tstate = PyThreadState_Get();

    // test PyThreadState_GetInterpreter()
    PyInterpreterState *interp = PyThreadState_GetInterpreter(tstate);
    assert(interp != _Py_NULL);

#if !defined(PYPY_VERSION)
    // test PyThreadState_GetFrame()
    PyFrameObject *frame = PyThreadState_GetFrame(tstate);
    if (frame != _Py_NULL) {
        assert(PyFrame_Check(frame));
    }
    Py_XDECREF(frame);
#endif

#if 0x030700A1 <= PY_VERSION_HEX && !defined(PYPY_VERSION)
    uint64_t id = PyThreadState_GetID(tstate);
    assert(id > 0);
#endif

#if !defined(PYPY_VERSION)
    // PyThreadState_EnterTracing(), PyThreadState_LeaveTracing()
    PyThreadState_EnterTracing(tstate);
    PyThreadState_LeaveTracing(tstate);
#endif

    Py_RETURN_NONE;
}


static PyObject *
test_interpreter(PyObject *Py_UNUSED(module), PyObject* Py_UNUSED(ignored))
{
    // test PyInterpreterState_Get()
    PyInterpreterState *interp = PyInterpreterState_Get();
    assert(interp != _Py_NULL);
    PyThreadState *tstate = PyThreadState_Get();
    PyInterpreterState *interp2 = PyThreadState_GetInterpreter(tstate);
    assert(interp == interp2);

    Py_RETURN_NONE;
}


static PyObject *
test_calls(PyObject *Py_UNUSED(module), PyObject* Py_UNUSED(ignored))
{
    PyObject *func = _Py_CAST(PyObject*, &PyUnicode_Type);

    // test PyObject_CallNoArgs(): str() returns ''
    PyObject *res = PyObject_CallNoArgs(func);
    if (res == _Py_NULL) {
        return _Py_NULL;
    }
    assert(PyUnicode_Check(res));
    Py_DECREF(res);

    // test PyObject_CallOneArg(): str(1) returns '1'
    PyObject *arg = PyLong_FromLong(1);
    if (arg == _Py_NULL) {
        return _Py_NULL;
    }
    res = PyObject_CallOneArg(func, arg);
    Py_DECREF(arg);
    if (res == _Py_NULL) {
        return _Py_NULL;
    }
    assert(PyUnicode_Check(res));
    Py_DECREF(res);

    Py_RETURN_NONE;
}


static PyObject *
test_gc(PyObject *Py_UNUSED(module), PyObject* Py_UNUSED(ignored))
{
    PyObject *tuple = PyTuple_New(1);
    Py_INCREF(Py_None);
    PyTuple_SET_ITEM(tuple, 0, Py_None);

#if !defined(PYPY_VERSION)
    // test PyObject_GC_IsTracked()
    int tracked = PyObject_GC_IsTracked(tuple);
    assert(tracked);
#endif

#if PY_VERSION_HEX >= 0x030400F0 && !defined(PYPY_VERSION)
    // test PyObject_GC_IsFinalized()
    int finalized = PyObject_GC_IsFinalized(tuple);
    assert(!finalized);
#endif

    Py_DECREF(tuple);
    Py_RETURN_NONE;
}


// test PyModule_AddType()
static int
test_module_add_type(PyObject *module)
{
    PyTypeObject *type = &PyUnicode_Type;
#ifdef PYTHON3
    const char *type_name = "str";
#else
    const char *type_name = "unicode";
#endif
#ifdef CHECK_REFCNT
    Py_ssize_t refcnt = Py_REFCNT(type);
#endif

    if (PyModule_AddType(module, type) < 0) {
        return -1;
    }
    ASSERT_REFCNT(Py_REFCNT(type) == refcnt + 1);

    PyObject *attr = PyObject_GetAttrString(module, type_name);
    if (attr == _Py_NULL) {
        return -1;
    }
    assert(attr == _Py_CAST(PyObject*, type));
    Py_DECREF(attr);

    if (PyObject_DelAttrString(module, type_name) < 0) {
        return -1;
    }
    ASSERT_REFCNT(Py_REFCNT(type) == refcnt);
    return 0;
}


// test PyModule_AddObjectRef()
static int
test_module_addobjectref(PyObject *module)
{
    PyObject *obj = Py_True;
    const char *name = "test_module_addobjectref";
#ifdef CHECK_REFCNT
    Py_ssize_t refcnt = Py_REFCNT(obj);
#endif

    if (PyModule_AddObjectRef(module, name, obj) < 0) {
        ASSERT_REFCNT(Py_REFCNT(obj) == refcnt);
        return -1;
    }
    ASSERT_REFCNT(Py_REFCNT(obj) == refcnt + 1);

    if (PyObject_DelAttrString(module, name) < 0) {
        return -1;
    }
    ASSERT_REFCNT(Py_REFCNT(obj) == refcnt);

    // PyModule_AddObjectRef() with value=NULL must not crash
    int res = PyModule_AddObjectRef(module, name, _Py_NULL);
    assert(res < 0);
    PyErr_Clear();

    return 0;
}


static PyObject *
test_module(PyObject *Py_UNUSED(module), PyObject* Py_UNUSED(ignored))
{
    PyObject *module = PyImport_ImportModule("sys");
    if (module == _Py_NULL) {
        return _Py_NULL;
    }
    assert(PyModule_Check(module));

    if (test_module_add_type(module) < 0) {
        goto error;
    }

    if (test_module_addobjectref(module) < 0) {
        goto error;
    }

    Py_DECREF(module);
    Py_RETURN_NONE;

error:
    Py_DECREF(module);
    return _Py_NULL;
}


#if (PY_VERSION_HEX <= 0x030B00A1 || 0x030B00A7 <= PY_VERSION_HEX) && !defined(PYPY_VERSION)
static PyObject *
test_float_pack(PyObject *Py_UNUSED(module), PyObject* Py_UNUSED(ignored))
{
    const int big_endian = 0;
    const int little_endian = 1;
    char data[8];
    const double d = 1.5;

#if PY_VERSION_HEX >= 0x030600B1
#  define HAVE_FLOAT_PACK2
#endif

    // Test Pack (big endian)
#ifdef HAVE_FLOAT_PACK2
    assert(PyFloat_Pack2(d, data, big_endian) == 0);
    assert(memcmp(data, ">\x00", 2) == 0);
#endif

    assert(PyFloat_Pack4(d, data, big_endian) == 0);
    assert(memcmp(data, "?\xc0\x00\x00", 2) == 0);

    assert(PyFloat_Pack8(d, data, big_endian) == 0);
    assert(memcmp(data, "?\xf8\x00\x00\x00\x00\x00\x00", 2) == 0);

    // Test Pack (little endian)
#ifdef HAVE_FLOAT_PACK2
    assert(PyFloat_Pack2(d, data, little_endian) == 0);
    assert(memcmp(data, "\x00>", 2) == 0);
#endif

    assert(PyFloat_Pack4(d, data, little_endian) == 0);
    assert(memcmp(data, "\x00\x00\xc0?", 2) == 0);

    assert(PyFloat_Pack8(d, data, little_endian) == 0);
    assert(memcmp(data, "\x00\x00\x00\x00\x00\x00\xf8?", 2) == 0);

    // Test Unpack (big endian)
#ifdef HAVE_FLOAT_PACK2
    assert(PyFloat_Unpack2(">\x00", big_endian) == d);
#endif
    assert(PyFloat_Unpack4("?\xc0\x00\x00", big_endian) == d);
    assert(PyFloat_Unpack8("?\xf8\x00\x00\x00\x00\x00\x00", big_endian) == d);

    // Test Unpack (little endian)
#ifdef HAVE_FLOAT_PACK2
    assert(PyFloat_Unpack2("\x00>", little_endian) == d);
#endif
    assert(PyFloat_Unpack4("\x00\x00\xc0?", little_endian) == d);
    assert(PyFloat_Unpack8("\x00\x00\x00\x00\x00\x00\xf8?", little_endian) == d);

    Py_RETURN_NONE;
}
#endif


#if !defined(PYPY_VERSION)
static PyObject *
test_code(PyObject *Py_UNUSED(module), PyObject* Py_UNUSED(ignored))
{
    PyThreadState *tstate = PyThreadState_Get();
    PyFrameObject *frame = PyThreadState_GetFrame(tstate);
    if (frame == _Py_NULL) {
        PyErr_SetString(PyExc_AssertionError, "PyThreadState_GetFrame failed");
        return _Py_NULL;
    }
    PyCodeObject *code = PyFrame_GetCode(frame);

    // PyCode_GetCode()
    {
        PyObject *co_code = PyCode_GetCode(code);
        assert(co_code != _Py_NULL);
        assert(PyBytes_Check(co_code));
        Py_DECREF(co_code);
    }

    // PyCode_GetVarnames
    {
        PyObject *co_varnames = PyCode_GetVarnames(code);
        assert(co_varnames != NULL);
        assert(PyTuple_CheckExact(co_varnames));
        assert(PyTuple_GET_SIZE(co_varnames) != 0);
        Py_DECREF(co_varnames);
    }

    // PyCode_GetCellvars
    {
        PyObject *co_cellvars = PyCode_GetCellvars(code);
        assert(co_cellvars != NULL);
        assert(PyTuple_CheckExact(co_cellvars));
        assert(PyTuple_GET_SIZE(co_cellvars) == 0);
        Py_DECREF(co_cellvars);
    }

    // PyCode_GetFreevars
    {
        PyObject *co_freevars = PyCode_GetFreevars(code);
        assert(co_freevars != NULL);
        assert(PyTuple_CheckExact(co_freevars));
        assert(PyTuple_GET_SIZE(co_freevars) == 0);
        Py_DECREF(co_freevars);
    }

    Py_DECREF(code);
    Py_DECREF(frame);
    Py_RETURN_NONE;
}
#endif


#ifdef __cplusplus
// Class to test operator casting an object to PyObject*
class StrongRef
{
public:
    StrongRef(PyObject *obj) : m_obj(obj) {
        Py_INCREF(this->m_obj);
    }

    ~StrongRef() {
        Py_DECREF(this->m_obj);
    }

    // Cast to PyObject*: get a borrowed reference
    inline operator PyObject*() const { return this->m_obj; }

private:
    PyObject *m_obj;  // Strong reference
};
#endif


static PyObject *
test_api_casts(PyObject *Py_UNUSED(module), PyObject *Py_UNUSED(args))
{
    PyObject *obj = Py_BuildValue("(ii)", 1, 2);
    if (obj == _Py_NULL) {
        return _Py_NULL;
    }
    Py_ssize_t refcnt = Py_REFCNT(obj);
    assert(refcnt >= 1);

    // gh-92138: For backward compatibility, functions of Python C API accepts
    // "const PyObject*". Check that using it does not emit C++ compiler
    // warnings.
    const PyObject *const_obj = obj;
    Py_INCREF(const_obj);
    Py_DECREF(const_obj);
    PyTypeObject *type = Py_TYPE(const_obj);
    assert(Py_REFCNT(const_obj) == refcnt);
    assert(type == &PyTuple_Type);
    assert(PyTuple_GET_SIZE(const_obj) == 2);
    PyObject *one = PyTuple_GET_ITEM(const_obj, 0);
    assert(PyLong_AsLong(one) == 1);

#ifdef __cplusplus
    // gh-92898: StrongRef doesn't inherit from PyObject but has an operator to
    // cast to PyObject*.
    StrongRef strong_ref(obj);
    assert(Py_TYPE(strong_ref) == &PyTuple_Type);
    assert(Py_REFCNT(strong_ref) == (refcnt + 1));
    Py_INCREF(strong_ref);
    Py_DECREF(strong_ref);
#endif

    // gh-93442: Pass 0 as NULL for PyObject*
    Py_XINCREF(0);
    Py_XDECREF(0);
#if _cplusplus >= 201103
    // Test nullptr passed as PyObject*
    Py_XINCREF(nullptr);
    Py_XDECREF(nullptr);
#endif

    Py_DECREF(obj);
    Py_RETURN_NONE;
}


static struct PyMethodDef methods[] = {
    {"test_object", test_object, METH_NOARGS, _Py_NULL},
    {"test_py_is", test_py_is, METH_NOARGS, _Py_NULL},
#if !defined(PYPY_VERSION)
    {"test_frame", test_frame, METH_NOARGS, _Py_NULL},
#endif
    {"test_thread_state", test_thread_state, METH_NOARGS, _Py_NULL},
    {"test_interpreter", test_interpreter, METH_NOARGS, _Py_NULL},
    {"test_calls", test_calls, METH_NOARGS, _Py_NULL},
    {"test_gc", test_gc, METH_NOARGS, _Py_NULL},
    {"test_module", test_module, METH_NOARGS, _Py_NULL},
#if (PY_VERSION_HEX <= 0x030B00A1 || 0x030B00A7 <= PY_VERSION_HEX) && !defined(PYPY_VERSION)
    {"test_float_pack", test_float_pack, METH_NOARGS, _Py_NULL},
#endif
#if !defined(PYPY_VERSION)
    {"test_code", test_code, METH_NOARGS, _Py_NULL},
#endif
    {"test_api_casts", test_api_casts, METH_NOARGS, _Py_NULL},
    {_Py_NULL, _Py_NULL, 0, _Py_NULL}
};


#ifdef __cplusplus
static int
module_exec(PyObject *module)
{
    if (PyModule_AddIntMacro(module, __cplusplus)) {
        return -1;
    }
    return 0;
}
#else
static int
module_exec(PyObject *Py_UNUSED(module))
{
    return 0;
}
#endif


#if PY_VERSION_HEX >= 0x03050000
static PyModuleDef_Slot module_slots[] = {
    {Py_mod_exec, _Py_CAST(void*, module_exec)},
    {0, _Py_NULL}
};
#endif


#ifdef PYTHON3
static struct PyModuleDef module_def = {
    PyModuleDef_HEAD_INIT,
    MODULE_NAME_STR,     // m_name
    _Py_NULL,            // m_doc
    0,                   // m_doc
    methods,             // m_methods
#if PY_VERSION_HEX >= 0x03050000
    module_slots,        // m_slots
#else
    _Py_NULL,            // m_reload
#endif
    _Py_NULL,            // m_traverse
    _Py_NULL,            // m_clear
    _Py_NULL,            // m_free
};


#define INIT_FUNC CONCAT(PyInit_, MODULE_NAME)

#if PY_VERSION_HEX >= 0x03050000
PyMODINIT_FUNC
INIT_FUNC(void)
{
    return PyModuleDef_Init(&module_def);
}
#else
// Python 3.4
PyMODINIT_FUNC
INIT_FUNC(void)
{
    PyObject *module = PyModule_Create(&module_def);
    if (module == NULL) {
        return NULL;
    }
    if (module_exec(module) < 0) {
        Py_DECREF(module);
        return NULL;
    }
    return module;
}
#endif

#else
// Python 2

#define INIT_FUNC CONCAT(init, MODULE_NAME)

PyMODINIT_FUNC
INIT_FUNC(void)
{
    PyObject *module;
    module = Py_InitModule4(MODULE_NAME_STR,
                            methods,
                            _Py_NULL,
                            _Py_NULL,
                            PYTHON_API_VERSION);
    if (module == NULL) {
        return;
    }

    if (module_exec(module) < 0) {
        return;
    }
}
#endif
