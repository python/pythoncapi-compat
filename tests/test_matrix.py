#!/usr/bin/python3
import os.path
import subprocess
import sys
import shutil


VERSIONS = (
    (3, 6),
    (3, 7),
    (3, 8),
    (3, 9),
)


def test_python(version, run_tests):
    python = "python%s.%s" % version
    executable = shutil.which(python)
    if not executable:
        print(f"Ignore missing {python}")
        return

    cmd = [executable, run_tests]
    proc = subprocess.Popen(cmd)
    proc.wait()
    exitcode = proc.returncode
    if exitcode:
        sys.exit(exitcode)


def main():
    run_tests = os.path.join(os.path.dirname(__file__), "run_tests.py")
    for version in VERSIONS:
        test_python(version, run_tests)


if __name__ == "__main__":
    main()
