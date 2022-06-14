#!/usr/bin/env python3
import os.path
import sys


TEST_CPP = False
SRC_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))

# Windows uses MSVC compiler
MSVC = (os.name == "nt")

# C compiler flags for GCC and clang
COMMON_FLAGS = [
    # Treat warnings as error
    '-Werror',
    # Enable all warnings
    '-Wall', '-Wextra',
    # Extra warnings
    '-Wconversion',
    # /usr/lib64/pypy3.7/include/pyport.h:68:20: error: redefinition of typedef
    # 'Py_hash_t' is a C11 feature
    "-Wno-typedef-redefinition",
]
CFLAGS = COMMON_FLAGS + [
    # Use C99 for pythoncapi_compat.c which initializes PyModuleDef with a
    # mixture of designated and non-designated initializers
    '-std=c99',
]
CPPFLAGS = list(COMMON_FLAGS)
if sys.version_info >= (3, 12):
    CPPFLAGS.extend((
        '-Wold-style-cast',
        '-Wzero-as-null-pointer-constant',
    ))


def main():
    try:
        from setuptools import setup, Extension
    except ImportError:
        from distutils.core import setup, Extension

    if len(sys.argv) >= 3 and sys.argv[2] == '--build-cppext':
        global TEST_CPP
        TEST_CPP = True
        del sys.argv[2]

    cflags = ['-I' + SRC_DIR]
    cppflags = list(cflags)
    if not MSVC:
        cflags.extend(CFLAGS)
        cppflags.extend(CPPFLAGS)

    # C extension
    c_ext = Extension(
        'test_pythoncapi_compat_cext',
        sources=['test_pythoncapi_compat_cext.c'],
        extra_compile_args=cflags)
    extensions = [c_ext]

    if TEST_CPP:
        # C++ extension
        versions = [('test_pythoncapi_compat_cpp11ext', 'c++11')]
        if not MSVC:
            versions.append(('test_pythoncapi_compat_cpp03ext', 'c++03'))
        for name, std in versions:
            flags = list(cppflags)
            # MSVC has /std flag but doesn't support /std:c++11
            if not MSVC:
                flags.append('-std=' + std)
            cpp_ext = Extension(
                name,
                sources=['test_pythoncapi_compat_cppext.cpp'],
                extra_compile_args=flags,
                language='c++')
            extensions.append(cpp_ext)

    setup(name="test_pythoncapi_compat",
          ext_modules=extensions)


if __name__ == "__main__":
    main()
