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


PYTHONS = (
    "python3.6",
    "python3.7",
    "python3.8",
    "python3.9",
    "python3",
    "python3-debug",
)


def run_command(cmd):
    proc = subprocess.Popen(cmd)
    proc.wait()
    exitcode = proc.returncode
    if exitcode:
        sys.exit(exitcode)


def main():
    verbose = "-v" in sys.argv[1:]

    run_tests = os.path.join(os.path.dirname(__file__), "run_tests.py")
    tested = set()
    for python in PYTHONS:
        executable = shutil.which(python)
        if not executable:
            print(f"Ignore missing: {python}")
            return
        executable = os.path.realpath(executable)
        if executable is tested:
            continue

        cmd = [executable, run_tests]
        if verbose:
            cmd.append('-v')
        run_command(cmd)
        tested.add(executable)

    print()
    print(f"Tested: {len(tested)} Python executables")


if __name__ == "__main__":
    main()
