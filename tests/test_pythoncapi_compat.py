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


VERBOSE = False


def display_title(title):
    if not VERBOSE:
        return

    print(title)
    print("=" * len(title))
    print()
    sys.stdout.flush()


def build_ext():
    display_title("Build the C extension")
    if os.path.exists("build"):
        shutil.rmtree("build")
    os.environ['CFLAGS'] = "-I .."
    cmd = [sys.executable, "setup.py", "build"]
    if VERBOSE:
        run_command(cmd)
        print()
    else:
        exitcode, stdout = command_stdout(cmd, stderr=subprocess.STDOUT)
        if exitcode:
            print(stdout.rstrip())
            sys.exit(exitcode)


def import_tests():
    pythonpath = None
    for name in os.listdir("build"):
        if name.startswith('lib.'):
            pythonpath = os.path.join("build", name)

    if not pythonpath:
        raise Exception("Failed to find the build directory")
    sys.path.append(pythonpath)
    import test_pythoncapi_compat_cext
    return test_pythoncapi_compat_cext


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


def run_tests(testmod):
    display_title("Run tests")

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
    msg = "%s tests succeeded!" % len(tests)
    msg = "Python %s.%s (%s build): %s" % (ver.major, ver.minor, build, msg)
    if check_refleak:
        msg = "%s (no reference leak detected)" % msg
    print(msg)


def main():
    global VERBOSE
    VERBOSE = "-v" in sys.argv[1:]

    if faulthandler is not None:
        faulthandler.enable()

    src_dir = os.path.dirname(__file__)
    if src_dir:
        os.chdir(src_dir)

    build_ext()
    mod = import_tests()
    run_tests(mod)


if __name__ == "__main__":
    main()
