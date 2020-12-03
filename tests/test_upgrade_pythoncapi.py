#!/usr/bin/env python3
import io
import os
import sys
import tempfile
import textwrap
import unittest

# Get upgrade_pythoncapi.py of the parent directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import upgrade_pythoncapi   # noqa


def patch(source):
    args = ['script', 'mod.c']
    patcher = upgrade_pythoncapi.Patcher(args)
    return patcher.patch(source)


def reformat(source):
    return textwrap.dedent(source).strip()


class Tests(unittest.TestCase):
    def _test_patch_file(self, tmp_dir):
        # test Patcher.patcher()
        source = """
            PyTypeObject*
            test_type(PyObject *obj, PyTypeObject *type)
            {
                Py_TYPE(obj) = type;
                return Py_TYPE(obj);
            }
        """
        expected = """
            #include "pythoncapi_compat.h"

            PyTypeObject*
            test_type(PyObject *obj, PyTypeObject *type)
            {
                Py_SET_TYPE(obj, type);
                return Py_TYPE(obj);
            }
        """
        source = reformat(source)
        expected = reformat(expected)

        filename = tempfile.mktemp(suffix='.c', dir=tmp_dir)
        old_filename = filename + ".old"
        try:
            with open(filename, "w", encoding="utf-8") as fp:
                fp.write(source)

            old_stderr = sys.stderr
            old_argv = list(sys.argv)
            try:
                # redirect stderr
                sys.stderr = io.StringIO()

                if tmp_dir is not None:
                    arg = tmp_dir
                else:
                    arg = filename
                sys.argv = ['script', arg]
                try:
                    upgrade_pythoncapi.Patcher().main()
                except SystemExit as exc:
                    self.assertEqual(exc.code, 0)
                else:
                    self.fail("SystemExit not raised")
            finally:
                sys.stderr = old_stderr
                sys.argv = old_argv

            with open(filename, encoding="utf-8") as fp:
                new_contents = fp.read()

            with open(old_filename, encoding="utf-8") as fp:
                old_contents = fp.read()
        finally:
            try:
                os.unlink(filename)
            except FileNotFoundError:
                pass
            try:
                os.unlink(old_filename)
            except FileNotFoundError:
                pass

        self.assertEqual(new_contents, expected)
        self.assertEqual(old_contents, source)

    def test_patch_file(self):
        self._test_patch_file(None)

    def test_patch_directory(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            self._test_patch_file(tmp_dir)

    def check_replace(self, source, expected):
        source = reformat(source)
        expected = reformat(expected)
        self.assertEqual(patch(source), expected)

    def check_dont_replace(self, source):
        source = reformat(source)
        self.assertEqual(patch(source), source)

    def test_expr_regex(self):
        self.check_replace("a->b->ob_type", "Py_TYPE(a->b)")
        self.check_replace("a.b->ob_type", "Py_TYPE(a.b)")
        self.check_replace("array[2]->ob_type", "Py_TYPE(array[2])")

        # Don't match function calls
        self.check_dont_replace("func()->ob_type")

    def test_pythoncapi_compat(self):
        # If pythoncapi_compat.h is included, avoid compatibility includes
        # and macros.
        #
        # Otherise, Py_SET_TYPE() requires a macro and PyFrame_GetBack()
        # requires 2 macros and an include.
        HEADERS = (
            '<pythoncapi_compat.h>',
            '"pythoncapi_compat.h"',
        )
        for header in HEADERS:
            # There is no empty line between the include and the function
            # on purpose.
            self.check_replace("""
                #include %s
                void test_set_type(PyObject *obj, PyTypeObject *type)
                {
                    Py_TYPE(obj) = type;
                }
                PyFrameObject* frame_back_borrowed(PyFrameObject *frame)
                {
                    return frame->f_back;
                }
            """ % header, """
                #include %s
                void test_set_type(PyObject *obj, PyTypeObject *type)
                {
                    Py_SET_TYPE(obj, type);
                }
                PyFrameObject* frame_back_borrowed(PyFrameObject *frame)
                {
                    return _PyFrame_GetBackBorrow(frame);
                }
            """ % header)

    def test_py_type(self):
        source = """
            PyTypeObject* get_type(PyObject *obj)
            { return obj->ob_type; }
        """
        expected = """
            PyTypeObject* get_type(PyObject *obj)
            { return Py_TYPE(obj); }
        """
        self.check_replace(source, expected)

    def test_py_size(self):
        source = """
            Py_ssize_t get_size(PyVarObject *obj)
            { return obj->ob_size; }
        """
        expected = """
            Py_ssize_t get_size(PyVarObject *obj)
            { return Py_SIZE(obj); }
        """
        self.check_replace(source, expected)

    def test_py_refcnt(self):
        source = """
            Py_ssize_t get_refcnt(PyObject *obj)
            { return obj->ob_refcnt; }
        """
        expected = """
            Py_ssize_t get_refcnt(PyObject *obj)
            { return Py_REFCNT(obj); }
        """
        self.check_replace(source, expected)

    def test_py_set_type(self):
        source = """
            void test_type(PyObject *obj, PyTypeObject *type)
            {
                obj->ob_type = type;
                Py_TYPE(obj) = type;
            }
        """
        expected = """
            #include "pythoncapi_compat.h"

            void test_type(PyObject *obj, PyTypeObject *type)
            {
                Py_SET_TYPE(obj, type);
                Py_SET_TYPE(obj, type);
            }
        """
        self.check_replace(source, expected)

        self.check_dont_replace("""
            PyTypeObject* get_type(PyObject *obj, PyTypeObject *check_type)
            {
                assert(Py_TYPE(args) == check_type);
                return Py_TYPE(obj);
            }
        """)

    def test_py_set_size(self):
        source = """\
            void test_size(PyVarObject *obj)
            {
                obj->ob_size = 3;
                Py_SIZE(obj) = 4;
            }
        """
        expected = """\
            #include "pythoncapi_compat.h"

            void test_size(PyVarObject *obj)
            {
                Py_SET_SIZE(obj, 3);
                Py_SET_SIZE(obj, 4);
            }
        """
        self.check_replace(source, expected)

        self.check_dont_replace("""
            Py_ssize_t
            get_size(PyObject *obj)
            {
                assert(Py_SIZE(args) == 1);
                return Py_SIZE(obj);
            }
        """)

    def test_py_set_refcnt(self):
        source = """\
            void set_refcnt(PyObject *obj)
            {
                obj->ob_refcnt = 1;
                Py_REFCNT(obj) = 2;
            }
        """
        expected = """\
            #include "pythoncapi_compat.h"

            void set_refcnt(PyObject *obj)
            {
                Py_SET_REFCNT(obj, 1);
                Py_SET_REFCNT(obj, 2);
            }
        """
        self.check_replace(source, expected)

        self.check_dont_replace("""
            Py_ssize_t
            get_refcnt(PyObject *obj)
            {
                assert(Py_REFCNT(args) == 1);
                return Py_REFCNT(obj);
            }
        """)

    def test_pyobject_new(self):
        source = """\
            capsule = PyObject_NEW(PyCapsule, &PyCapsule_Type);
            pattern = PyObject_NEW_VAR(PatternObject, Pattern_Type, n);
        """
        expected = """\
            capsule = PyObject_New(PyCapsule, &PyCapsule_Type);
            pattern = PyObject_NewVar(PatternObject, Pattern_Type, n);
        """
        self.check_replace(source, expected)

        self.check_dont_replace("""
            func = PyObject_NEW;
            capsule2 = PyObject_NEW2(PyCapsule, &PyCapsule_Type);

            func2 = PyObject_NEW_VAR;
            pattern2 = PyObject_NEW_VAR2(PatternObject, Pattern_Type, n);
        """)

    def test_pymem_malloc(self):
        source = """\
            void *ptr = PyMem_MALLOC(10);
            ptr = PyMem_REALLOC(ptr, 20);
            PyMem_FREE(ptr);
            PyMem_DEL(ptr);
            PyMem_Del(ptr);
        """
        expected = """\
            void *ptr = PyMem_Malloc(10);
            ptr = PyMem_Realloc(ptr, 20);
            PyMem_Free(ptr);
            PyMem_Free(ptr);
            PyMem_Free(ptr);
        """
        self.check_replace(source, expected)

    def test_pyobject_malloc(self):
        source = """\
            void *ptr = PyObject_MALLOC(10);
            ptr = PyObject_REALLOC(ptr, 20);
            PyObject_FREE(ptr);
            PyObject_DEL(ptr);
            PyObject_Del(ptr);
        """
        expected = """\
            void *ptr = PyObject_Malloc(10);
            ptr = PyObject_Realloc(ptr, 20);
            PyObject_Free(ptr);
            PyObject_Free(ptr);
            PyObject_Free(ptr);
        """
        self.check_replace(source, expected)

    def test_pyframe_getback(self):
        source = """\
            PyFrameObject* frame_back_borrowed(PyFrameObject *frame)
            {
                return frame->f_back;
            }
        """
        expected = """\
            #include "pythoncapi_compat.h"

            PyFrameObject* frame_back_borrowed(PyFrameObject *frame)
            {
                return _PyFrame_GetBackBorrow(frame);
            }
        """
        self.check_replace(source, expected)

    def test_pyframe_getcode(self):
        self.check_replace("""\
            PyCodeObject* frame_code_borrowed(PyFrameObject *frame)
            {
                return frame->f_code;
            }
        """, """\
            #include "pythoncapi_compat.h"

            PyCodeObject* frame_code_borrowed(PyFrameObject *frame)
            {
                return _PyFrame_GetCodeBorrow(frame);
            }
        """)

    def test_get_member_regex(self):
        # Use PyFrame_GetCode() to test get_member_regex()
        self.check_dont_replace("""
            void frame_set_code(PyFrameObject *frame, PyCodeObject *code)
            {
                frame->f_code = code;
            }

            void frame_clear_code(PyFrameObject *frame)
            {
                Py_CLEAR(frame->f_code);
            }
        """)

    def test_pythreadstate_getinterpreter(self):
        self.check_replace("""
            PyInterpreterState* get_interp(PyThreadState *tstate)
            { return tstate->interp; }
        """, """
            #include "pythoncapi_compat.h"

            PyInterpreterState* get_interp(PyThreadState *tstate)
            { return PyThreadState_GetInterpreter(tstate); }
        """)

    def test_pythreadstate_getframe(self):
        self.check_replace("""
            PyFrameObject* get_frame(PyThreadState *tstate)
            { return tstate->frame; }
        """, """
            #include "pythoncapi_compat.h"

            PyFrameObject* get_frame(PyThreadState *tstate)
            { return _PyThreadState_GetFrameBorrow(tstate); }
        """)

    @unittest.skipUnless(upgrade_pythoncapi.FORCE_NEWREF, 'FORCE_NEWREF=False')
    def test_py_incref_return(self):
        self.check_replace("""
            PyObject* new_ref(PyObject *obj)
            {
                Py_INCREF(obj);
                return obj;
            }
        """, """
            #include "pythoncapi_compat.h"

            PyObject* new_ref(PyObject *obj)
            {
                return Py_NewRef(obj);
            }
        """)

    @unittest.skipUnless(upgrade_pythoncapi.FORCE_NEWREF, 'FORCE_NEWREF=False')
    def test_py_incref_assign(self):
        self.check_replace("""
            void set_attr(MyStruct *obj, PyObject *value)
            {
                Py_INCREF(value);
                obj->attr = value;
            }
        """, """
            #include "pythoncapi_compat.h"

            void set_attr(MyStruct *obj, PyObject *value)
            {
                obj->attr = Py_NewRef(value);
            }
        """)


if __name__ == "__main__":
    unittest.main()
