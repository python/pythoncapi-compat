#!/usr/bin/python3
"""
Run the test suite on multiple Python versions.

Usage::

    python3 test_matrix.py
    python3 test_matrix.py -v # verbose mode
"""
import os.path
import subprocess
import sys
import shutil


TEST_DIR = os.path.join(os.path.dirname(__file__), 'tests')
TEST_COMPAT = os.path.join(TEST_DIR, "test_pythoncapi_compat.py")
TEST_UPGRADE = os.path.join(TEST_DIR, "test_upgrade_pythoncapi.py")

PYTHONS = (
    "python3.6",
    "python3.7",
    "python3.8",
    "python3.9",
    "python3.10",
    "python3",
    "python3-debug",
)


def run_command(cmd):
    proc = subprocess.Popen(cmd)
    proc.wait()
    exitcode = proc.returncode
    if exitcode:
        sys.exit(exitcode)


def run_tests_exe(executable, verbose, tested):
    executable = os.path.realpath(executable)
    if executable in tested:
        return

    cmd = [executable, TEST_COMPAT]
    if verbose:
        cmd.append('-v')
    run_command(cmd)
    tested.add(executable)


def run_tests(python, verbose, tested):
    executable = shutil.which(python)
    if not executable:
        print(f"Ignore missing: {python}")
        return
    run_tests_exe(executable, verbose, tested)


def main():
    verbose = "-v" in sys.argv[1:]

    cmd = [sys.executable, TEST_UPGRADE]
    if verbose:
        cmd.append('-v')
    run_command(cmd)

    tested = set()
    for python in PYTHONS:
        run_tests(python, verbose, tested)
    run_tests_exe(sys.executable, verbose, tested)

    print()
    print(f"Tested: {len(tested)} Python executables")


if __name__ == "__main__":
    main()
