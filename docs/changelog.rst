Changelog
=========

* 2022-11-15: Add experimental operations to the upgrade_pythoncapi script:
  ``Py_NewRef``, ``Py_CLEAR`` and ``Py_SETREF``.
* 2022-11-09: Fix ``Py_SETREF()`` and ``Py_XSETREF()`` macros
  for `gh-98724 <https://github.com/python/cpython/issues/98724>`_.
* 2022-11-04: Add ``PyFrame_GetVar()`` and ``PyFrame_GetVarString()``
  functions.
* 2022-08-04: Add ``PyCode_GetVarnames()``, ``PyCode_GetFreevars()``
  and ``PyCode_GetCellvars()`` functions.
* 2022-06-14: Fix compatibility with C++ older than C++11.
* 2022-05-03: Add ``PyCode_GetCode()`` function.
* 2022-04-26: Rename the project from ``pythoncapi_compat`` to
  ``pythoncapi-compat``: replace the underscore separator with a dash.
* 2022-04-08: Add functions ``PyFrame_GetLocals()``, ``PyFrame_GetGlobals()``
  ``PyFrame_GetBuiltins()``, and ``PyFrame_GetLasti()``.
* 2022-03-12: Add functions ``PyFloat_Pack2()``, ``PyFloat_Pack4()``,
  ``PyFloat_Pack8()``, ``PyFloat_Unpack2()``, ``PyFloat_Unpack4()`` and
  ``PyFloat_Unpack8()``.
* 2022-03-03: The project moved to https://github.com/python/pythoncapi-compat
* 2022-02-11: The project license changes from the MIT license to the Zero
  Clause BSD (0BSD) license. Projects copying ``pythoncapi_compat.h`` no longer
  have to include the MIT license and the copyright notice.
* 2022-02-08: Add documentation.
* 2022-02-09: ``pythoncapi_compat.h`` now supports C++ on Python 3.6 and newer:
  use ``nullptr`` and ``reinterpret_cast<type>`` cast on C++, and use ``NULL``
  and ``(type)`` cast on C.
* 2021-10-15: Add ``PyThreadState_EnterTracing()`` and
  ``PyThreadState_LeaveTracing()``.
* 2021-04-09: Add ``Py_Is()``, ``Py_IsNone()``, ``Py_IsTrue()``,
  ``Py_IsFalse()`` functions.
* 2021-04-01:

  * Add ``Py_SETREF()``, ``Py_XSETREF()`` and ``Py_UNUSED()``.
  * Add PyPy support.

* 2021-01-27: Fix compatibility with Visual Studio 2008 for Python 2.7.
* 2020-11-30: Creation of the ``upgrade_pythoncapi.py`` script.
* 2020-06-04: Creation of the ``pythoncapi_compat.h`` header file.

