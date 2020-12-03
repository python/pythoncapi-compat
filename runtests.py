#!/usr/bin/python3
"""
Run the test suite on multiple Python versions.

Usage::

    python3 test_matrix.py
    python3 test_matrix.py -v # verbose mode
"""
import argparse
import os.path
import shutil
import subprocess
import sys


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


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action="store_true",
                        help='Verbose mode')
    parser.add_argument('-c', '--current', action="store_true",
                        help="Only test the current Python executable "
                             "(don't test multiple Python versions)")
    return parser.parse_args()


def main():
    args = parse_args()

    cmd = [sys.executable, TEST_UPGRADE]
    if args.verbose:
        cmd.append('-v')
    run_command(cmd)
    print()

    tested = set()
    if not args.current:
        for python in PYTHONS:
            run_tests(python, args.verbose, tested)
        run_tests_exe(sys.executable, args.verbose, tested)

        print()
        print(f"Tested: {len(tested)} Python executables")
    else:
        run_tests_exe(sys.executable, args.verbose, tested)


if __name__ == "__main__":
    main()
