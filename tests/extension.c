// C extension made of two C files (extension.c and static_inline.c) to detect
// when a pythoncapi_compat.h function is implemented without "static inline".

#ifndef MODULE_NAME
#   error "MODULE_NAME macro is not set"
#endif

#include "pythoncapi_compat.h"

#define STR(NAME) #NAME
#define CONCAT(a, b) a ## b

// No method and no module exec method needed, most basic C extension

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
