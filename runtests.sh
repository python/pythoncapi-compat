set -e -x
python3 tests/test_upgrade_pythoncapi.py -v
python3 tests/test_matrix.py
