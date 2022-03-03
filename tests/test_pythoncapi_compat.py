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


# C++ is only supported on Python 3.6 and newer
TEST_CPP = (sys.version_info >= (3, 6))
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
    if TEST_CPP:
        display_title("Build the C and C++ extensions")
    else:
        display_title("Build the C extension")
    if os.path.exists("build"):
        shutil.rmtree("build")
    cmd = [sys.executable, "setup.py", "build"]
    if TEST_CPP:
        cmd.append('--build-cppext')
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

        init_refcnt = sys.gettotalrefcount()
        test_func()
        diff = sys.gettotalrefcount() - init_refcnt

        if i > 3 and diff:
            raise AssertionError("refcnt leak, diff: %s" % diff)


def run_tests(module_name):
    if "cppext" in module_name:
        lang = "C++"
    else:
        lang = "C"
    title = "Test %s (%s)" % (module_name, lang)
    display_title(title)

    testmod = import_tests(module_name)

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

    ver = sys.version_info
    build = 'debug' if hasattr(sys, 'gettotalrefcount') else 'release'
    msg = "%s %s tests succeeded!" % (len(tests), lang)
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
    msg = "%s %s.%s (%s build): %s" % (python_impl, ver.major, ver.minor, build, msg)
    if check_refleak:
        msg = "%s (no reference leak detected)" % msg
    print(msg)


def main():
    global VERBOSE
    VERBOSE = ("-v" in sys.argv[1:] or "--verbose" in sys.argv[1:])

    if faulthandler is not None:
        faulthandler.enable()

    src_dir = os.path.dirname(__file__)
    if src_dir:
        os.chdir(src_dir)

    build_ext()

    run_tests("test_pythoncapi_compat_cext")
    if TEST_CPP:
        run_tests("test_pythoncapi_compat_cppext")


if __name__ == "__main__":
    main()
