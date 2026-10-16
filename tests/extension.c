// C extension made of two C files (extension.c and static_inline.c) to detect
// when a pythoncapi_compat.h function is implemented without "static inline".

#ifndef MODULE_NAME
#   error "MODULE_NAME macro is not set"
#endif

#include "pythoncapi_compat.h"

#define _STR(NAME) #NAME
#define STR(NAME) _STR(NAME)
#define _CONCAT(a, b) a ## b
#define CONCAT(a, b) _CONCAT(a, b)


// No method and no module exec method needed, most basic C extension


// Use PySlot API on Python 3.15 and newer and on limited C API 3.15 and newer
#if (PY_VERSION_HEX >= _Py_PACK_VERSION(3, 15) \
     && (!defined(Py_LIMITED_API) || Py_LIMITED_API+0 >= _Py_PACK_VERSION(3, 15)))

PyABIInfo_VAR(abi_info);

static PySlot module_slots[] = {
    PySlot_PTR_STATIC(Py_mod_abi, &abi_info),
    PySlot_PTR_STATIC(Py_mod_name, (void*)STR(MODULE_NAME)),
    PySlot_PTR_STATIC(Py_mod_state_size, 0),
    PySlot_PTR_STATIC(Py_mod_gil, Py_MOD_GIL_NOT_USED),
    {0, 0, {0}, {0}}
};

#define EXPORT_FUNC CONCAT(PyModExport_, MODULE_NAME)

PyMODEXPORT_FUNC
EXPORT_FUNC(void)
{
    return module_slots;
}

#ifdef MS_WINDOWS
#   define INIT_FUNC CONCAT(PyInit_, MODULE_NAME)

// Workaround for https://github.com/pypa/distutils/issues/387
// https://docs.python.org/3.16/howto/abi3t-migration.html#module-export-hook
PyMODINIT_FUNC
INIT_FUNC(void)
{
    PyErr_SetString(PyExc_SystemError,
                    "PyInit_* called for module with PyModExport_*");
    return NULL;
}
#endif

#else

static struct PyModuleDef module_def = {
    PyModuleDef_HEAD_INIT,
    STR(MODULE_NAME),    // m_name
    _Py_NULL,            // m_doc
    0,                   // m_size
    _Py_NULL,            // m_methods
    _Py_NULL,            // m_slots
    _Py_NULL,            // m_traverse
    _Py_NULL,            // m_clear
    _Py_NULL,            // m_free
};


#define INIT_FUNC CONCAT(PyInit_, MODULE_NAME)

PyMODINIT_FUNC
INIT_FUNC(void)
{
    return PyModule_Create(&module_def);
}
#endif
