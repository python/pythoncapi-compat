#!/usr/bin/env python3
import argparse
import os
import re
import sys


FORCE_NEWREF = False


PYTHONCAPI_COMPAT_URL = ('https://raw.githubusercontent.com/pythoncapi/'
                         'pythoncapi_compat/master/pythoncapi_compat.h')
PYTHONCAPI_COMPAT_H = 'pythoncapi_compat.h'
INCLUDE_PYTHONCAPI_COMPAT = f'#include "{PYTHONCAPI_COMPAT_H}"'
INCLUDE_PYTHONCAPI_COMPAT2 = f'#include <{PYTHONCAPI_COMPAT_H}>'


# Match a C identifier: 'identifier', 'var_3', 'NameCamelCase'
ID_REGEX = r'[a-zA-Z][a-zA-Z0-9_]*'
# Match 'array[3]'
SUBEXPR_REGEX = fr'{ID_REGEX}(?:\[[^]]+\])*'
# Match a C expression like "frame", "frame.attr" or "obj->attr".
# Don't match functions calls like "func()".
EXPR_REGEX = fr"{SUBEXPR_REGEX}(?:(?:->|\.){SUBEXPR_REGEX})*"


def get_member_regex_str(member):
    # Match "var->member".
    return fr'\b({EXPR_REGEX}) *-> *%s\b' % member


def get_member_regex(member):
    # Match "var->member" (get).
    # Don't match "var->member = value" (set).
    # Don't match "Py_CLEAR(var->member)".
    # Only "Py_CLEAR(" exact string is excluded.
    regex = (r'(?<!Py_CLEAR\()'
             + get_member_regex_str(member)
             + r'(?!\s*=\s*)')
    return re.compile(regex)


def assign_regex_str(var, expr):
    # Match "var = expr;".
    return (r'%s\s*=\s*%s\s*;' % (var, expr))


def set_member_regex(member):
    # Match "var->member = expr;".
    regex = assign_regex_str(get_member_regex_str(member), r'([^=].*)')
    return re.compile(regex)


def call_assign_regex(name):
    # Match "Py_TYPE(expr) = expr;".
    # Don't match "assert(Py_TYPE(expr) == expr);".
    # Tolerate spaces
    regex = (r'%s *\( *(.+) *\) *= *([^=].*) *;' % name)
    return re.compile(regex)


def is_c_filename(filename):
    return filename.endswith((".c", ".h"))


class Operation:
    NAME = "<name>"
    DOC = "<doc>"
    REPLACE = ()
    NEED_PYTHONCAPI_COMPAT = False

    def __init__(self, patcher):
        self.patcher = patcher

    def patch(self, content):
        old_content = content
        for regex, replace in self.REPLACE:
            content = regex.sub(replace, content)
        if content != old_content and self.NEED_PYTHONCAPI_COMPAT:
            content = self.patcher.add_pythoncapi_compat(content)
        return content


class Py_TYPE(Operation):
    NAME = "Py_TYPE"
    DOC = 'replace "op->ob_type" with "Py_TYPE(op)"'
    REPLACE = (
        (get_member_regex('ob_type'), r'Py_TYPE(\1)'),
    )
    # Py_TYPE() was added to Python 2.6.


class Py_SIZE(Operation):
    NAME = "Py_SIZE"
    DOC = 'replace "op->ob_size" with "Py_SIZE(op)"'
    REPLACE = (
        (get_member_regex('ob_size'), r'Py_SIZE(\1)'),
    )
    # Py_SIZE() was added to Python 2.6.


class Py_REFCNT(Operation):
    NAME = "Py_REFCNT"
    DOC = 'replace "op->ob_refcnt " with "Py_REFCNT(op)"'
    REPLACE = (
        (get_member_regex('ob_refcnt'), r'Py_REFCNT(\1)'),
    )
    # Py_REFCNT() was added to Python 2.6.


class Py_SET_TYPE(Operation):
    NAME = "Py_SET_TYPE"
    DOC = 'replace "Py_TYPE(obj) = type;" with "Py_SET_TYPE(obj, type);"'
    REPLACE = (
        (call_assign_regex('Py_TYPE'), r'Py_SET_TYPE(\1, \2);'),
        (set_member_regex('ob_type'), r'Py_SET_TYPE(\1, \2);'),
    )
    # Need Py_SET_TYPE(): new in Python 3.9.
    NEED_PYTHONCAPI_COMPAT = True


class Py_SET_SIZE(Operation):
    NAME = "Py_SET_SIZE"
    DOC = 'replace "Py_SIZE(obj) = size;" with "Py_SET_SIZE(obj, size);"'
    REPLACE = (
        (call_assign_regex('Py_SIZE'), r'Py_SET_SIZE(\1, \2);'),
        (set_member_regex('ob_size'), r'Py_SET_SIZE(\1, \2);'),
    )
    # Need Py_SET_SIZE(): new in Python 3.9.
    NEED_PYTHONCAPI_COMPAT = True


class Py_SET_REFCNT(Operation):
    NAME = "Py_SET_REFCNT"
    DOC = ('replace "Py_REFCNT(obj) = refcnt;" '
           'with "Py_SET_REFCNT(obj, refcnt);"')
    REPLACE = (
        (call_assign_regex('Py_REFCNT'), r'Py_SET_REFCNT(\1, \2);'),
        (set_member_regex('ob_refcnt'), r'Py_SET_REFCNT(\1, \2);'),
    )
    # Need Py_SET_REFCNT(): new in Python 3.9.
    NEED_PYTHONCAPI_COMPAT = True


class PyObject_NEW(Operation):
    NAME = "PyObject_NEW"
    # In Python 3.9, the PyObject_NEW() macro becomes an alias to the
    # PyObject_New() macro, and the PyObject_NEW_VAR() macro becomes an alias
    # to the PyObject_NewVar() macro.
    DOC = ('replace "PyObject_NEW(...)" with "PyObject_New(...)", '
           'and replace "PyObject_NEW_VAR(...)" with "PyObject_NewVar(...)"')
    REPLACE = (
        (re.compile(r"\bPyObject_NEW\b( *\()"), r'PyObject_New\1'),
        (re.compile(r"\bPyObject_NEW_VAR\b( *\()"), r'PyObject_NewVar\1'),
    )


class PyMem_MALLOC(Operation):
    NAME = "PyMem_MALLOC"
    # In Python 3.9, the PyObject_NEW() macro becomes an alias to the
    # PyObject_New() macro, and the PyObject_NEW_VAR() macro becomes an alias
    # to the PyObject_NewVar() macro.
    DOC = ('replace "PyMem_MALLOC(...)" with "PyMem_Malloc(...)", '
           'replace "PyMem_REALLOC(...)" with "PyMem_Realloc(...)", '
           'and replace "PyMem_FREE(...)" with "PyMem_Free(...)", '
           'and replace "PyMem_DEL(...)" with "PyMem_Free(...)", '
           'and replace "PyMem_Del(...)" with "PyMem_Free(...)"')

    REPLACE = (
        (re.compile(r"\bPyMem_MALLOC\b( *\()"), r'PyMem_Malloc\1'),
        (re.compile(r"\bPyMem_REALLOC\b( *\()"), r'PyMem_Realloc\1'),
        (re.compile(r"\bPyMem_FREE\b( *\()"), r'PyMem_Free\1'),
        (re.compile(r"\bPyMem_Del\b( *\()"), r'PyMem_Free\1'),
        (re.compile(r"\bPyMem_DEL\b( *\()"), r'PyMem_Free\1'),
    )


class PyObject_MALLOC(Operation):
    NAME = "PyObject_MALLOC"
    # In Python 3.9, the PyObject_NEW() macro becomes an alias to the
    # PyObject_New() macro, and the PyObject_NEW_VAR() macro becomes an alias
    # to the PyObject_NewVar() macro.
    DOC = ('replace "PyObject_MALLOC(...)" with "PyObject_Malloc(...)", '
           'replace "PyObject_REALLOC(...)" with "PyObject_Realloc(...)", '
           'and replace "PyObject_FREE(...)" with "PyObject_Free(...)", '
           'and replace "PyObject_DEL(...)" with "PyObject_Free(...)", '
           'and replace "PyObject_Del(...)" with "PyObject_Free(...)"')

    REPLACE = (
        (re.compile(r"\bPyObject_MALLOC\b( *\()"), r'PyObject_Malloc\1'),
        (re.compile(r"\bPyObject_REALLOC\b( *\()"), r'PyObject_Realloc\1'),
        (re.compile(r"\bPyObject_FREE\b( *\()"), r'PyObject_Free\1'),
        (re.compile(r"\bPyObject_Del\b( *\()"), r'PyObject_Free\1'),
        (re.compile(r"\bPyObject_DEL\b( *\()"), r'PyObject_Free\1'),
    )


class PyFrame_GetBack(Operation):
    NAME = "PyFrame_GetBack"
    DOC = 'replace "frame->f_back" with "_PyFrame_GetBackBorrow(frame)"'
    REPLACE = (
        (get_member_regex('f_back'), r'_PyFrame_GetBackBorrow(\1)'),
    )
    # Need _PyFrame_GetBackBorrow() (PyFrame_GetBack() is new in Python 3.9)
    NEED_PYTHONCAPI_COMPAT = True


class PyFrame_GetCode(Operation):
    NAME = "PyFrame_GetCode"
    DOC = ('replace "frame->f_code" with "_PyFrame_GetCodeBorrow(frame)" '
           'and add a Py_Borrow() static inline function')

    REPLACE = (
        (get_member_regex('f_code'), r'_PyFrame_GetCodeBorrow(\1)'),
    )
    # Need _PyFrame_GetCodeBorrow() (PyFrame_GetCode() is new in Python 3.9)
    NEED_PYTHONCAPI_COMPAT = True


class PyThreadState_GetInterpreter(Operation):
    NAME = "PyThreadState_GetInterpreter"
    DOC = ('replace "tstate->interp" '
           'with "PyThreadState_GetInterpreter(tstate)"')
    REPLACE = (
        (get_member_regex('interp'), r'PyThreadState_GetInterpreter(\1)'),
    )
    # Need PyThreadState_GetInterpreter() (new in Python 3.9)
    NEED_PYTHONCAPI_COMPAT = True


class PyThreadState_GetFrame(Operation):
    NAME = "PyThreadState_GetFrame"
    DOC = ('replace "tstate->frame" '
           'with "_PyThreadState_GetFrameBorrow(tstate)"')
    REPLACE = (
        (get_member_regex('frame'), r'_PyThreadState_GetFrameBorrow(\1)'),
    )
    # Need _PyThreadState_GetFrameBorrow()
    # (PyThreadState_GetFrame() is new in Python 3.9)
    NEED_PYTHONCAPI_COMPAT = True


class Py_INCREF_return(Operation):
    NAME = "Py_INCREF_return"
    DOC = ('replace "Py_INCREF(obj); return (obj);" '
           'with "return Py_NewRef(obj);"')
    REPLACE = (
        (re.compile(r'Py_INCREF\((%s)\);\s*return \1;' % ID_REGEX),
         r'return Py_NewRef(\1);'),
    )
    # Need Py_NewRef(): new in Python 3.10
    NEED_PYTHONCAPI_COMPAT = True


class Py_INCREF_assign(Operation):
    NAME = "Py_INCREF_assign"
    DOC = 'replace "Py_INCREF(obj); var = (obj);" with "var = Py_NewRef(obj);"'
    REPLACE = (
        (re.compile(r'Py_INCREF\((%s)\);\s*' % ID_REGEX
                    + assign_regex_str(r'(%s)' % EXPR_REGEX, r'\1')),
         r'\2 = Py_NewRef(\1);'),
    )
    # Need Py_NewRef(): new in Python 3.10
    NEED_PYTHONCAPI_COMPAT = True


OPERATIONS = (
    Py_SET_TYPE,
    Py_SET_SIZE,
    Py_SET_REFCNT,
    # Py_SET_xxx must be run before Py_xxx
    Py_TYPE,
    Py_SIZE,
    Py_REFCNT,

    PyObject_NEW,
    PyMem_MALLOC,
    PyObject_MALLOC,

    PyFrame_GetBack,
    PyFrame_GetCode,

    PyThreadState_GetInterpreter,
    PyThreadState_GetFrame,
)
if FORCE_NEWREF:
    OPERATIONS.extend((
        Py_INCREF_return,
        Py_INCREF_assign,
    ))


class Patcher:
    def __init__(self, args=None):
        self.exitcode = 0
        self.pythoncapi_compat_added = 0
        self.want_pythoncapi_compat = False
        self.operations = None

        # Set temporariliy by patch()
        self._has_pythoncapi_compat = None
        self._applied_operations = None

        self._parse_options(args)

    def log(self, msg=''):
        print(msg, file=sys.stderr, flush=True)

    def warning(self, msg):
        self.log("WARNING: %s" % msg)

    def _get_operations(self, parser):
        args_names = self.args.operations.split(',')

        wanted = set()
        for name in args_names:
            name = name.strip()
            if not name:
                continue

            if name == "all":
                wanted |= set(operation_class.NAME
                              for operation_class in OPERATIONS)
            elif name.startswith("-"):
                name = name[1:]
                wanted.discard(name)
            else:
                wanted.add(name)

        operations = []
        for operation_class in OPERATIONS:
            name = operation_class.NAME
            if name not in wanted:
                continue
            wanted.discard(name)
            operation = operation_class(self)
            operations.append(operation)

        if wanted:
            print("invalid operations: %s" % ','.join(wanted))
            print()
            self.usage(parser)
            sys.exit(1)

        return operations

    def add_line(self, content, line):
        line = line + '\n'
        # FIXME: tolerate trailing spaces
        if line not in content:
            # FIXME: add macro after the first header comment
            # FIXME: add macro after includes
            # FIXME: add macro after: #define PY_SSIZE_T_CLEAN
            return line + '\n' + content
        else:
            return content

    def add_pythoncapi_compat(self, content):
        if self._has_pythoncapi_compat:
            return content
        content = self.add_line(content, INCLUDE_PYTHONCAPI_COMPAT)
        self._has_pythoncapi_compat = True
        self.pythoncapi_compat_added += 1
        return content

    def _patch(self, content):
        try:
            has = (self.args.no_compat
                   or INCLUDE_PYTHONCAPI_COMPAT in content
                   or INCLUDE_PYTHONCAPI_COMPAT2 in content)
            self._has_pythoncapi_compat = has
            self._applied_operations = []
            for operation in self.operations:
                new_content = operation.patch(content)
                if new_content != content:
                    self._applied_operations.append(operation.NAME)
                content = new_content
            applied_operations = self._applied_operations
        finally:
            self._has_pythoncapi_compat = None
            self._applied_operations = None
        return (content, applied_operations)

    def patch(self, content):
        return self._patch(content)[0]

    def patch_file(self, filename):
        encoding = "utf-8"
        errors = "surrogateescape"

        with open(filename, encoding=encoding, errors=errors) as fp:
            old_contents = fp.read()

        new_contents, operations = self._patch(old_contents)

        if self.args.to_stdout:
            print(new_contents, end="")
            return (new_contents != old_contents)

        # Don't rewrite if the filename for in-place replacement,
        # to avoid changing the file modification time.
        if new_contents == old_contents:
            return False

        if not self.args.no_backup:
            old_filename = filename + ".old"
            # If old_filename already exists, replace it
            os.replace(filename, old_filename)

        with open(filename, "w", encoding=encoding, errors=errors) as fp:
            fp.write(new_contents)

        operations = ', '.join(operations)
        self.log(f"Patched file: {filename} ({operations})")
        return True

    def _walk_dir(self, path):
        empty = True

        for dirpath, dirnames, filenames in os.walk(path):
            # Don't walk into .tox
            try:
                dirnames.remove(".tox")
            except ValueError:
                pass
            for filename in filenames:
                if is_c_filename(filename):
                    yield os.path.join(dirpath, filename)
                    empty = False

        if empty:
            self.warning("Directory %s doesn't contain any "
                         "C file" % path)
            self.exitcode = 1

    def walk(self, paths):
        for path in paths:
            if os.path.isdir(path):
                for filename in self._walk_dir(path):
                    yield filename
            elif os.path.exists(path):
                yield path
            else:
                self.warning("Path %s does not exist" % path)
                self.exitcode = 1

    @staticmethod
    def usage(parser):
        parser.print_help()
        print()
        print("Operations:")
        print()
        for operation in sorted(OPERATIONS,
                                key=lambda operation: operation.NAME):
            print("- %s: %s" % (operation.NAME, operation.DOC))
        print()
        print("If a directory is passed, search for .c and .h files "
              "in subdirectories.")

    def _parse_options(self, args):
        parser = argparse.ArgumentParser(
            description="Upgrade C extension modules to newer Python C API")
        parser.add_argument(
            '-o', '--operations', action="store",
            default="all",
            help='Space separated list of operation names to apply')
        parser.add_argument(
            '-q', '--quiet', action="store_true",
            help='Quiet mode')
        parser.add_argument(
            '-c', '--to-stdout', action="store_true",
            help='Write output into stdout instead of modifying files '
                 'in-place (imply quiet mode)')
        parser.add_argument(
            '-B', '--no-backup', action="store_true",
            help="Don't create .old backup files")
        parser.add_argument(
            '-C', '--no-compat', action="store_true",
            help=f"Don't add: {INCLUDE_PYTHONCAPI_COMPAT}")
        parser.add_argument(
            metavar='file_or_directory', dest="paths", nargs='*')

        args = parser.parse_args(args)
        if not args.paths:
            self.usage(parser)
            sys.exit(1)

        if args.to_stdout:
            args.quiet = True

        self.args = args
        self.operations = self._get_operations(parser)

    def main(self):
        for filename in self.walk(self.args.paths):
            self.patch_file(filename)

        if self.pythoncapi_compat_added and not self.args.quiet:
            self.log()
            self.log(f"{INCLUDE_PYTHONCAPI_COMPAT} added: you may have "
                     f"to copy {PYTHONCAPI_COMPAT_H } to your project")
            self.log("It can be copied from:")
            self.log(PYTHONCAPI_COMPAT_URL)

        sys.exit(self.exitcode)


if __name__ == "__main__":
    Patcher().main()
