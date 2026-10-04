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

FREE_THREADING = bool(sysconfig.get_config_var('Py_GIL_DISABLED'))
if sys.implementation.name == 'cpython':
    if FREE_THREADING:
        TEST_LIMITED_C_API = (sys.version_info >= (3, 15))
    else:
        TEST_LIMITED_C_API = (sys.version_info >= (3, 11))
else:
    TEST_LIMITED_C_API = False

# C++ is only supported on Python 3.6 and newer
TEST_CXX = (sys.version_info >= (3, 6))

SRC_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))

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

if not MSVC:
    C_VERSIONS = ('c99', 'c11')
else:
    # MSVC doesn't support /std:c99 flag
    C_VERSIONS = ('c11',)
C_EXTENSION_PREFIX = 'test_pythoncapi_compat_cext_'
C_VERSIONS = [(C_EXTENSION_PREFIX + std, std) for std in C_VERSIONS]

LIMITED_SUFFIX = "_limited"

if not MSVC:
    CXX_VERSIONS = [
        'c++03',
        'c++11',
        'c++14',
        'c++17',
        'c++20',
    ]
else:
    # MSVC doesn't support /std:c++11
    CXX_VERSIONS = [
        None,
        'c++14',
    ]
CXX_EXTENSION_PREFIX = 'test_pythoncapi_compat_cppext'

def cxx_extension_name(std):
    if not std:
        return CXX_EXTENSION_PREFIX

    if std.startswith("c++"):
        std = std[3:]
    else:
        raise ValueError(f"invalid options: {std!r}")
    return CXX_EXTENSION_PREFIX + std

CXX_VERSIONS = [(cxx_extension_name(options), options) for options in CXX_VERSIONS]

DEBUG_FLAGS = ('-O0', '-ggdb')


def main():
    try:
        from setuptools import setup, Extension
    except ImportError:
        from distutils.core import setup, Extension

    cflags = list(CFLAGS)
    cxxflags = list(CXXFLAGS)

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

    if DEBUG:
        cflags.extend(DEBUG_FLAGS)
        cxxflags.extend(DEBUG_FLAGS)

    if TEST_LIMITED_C_API:
        limited = f'-DPy_LIMITED_API={sys.hexversion:#x}'
        cflags.append(limited)
        cxxflags.append(limited)

    # C extension
    extensions = []
    sources = ['test_pythoncapi_compat_cext.c']
    for name, std in C_VERSIONS:
        if not MSVC:
            flags = cflags + [f'-std={std}']
        else:
            flags = cflags + [f'/std:{std}']

        def add_extension(name):
            ext_flags = [*flags, f'-DMODULE_NAME={name}']
            ext = Extension(name, sources=sources, extra_compile_args=ext_flags)
            extensions.append(ext)

        add_extension(name)
        if TEST_LIMITED_C_API:
            add_extension(name + LIMITED_SUFFIX)

    if TEST_CXX:
        # C++ extension
        sources = ['test_pythoncapi_compat_cppext.cpp']
        for name, std in CXX_VERSIONS:
            flags = list(cxxflags)
            if std is not None:
                if MSVC:
                    std_flags = [f'/std:{std}', '/Zc:__cplusplus']
                else:
                    std_flags = [f'-std={std}']
                flags.extend(std_flags)

            def add_extension(name):
                ext_flags = [*flags, f'-DMODULE_NAME={name}']
                ext = Extension(name, sources=sources,
                                extra_compile_args=ext_flags, language='c++')
                extensions.append(ext)

            add_extension(name)
            if TEST_LIMITED_C_API:
                add_extension(name + LIMITED_SUFFIX)

    setup(name="test_pythoncapi_compat", ext_modules=extensions)


if __name__ == "__main__":
    main()
