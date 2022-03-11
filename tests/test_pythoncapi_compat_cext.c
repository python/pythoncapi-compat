// Always enable assertions
#undef NDEBUG

#include "pythoncapi_compat.h"

#ifdef Py_LIMITED_API
#  error "Py_LIMITED_API is not supported"
#endif

#if PY_VERSION_HEX >= 0x03000000
#  define PYTHON3 1
#endif

#ifdef __cplusplus
#  define MODULE_NAME test_pythoncapi_compat_cppext
#  define MODULE_NAME_STR "test_pythoncapi_compat_cppext"
#else
#  define MODULE_NAME test_pythoncapi_compat_cext
#  define MODULE_NAME_STR "test_pythoncapi_compat_cext"
#endif

// Ignore reference count checks on PyPy
#if !defined(PYPY_VERSION)
#  define CHECK_REFCNT
#endif

#ifdef CHECK_REFCNT
#  define ASSERT_REFCNT(expr) assert(expr)
#else
#  define ASSERT_REFCNT(expr)
#endif

#define CONCAT(a, b) a ## b

static PyObject *
test_object(PyObject *Py_UNUSED(module), PyObject* Py_UNUSED(ignored))
{
    PyObject *obj = PyList_New(0);
    if (obj == NULL) {
        return NULL;
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

    assert(Py_XNewRef(NULL) == NULL);

    // Py_SETREF()
    PyObject *setref = Py_NewRef(obj);
    PyObject *none = Py_None;
    assert(Py_REFCNT(obj) == (refcnt + 1));

    Py_SETREF(setref, none);
    assert(setref == none);
    assert(Py_REFCNT(obj) == refcnt);
    Py_INCREF(setref);

    Py_SETREF(setref, NULL);
    assert(setref == NULL);

    // Py_XSETREF()
    PyObject *xsetref = NULL;

    Py_INCREF(obj);
    assert(Py_REFCNT(obj) == (refcnt + 1));
    Py_XSETREF(xsetref, obj);
    assert(xsetref == obj);

    Py_XSETREF(xsetref, NULL);
    assert(Py_REFCNT(obj) == refcnt);
    assert(xsetref == NULL);

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
    if (obj == NULL) {
        return NULL;
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


static PyObject *
test_steal_ref(PyObject *Py_UNUSED(module), PyObject* Py_UNUSED(ignored))
{
    PyObject *obj = PyList_New(0);
    if (obj == NULL) {
        return NULL;
    }
    Py_ssize_t refcnt = Py_REFCNT(obj);

    // _Py_StealRef()
    Py_INCREF(obj);
    PyObject *ref = _Py_StealRef(obj);
    assert(ref == obj);
    assert(Py_REFCNT(obj) == refcnt);

    // _Py_XStealRef()
    Py_INCREF(obj);
    PyObject *xref = _Py_XStealRef(obj);
    assert(xref == obj);
    assert(Py_REFCNT(obj) == refcnt);

    assert(_Py_XStealRef(NULL) == NULL);

    assert(Py_REFCNT(obj) == refcnt);
    Py_DECREF(obj);
    Py_RETURN_NONE;
}


#if !defined(PYPY_VERSION)
static PyObject *
test_frame(PyObject *Py_UNUSED(module), PyObject* Py_UNUSED(ignored))
{
    PyThreadState *tstate = PyThreadState_Get();

    // test PyThreadState_GetFrame()
    PyFrameObject *frame = PyThreadState_GetFrame(tstate);
    if (frame == NULL) {
        PyErr_SetString(PyExc_AssertionError, "PyThreadState_GetFrame failed");
        return NULL;
    }

    // test _PyThreadState_GetFrameBorrow()
    Py_ssize_t frame_refcnt = Py_REFCNT(frame);
    PyFrameObject *frame2 = _PyThreadState_GetFrameBorrow(tstate);
    assert(frame2 == frame);
    assert(Py_REFCNT(frame) == frame_refcnt);

    // test PyFrame_GetCode()
    PyCodeObject *code = PyFrame_GetCode(frame);
    assert(code != NULL);
    assert(PyCode_Check(code));

    // test _PyFrame_GetCodeBorrow()
    Py_ssize_t code_refcnt = Py_REFCNT(code);
    PyCodeObject *code2 = _PyFrame_GetCodeBorrow(frame);
    assert(code2 == code);
    assert(Py_REFCNT(code) == code_refcnt);
    Py_DECREF(code);

    // PyFrame_GetBack()
    PyFrameObject* back = PyFrame_GetBack(frame);
    if (back != NULL) {
        assert(PyFrame_Check(back));
    }

    // test _PyFrame_GetBackBorrow()
    if (back != NULL) {
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
    assert(interp != NULL);

#if !defined(PYPY_VERSION)
    // test PyThreadState_GetFrame()
    PyFrameObject *frame = PyThreadState_GetFrame(tstate);
    if (frame != NULL) {
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
    assert(interp != NULL);
    PyThreadState *tstate = PyThreadState_Get();
    PyInterpreterState *interp2 = PyThreadState_GetInterpreter(tstate);
    assert(interp == interp2);

    Py_RETURN_NONE;
}


static PyObject *
test_calls(PyObject *Py_UNUSED(module), PyObject* Py_UNUSED(ignored))
{
    PyObject *func = (PyObject *)&PyUnicode_Type;

    // test PyObject_CallNoArgs(): str() returns ''
    PyObject *res = PyObject_CallNoArgs(func);
    if (res == NULL) {
        return NULL;
    }
    assert(PyUnicode_Check(res));
    Py_DECREF(res);

    // test PyObject_CallOneArg(): str(1) returns '1'
    PyObject *arg = PyLong_FromLong(1);
    if (arg == NULL) {
        return NULL;
    }
    res = PyObject_CallOneArg(func, arg);
    Py_DECREF(arg);
    if (res == NULL) {
        return NULL;
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
    if (attr == NULL) {
        return -1;
    }
    assert(attr == (PyObject *)type);
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
    int res = PyModule_AddObjectRef(module, name, NULL);
    assert(res < 0);
    PyErr_Clear();

    return 0;
}


static PyObject *
test_module(PyObject *Py_UNUSED(module), PyObject* Py_UNUSED(ignored))
{
    PyObject *module = PyImport_ImportModule("sys");
    if (module == NULL) {
        return NULL;
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
    return NULL;
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


static struct PyMethodDef methods[] = {
    {"test_object", test_object, METH_NOARGS, NULL},
    {"test_py_is", test_py_is, METH_NOARGS, NULL},
    {"test_steal_ref", test_steal_ref, METH_NOARGS, NULL},
#if !defined(PYPY_VERSION)
    {"test_frame", test_frame, METH_NOARGS, NULL},
#endif
    {"test_thread_state", test_thread_state, METH_NOARGS, NULL},
    {"test_interpreter", test_interpreter, METH_NOARGS, NULL},
    {"test_calls", test_calls, METH_NOARGS, NULL},
    {"test_gc", test_gc, METH_NOARGS, NULL},
    {"test_module", test_module, METH_NOARGS, NULL},
#if (PY_VERSION_HEX <= 0x030B00A1 || 0x030B00A7 <= PY_VERSION_HEX) && !defined(PYPY_VERSION)
    {"test_float_pack", test_float_pack, METH_NOARGS, NULL},
#endif
    {NULL, NULL, 0, NULL}
};


#ifdef PYTHON3
static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    MODULE_NAME_STR,     // m_name
    PYCAPI_COMPAT_NULL,  // m_doc
    0,                   // m_doc
    methods,             // m_methods
#if PY_VERSION_HEX >= 0x03050000
    PYCAPI_COMPAT_NULL,  // m_slots
#else
    PYCAPI_COMPAT_NULL,  // m_reload
#endif
    PYCAPI_COMPAT_NULL,  // m_traverse
    PYCAPI_COMPAT_NULL,  // m_clear
    PYCAPI_COMPAT_NULL,  // m_free
};


#define _INIT_FUNC(name) CONCAT(PyInit_, name)
#define INIT_FUNC _INIT_FUNC(MODULE_NAME)

#if PY_VERSION_HEX >= 0x03050000
PyMODINIT_FUNC
INIT_FUNC(void)
{
    return PyModuleDef_Init(&module);
}
#else
// Python 3.4
PyMODINIT_FUNC
INIT_FUNC(void)
{
    return PyModule_Create(&module);
}
#endif

#else
// Python 2

#define _INIT_FUNC(name) CONCAT(init, name)
#define INIT_FUNC _INIT_FUNC(MODULE_NAME)

PyMODINIT_FUNC
INIT_FUNC(void)
{
    Py_InitModule4(MODULE_NAME_STR,
                   methods,
                   NULL,
                   NULL,
                   PYTHON_API_VERSION);
}
#endif
