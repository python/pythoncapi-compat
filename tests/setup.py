#!/usr/bin/env python3
import os.path
import shlex
import sys

try:
    import sysconfig
except ImportError:
    from distutils import sysconfig


# Set to true to debug C/C++ extensions in gdb
DEBUG = False

MS_WINDOWS = (sys.platform == 'win32')
FREE_THREADING = bool(sysconfig.get_config_var('Py_GIL_DISABLED'))
if sys.implementation.name == 'cpython':
    if FREE_THREADING:
        TEST_LIMITED_C_API = (sys.version_info >= (3, 15))
    else:
        TEST_LIMITED_C_API = True
else:
    TEST_LIMITED_C_API = False

SRC_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
LIMITED_SUFFIX = "_limited"
# Windows uses MSVC compiler
MSVC = (os.name == "nt")

COMMON_FLAGS = [
    '-I' + SRC_DIR,
]
if not MSVC:
    # C compiler flags for GCC and clang
    COMMON_FLAGS.extend((
        # Treat warnings as error
        '-Werror',
        # Enable all warnings
        '-Wall', '-Wextra',
        # Extra warnings
        '-Wconversion',
        # Formatting checks
        '-Wformat',
        '-Wformat-nonliteral',
        '-Wformat-security',
    ))
    CFLAGS = COMMON_FLAGS
else:
    # C compiler flags for MSVC
    COMMON_FLAGS.extend((
        # Treat all compiler warnings as compiler errors
        '/WX',
    ))
    # Python 3.11 and older emits C4100 "unreferenced parameter" warnings
    # on Py_UNUSED() parameters. Py_UNUSED() was modified in Python 3.12
    # to support MSVC.
    if sys.version_info >= (3, 12):
        COMMON_FLAGS.extend((
            # Display warnings level 1 to 4
            '/W4',
        ))
    CFLAGS = list(COMMON_FLAGS)
CXXFLAGS = list(COMMON_FLAGS)


# C extensions
C_EXTENSION_PREFIX = 'test_pythoncapi_compat_cext'
def c_extension_name(std):
    if not std:
        return C_EXTENSION_PREFIX

    if std.startswith("c"):
        std = std[1:]
    else:
        raise ValueError(f"invalid std: {std!r}")
    return C_EXTENSION_PREFIX + std

if not MSVC:
    C_TESTS = ('c99', 'c11')
else:
    # MSVC doesn't support /std:c99 flag
    C_TESTS = ('c11',)
C_TESTS = [(c_extension_name(std), std, False) for std in C_TESTS]
if TEST_LIMITED_C_API:
    C_TESTS.append((C_EXTENSION_PREFIX + LIMITED_SUFFIX, None, True))


# C++ extensions
CXX_EXTENSION_PREFIX = 'test_pythoncapi_compat_cppext'
def cxx_extension_name(std):
    if not std:
        return CXX_EXTENSION_PREFIX

    if std.startswith("c++"):
        std = std[3:]
    else:
        raise ValueError(f"invalid std: {std!r}")
    return CXX_EXTENSION_PREFIX + std

if not MSVC:
    CXX_TESTS = [
        'c++03',
        'c++11',
        'c++14',
        'c++17',
        'c++20',
    ]
    CXX_DEFAULT_STD = 'c++11'
else:
    # MSVC doesn't support /std:c++11
    CXX_TESTS = [
        None,
        'c++14',
    ]
    CXX_DEFAULT_STD = 'c++14'
CXX_TESTS = [(cxx_extension_name(options), options, False)
                for options in CXX_TESTS]
if TEST_LIMITED_C_API:
    CXX_TESTS.append((CXX_EXTENSION_PREFIX + LIMITED_SUFFIX, CXX_DEFAULT_STD, True))

DEBUG_FLAGS = ('-O0', '-ggdb')


def main():
    try:
        from setuptools import setup, Extension
    except ImportError:
        from distutils.core import setup, Extension

    cflags = list(CFLAGS)
    cxxflags = list(CXXFLAGS)
    limited_flag = f'-DPy_LIMITED_API={sys.hexversion:#x}'

    # gh-105776: When "gcc -std=11" is used as the C++ compiler, -std=c11
    # option emits a C++ compiler warning. Remove "-std11" option from the
    # CC command.
    cmd = (sysconfig.get_config_var('CC') or '')
    if cmd:
        cmd = shlex.split(cmd)
        cmd = [arg for arg in cmd if not arg.startswith('-std=')]
        if (sys.version_info >= (3, 8)):
            cmd = shlex.join(cmd)
        else:
            cmd = ' '.join(shlex.quote(arg) for arg in cmd)
        # CC env var overrides sysconfig CC variable in setuptools
        os.environ['CC'] = cmd

    def add_common_flags(flags, limited):
        if limited:
            flags.append(limited_flag)
        if DEBUG:
            flags.extend(DEBUG_FLAGS)

    # C extension
    extensions = []
    sources = ['test_pythoncapi_compat_cext.c']
    for name, std, limited in C_TESTS:
        flags = [*cflags, f'-DMODULE_NAME={name}']
        if std:
            if not MSVC:
                flags.append(f'-std={std}')
            else:
                flags.append(f'/std:{std}')
        add_common_flags(flags, limited)

        ext = Extension(
            name,
            sources=sources,
            extra_compile_args=flags)
        extensions.append(ext)

    # C++ extension
    sources = ['test_pythoncapi_compat_cppext.cpp']
    for name, std, limited in CXX_TESTS:
        flags = [*cxxflags, f'-DMODULE_NAME={name}']
        if std:
            if MSVC:
                flags.extend([f'/std:{std}', '/Zc:__cplusplus'])
            else:
                flags.append(f'-std={std}')
        add_common_flags(flags, limited)

        ext = Extension(
            name,
            sources=sources,
            extra_compile_args=flags,
            language='c++')
        extensions.append(ext)

    setup(name="test_pythoncapi_compat", ext_modules=extensions)


if __name__ == "__main__":
    main()
