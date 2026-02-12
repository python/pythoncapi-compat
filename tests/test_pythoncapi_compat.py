#!/usr/bin/python3
"""
Run the test suite.

Usage::

    python3 run_tests.py
    python3 run_tests.py -v # verbose mode
"""
from __future__ import absolute_import
from __future__ import print_function
import gc
import os.path
import shutil
import subprocess
import sys
try:
    import faulthandler
except ImportError:
    # Python 2
    faulthandler = None
try:
    import sysconfig
except ImportError:
    # Python 3.1 and older
    sysconfig = None

# test.utils
from utils import run_command, command_stdout


# Windows uses MSVC compiler
MSVC = (os.name == "nt")

# C++ is only supported on Python 3.6 and newer
TEST_CXX = (sys.version_info >= (3, 6))

if not MSVC:
    C_TESTS = [
        ("test_pythoncapi_compat_cext_c99", "C99"),
        ("test_pythoncapi_compat_cext_c11", "C11"),
    ]
    CXX_TESTS = [
        ("test_pythoncapi_compat_cpp03ext", "C++03"),
        ("test_pythoncapi_compat_cpp11ext", "C++11"),
        ("test_pythoncapi_compat_cpp14ext", "C++14"),
        ("test_pythoncapi_compat_cpp17ext", "C++17"),
        ("test_pythoncapi_compat_cpp20ext", "C++20"),
    ]
else:
    C_TESTS = [
        ("test_pythoncapi_compat_cext_c11", "C11"),
    ]
    CXX_TESTS = [
        ("test_pythoncapi_compat_cppext", "C++"),
        ("test_pythoncapi_compat_cpp14ext", "C++14"),
    ]


VERBOSE = False


def display_title(title):
    if not VERBOSE:
        return

    title = "%s: %s" % (python_version(), title)
    print(title)
    print("=" * len(title))
    print()
    sys.stdout.flush()


def build_ext():
    display_title("Build test extensions")
    if os.path.exists("build"):
        shutil.rmtree("build")
    cmd = [sys.executable, "setup.py", "build"]
    if VERBOSE:
        run_command(cmd)
        print()
    else:
        exitcode, stdout = command_stdout(cmd, stderr=subprocess.STDOUT)
        if exitcode:
            print(stdout.rstrip())
            sys.exit(exitcode)


def import_tests(module_name):
    pythonpath = None
    for name in os.listdir("build"):
        if name.startswith('lib.'):
            pythonpath = os.path.join("build", name)

    if not pythonpath:
        raise Exception("Failed to find the build directory")
    old_sys_path = list(sys.path)
    try:
        sys.path.append(pythonpath)
        return __import__(module_name)
    finally:
        sys.path[:] = old_sys_path


def _run_tests(tests, verbose):
    for name, test_func in tests:
        if verbose:
            print("%s()" % name)
            sys.stdout.flush()
        test_func()


_HAS_CLEAR_INTERNAL_CACHES = hasattr(sys, '_clear_internal_caches')
_HAS_CLEAR_TYPE_CACHE = hasattr(sys, '_clear_type_cache')

def _refleak_cleanup():
    if _HAS_CLEAR_INTERNAL_CACHES:
        sys._clear_internal_caches()
    elif _HAS_CLEAR_TYPE_CACHE:
        sys._clear_type_cache()
    gc.collect()


def _check_refleak(test_func, verbose):
    nrun = 6
    for i in range(1, nrun + 1):
        if verbose:
            if i > 1:
                print()
            print("Run %s/%s:" % (i, nrun))
            sys.stdout.flush()

        init_refcnt = sys.gettotalrefcount()
        test_func()
        _refleak_cleanup()
        diff = sys.gettotalrefcount() - init_refcnt

        if i > 3 and diff:
            raise AssertionError("refcnt leak, diff: %s" % diff)


def python_version():
    ver = sys.version_info
    build = 'debug' if hasattr(sys, 'gettotalrefcount') else 'release'
    if hasattr(sys, 'implementation'):
        python_impl = sys.implementation.name
        if python_impl == 'cpython':
            python_impl = 'CPython'
        elif python_impl == 'pypy':
            python_impl = 'PyPy'
    else:
        if "PyPy" in sys.version:
            python_impl = "PyPy"
        else:
            python_impl = 'Python'
    pyver = "%s.%s" % (ver.major, ver.minor)
    if ver >= (3, 13):
        if sysconfig.get_config_var('Py_GIL_DISABLED'):
            # Free-threaded build
            pyver += "t"
    return "%s %s (%s build)" % (python_impl, pyver, build)


def run_tests(module_name, lang):
    if VERBOSE:
        print("")

    title = "Test %s (%s)" % (module_name, lang)
    display_title(title)

    testmod = import_tests(module_name)

    if VERBOSE:
        empty_line = False
        for attr in ('__cplusplus', 'PY_VERSION', 'PY_VERSION_HEX',
                     'PYPY_VERSION', 'PYPY_VERSION_NUM'):
            try:
                value = getattr(testmod, attr)
            except AttributeError:
                pass
            else:
                if attr in ("PY_VERSION_HEX", "PYPY_VERSION_NUM"):
                    value = "0x%x" % value
                print("%s: %s" % (attr, value))
                empty_line = True

        if empty_line:
            print()

    check_refleak = hasattr(sys, 'gettotalrefcount')

    tests = [(name, getattr(testmod, name))
             for name in dir(testmod)
             if name.startswith("test")]

    def test_func():
        _run_tests(tests, VERBOSE)

    if check_refleak:
        _check_refleak(test_func, VERBOSE)
    else:
        test_func()

    if VERBOSE:
        print()

    msg = "%s %s tests succeeded!" % (len(tests), lang)
    msg = "%s: %s" % (python_version(), msg)
    if check_refleak:
        msg = "%s (no reference leak detected)" % msg
    print(msg)


def main():
    global VERBOSE
    VERBOSE = ("-v" in sys.argv[1:] or "--verbose" in sys.argv[1:])

    if (3, 13) <= sys.version_info <= (3, 13, 0, 'alpha', 4):
        print("SKIP Python 3.13 alpha 1..4: not supported!")
        return

    if faulthandler is not None:
        faulthandler.enable()

    src_dir = os.path.dirname(__file__)
    if src_dir:
        os.chdir(src_dir)

    build_ext()

    tests = list(C_TESTS)
    if TEST_CXX:
        tests += CXX_TESTS
    for module_name, lang in tests:
        run_tests(module_name, lang)


if __name__ == "__main__":
    main()
