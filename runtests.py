#!/usr/bin/python3 -u
"""
Run the test suite on multiple Python versions.

Usage::

    python3 runtests.py
    python3 runtests.py --verbose
    python3 runtests.py --current --verbose
"""
import argparse
import os.path
import shutil
import sys
import time
from concurrent.futures import ThreadPoolExecutor

from tests.utils import get_output, run_command

TEST_DIR = os.path.join(os.path.dirname(__file__), 'tests')
TEST_COMPAT = os.path.join(TEST_DIR, "test_pythoncapi_compat.py")
TEST_UPGRADE = os.path.join(TEST_DIR, "test_upgrade_pythoncapi.py")

PYTHONS = (
    # CPython
    "python3-debug",
    "python3",
    "python3.6",
    "python3.7",
    "python3.8",
    "python3.9",
    "python3.10",
    "python3.11",
    "python3.12",
    "python3.13",
    "python3.13t",
    "python3.14",
    "python3.14t",
    "python3.15",
    "python3.15t",

    # PyPy
    "pypy3",
    "pypy3.6",
    "pypy3.7",
    "pypy3.8",
    "pypy3.9",
    "pypy3.10",
    "pypy3.11",
    "pypy3.12",
)


def get_test_command(executable, verbose):
    # Don't use realpath() for the executed command to support virtual
    # environments
    cmd = [executable, TEST_COMPAT]
    if verbose:
        cmd.append('-v')
    return cmd


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action="store_true",
                        help='Verbose mode')
    parser.add_argument('-c', '--current', action="store_true",
                        help="Only test the current Python executable "
                             "(don't test multiple Python versions)")
    return parser.parse_args()


def run_tests_parallel(args):
    jobs = []

    tested = set()
    tested_key = os.path.realpath(sys.executable)
    tested.add(tested_key)
    jobs.append(sys.executable)

    for python in PYTHONS:
        executable = shutil.which(python)
        if not executable:
            print(f"Ignore missing Python executable: {python}")
            continue
        tested_key = os.path.realpath(executable)
        if tested_key in tested:
            continue
        tested.add(tested_key)
        jobs.append(executable)

    def worker(executable):
        cmd = get_test_command(executable, args.verbose)
        return get_output(cmd)

    if hasattr(os, 'process_cpu_count'):
        max_workers = os.process_cpu_count()
    else:
        max_workers = os.cpu_count()

    print()
    print(f"Run {len(jobs)} jobs with {max_workers} workers (threads)")
    print()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        exitcode = None
        for exitcode, stdout in executor.map(worker, jobs):
            print(stdout, end='')
            if exitcode:
                break

        if exitcode:
            executor.shutdown(wait=True, cancel_futures=True)
            sys.exit(exitcode)

    print()
    print(f"Tested: {len(jobs)} Python executables")


def test_upgrade_pythoncapi(args):
    # upgrade_pythoncapi.py requires Python 3.6 or newer
    print(f"Run {TEST_UPGRADE}")
    cmd = [sys.executable, TEST_UPGRADE]
    if args.verbose:
        cmd.append('-v')
    run_command(cmd)
    print()


def main():
    start_time = time.perf_counter()
    args = parse_args()

    test_upgrade_pythoncapi(args)

    if not args.current:
        run_tests_parallel(args)
    else:
        cmd = get_test_command(sys.executable, args.verbose)
        run_command(cmd)
        print()

    dt = time.perf_counter() - start_time
    print(f"Total time: {dt:.1f} seconds")


if __name__ == "__main__":
    main()
