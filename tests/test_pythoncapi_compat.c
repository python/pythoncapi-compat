#include "pythoncapi_compat.h"

static int
ASSERT_FAILED(const char *err_msg)
{
    PyErr_SetString(PyExc_AssertionError, err_msg);
    return -1;
}

static int
test_set_funcs(void)
{
    PyObject *obj = PyList_New(0);
    if (obj == NULL) {
        return -1;
    }
    Py_SET_REFCNT(obj, Py_REFCNT(obj));
    Py_SET_TYPE(obj, Py_TYPE(obj));
    Py_SET_SIZE(obj, Py_SIZE(obj));
    Py_DECREF(obj);
    return 0;
}


static int
test_frame(void)
{
    PyThreadState *tstate = PyThreadState_GET();
    PyFrameObject *frame = PyThreadState_GetFrame(tstate);
    if (frame == NULL) {
        return ASSERT_FAILED("PyThreadState_GetFrame failed");
    }

    PyCodeObject *code = PyFrame_GetCode(frame);
    assert(code != NULL);
    assert(PyCode_Check(code));
    Py_DECREF(code);

    Py_DECREF(frame);
    return 0;
}


static PyObject *
test_all(PyObject *self, PyObject *ignored)
{
    if (test_set_funcs() < 0) {
        return NULL;
    }
    if (test_frame() < 0) {
        return NULL;
    }

    Py_RETURN_NONE;
}


static struct PyMethodDef methods[] = {
    {"test_all", test_all, METH_NOARGS},
    {NULL,       NULL}          /* sentinel */
};


static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    .m_name = "test_pythoncapi_compat",
    .m_methods = methods,
};


PyMODINIT_FUNC
PyInit_test_pythoncapi_compat(void)
{
    return PyModuleDef_Init(&module);
}
