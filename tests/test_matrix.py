#!/usr/bin/python3
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


def test_python(python, run_tests):
    cmd = [python, run_tests]
    proc = subprocess.Popen(cmd)
    proc.wait()
    exitcode = proc.returncode
    if exitcode:
        sys.exit(exitcode)


def main():
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

        test_python(executable, run_tests)
        tested.add(executable)

    print()
    print(f"Tested: {len(tested)} Python executables")


if __name__ == "__main__":
    main()
