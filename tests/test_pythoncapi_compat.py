#!/usr/bin/python3
"""
Run the test suite.

Usage::

    python3 run_tests.py
    python3 run_tests.py -v # verbose mode
"""
from __future__ import absolute_import
from __future__ import print_function
import os.path
import shutil
import subprocess
import sys
try:
    import faulthandler
except ImportError:
    # Python 2
    faulthandler = None

# test.utils
from utils import run_command, command_stdout


TESTS = [
    ("test_pythoncapi_compat_cext", "C"),
    ("test_pythoncapi_compat_cppext", "C++"),
    ("test_pythoncapi_compat_cpp03ext", "C++03"),
    ("test_pythoncapi_compat_cpp11ext", "C++11"),
]

VERBOSE = False


def display_title(title):
    if not VERBOSE:
        return

    ver = sys.version_info
    title = "Python %s.%s: %s" % (ver.major, ver.minor, title)

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
    sys.path.append(pythonpath)

    return __import__(module_name)


def _run_tests(tests, verbose):
    for name, test_func in tests:
        if verbose:
            print("%s()" % name)
            sys.stdout.flush()
        test_func()


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
    return "%s %s.%s (%s build)" % (python_impl, ver.major, ver.minor, build)


def run_tests(module_name, lang):
    title = "Test %s (%s)" % (module_name, lang)
    display_title(title)

    try:
        testmod = import_tests(module_name)
    except ImportError:
        # The C extension must always be available
        if lang == "C":
            raise

        if VERBOSE:
            print("%s: skip %s, missing %s extension"
                  % (python_version(), lang, module_name))
            print()
        return

    if VERBOSE and hasattr(testmod, "__cplusplus"):
        print("__cplusplus: %s" % testmod.__cplusplus)

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

    # Implementing PyFrame_GetLocals() and PyCode_GetCode() require the
    # internal C API in Python 3.11 alpha versions.
    # Implementing PyCode_GetVarnames() requires the internal C API
    # in Python 3.11 beta versions.
    if 0x30b0000 <= sys.hexversion < 0x30b00c1:
        version = sys.version.split()[0]
        print("SKIP TESTS: Python %s is not supported" % version)
        return

    if faulthandler is not None:
        faulthandler.enable()

    src_dir = os.path.dirname(__file__)
    if src_dir:
        os.chdir(src_dir)

    build_ext()

    for module_name, lang in TESTS:
        run_tests(module_name, lang)


if __name__ == "__main__":
    main()
