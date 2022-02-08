++++++++++++++++++++++++++
Python C API compatibility
++++++++++++++++++++++++++

.. image:: https://github.com/pythoncapi/pythoncapi_compat/actions/workflows/build.yml/badge.svg
   :alt: Build status of pythoncapi_compat on GitHub Actions
   :target: https://github.com/pythoncapi/pythoncapi_compat/actions

The Python C API compatibility project is made of two parts:

* ``pythoncapi_compat.h``: Header file providing new functions of the Python C
  API to old Python versions.
* ``upgrade_pythoncapi.py``: Script upgrading C extension modules to newer
  Python API without losing support for old Python versions. It relies on
  ``pythoncapi_compat.h``.

Homepage:
https://github.com/pythoncapi/pythoncapi_compat

Latest header file:
https://raw.githubusercontent.com/pythoncapi/pythoncapi_compat/master/pythoncapi_compat.h

This project is distributed under the MIT license and is covered by the `PSF
Code of Conduct <https://www.python.org/psf/codeofconduct/>`_.
