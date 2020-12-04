// Always enable assertions
#undef NDEBUG

#include "pythoncapi_compat.h"

static PyObject*
ASSERT_FAILED(const char *err_msg)
{
    PyErr_SetString(PyExc_AssertionError, err_msg);
    return NULL;
}

static PyObject *
test_object(PyObject *self, PyObject *ignored)
{
    PyObject *obj = PyList_New(0);
    if (obj == NULL) {
        return NULL;
    }
    Py_ssize_t refcnt = Py_REFCNT(obj);

    // Py_NewRef() and Py_XNewRef()
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

    // test Py_SET_REFCNT
    Py_SET_REFCNT(obj, Py_REFCNT(obj));
    // test Py_SET_TYPE
    Py_SET_TYPE(obj, Py_TYPE(obj));
    // test Py_SET_SIZE
    Py_SET_SIZE(obj, Py_SIZE(obj));
    // test Py_IS_TYPE()
    int is_type = Py_IS_TYPE(obj, Py_TYPE(obj));
    assert(is_type);

    assert(Py_REFCNT(obj) == refcnt);
    Py_DECREF(obj);
    Py_RETURN_NONE;
}


static PyObject *
test_frame(PyObject *self, PyObject *ignored)
{
    PyThreadState *tstate = PyThreadState_Get();

    // test PyThreadState_GetFrame()
    PyFrameObject *frame = PyThreadState_GetFrame(tstate);
    if (frame == NULL) {
        return ASSERT_FAILED("PyThreadState_GetFrame failed");
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


static PyObject *
test_thread_state(PyObject *self, PyObject *ignored)
{
    PyThreadState *tstate = PyThreadState_Get();

    // test PyThreadState_GetInterpreter()
    PyInterpreterState *interp = PyThreadState_GetInterpreter(tstate);
    assert(interp != NULL);

    // test PyThreadState_GetFrame()
    PyFrameObject *frame = PyThreadState_GetFrame(tstate);
    if (frame != NULL) {
        assert(PyFrame_Check(frame));
    }
    Py_XDECREF(frame);

#if 0x030700A1 <= PY_VERSION_HEX
    uint64_t id = PyThreadState_GetID(tstate);
    assert(id > 0);
#endif

    Py_RETURN_NONE;
}


static PyObject *
test_interpreter(PyObject *self, PyObject *ignored)
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
test_calls(PyObject *self, PyObject *ignored)
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
test_gc(PyObject *self, PyObject *ignored)
{
    PyObject *tuple = PyTuple_New(1);
    Py_INCREF(Py_None);
    PyTuple_SET_ITEM(tuple, 0, Py_None);

    // test PyObject_GC_IsTracked()
    int tracked = PyObject_GC_IsTracked(tuple);
    assert(tracked);

#if PY_VERSION_HEX >= 0x030400F0
    // test PyObject_GC_IsFinalized()
    int finalized = PyObject_GC_IsFinalized(tuple);
    assert(!finalized);
#endif

    Py_DECREF(tuple);
    Py_RETURN_NONE;
}


static PyObject *
test_module(PyObject *self, PyObject *ignored)
{
    PyObject *module = self;
    assert(PyModule_Check(module));

    // test PyModule_AddType()
    PyTypeObject *type = &PyUnicode_Type;
    Py_ssize_t refcnt = Py_REFCNT(type);

    if (PyModule_AddType(module, type) < 0) {
        return NULL;
    }
    assert(Py_REFCNT(type) == refcnt + 1);

    PyObject *attr = PyObject_GetAttrString(module, "str");
    if (attr == NULL) {
        return NULL;
    }
    assert(attr == (PyObject *)type);
    Py_DECREF(attr);

    if (PyObject_DelAttrString(module, "str") < 0) {
        return NULL;
    }
    assert(Py_REFCNT(type) == refcnt);

    Py_RETURN_NONE;
}


static struct PyMethodDef methods[] = {
    {"test_object", test_object, METH_NOARGS},
    {"test_frame", test_frame, METH_NOARGS},
    {"test_thread_state", test_thread_state, METH_NOARGS},
    {"test_interpreter", test_interpreter, METH_NOARGS},
    {"test_calls", test_calls, METH_NOARGS},
    {"test_gc", test_gc, METH_NOARGS},
    {"test_module", test_module, METH_NOARGS},
    {NULL, NULL}
};


static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    .m_name = "test_pythoncapi_compat_cext",
    .m_methods = methods,
};


PyMODINIT_FUNC
PyInit_test_pythoncapi_compat_cext(void)
{
    return PyModuleDef_Init(&module);
}
