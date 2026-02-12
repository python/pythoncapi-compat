#!/usr/bin/env python3
import os.path
import shlex
import sys
try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension
try:
    from distutils import sysconfig
except ImportError:
    import sysconfig


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
        # /usr/lib64/pypy3.7/include/pyport.h:68:20: error: redefinition of typedef
        # 'Py_hash_t' is a C11 feature
        '-Wno-typedef-redefinition',
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
    CFLAGS = list(COMMON_FLAGS)
CXXFLAGS = list(COMMON_FLAGS)

if not MSVC:
    C_VERSIONS = ('c99', 'c11')
else:
    # MSVC doesn't support /std:c99 flag
    C_VERSIONS = ('c11',)

if not MSVC:
    CXX_VERSIONS = [
        ('test_pythoncapi_compat_cpp03ext', ['-std=c++03']),
        ('test_pythoncapi_compat_cpp11ext', ['-std=c++11']),
        ('test_pythoncapi_compat_cpp14ext', ['-std=c++14']),
        ('test_pythoncapi_compat_cpp17ext', ['-std=c++17']),
        ('test_pythoncapi_compat_cpp20ext', ['-std=c++20']),
    ]
else:
    # MSVC doesn't support /std:c++11
    CXX_VERSIONS = [
        ('test_pythoncapi_compat_cppext', None),
        ('test_pythoncapi_compat_cpp14ext', ['/std:c++14', '/Zc:__cplusplus']),
    ]


def main():
    # gh-105776: When "gcc -std=11" is used as the C++ compiler, -std=c11
    # option emits a C++ compiler warning. Remove "-std11" option from the
    # CC command.
    cmd = (sysconfig.get_config_var('CC') or '')
    if cmd:
        cmd = shlex.split(cmd)
        cmd = [arg for arg in cmd if not arg.startswith('-std=')]
        if (sys.version_info >= (3, 8)):
            cmd = shlex.join(cmd)
        elif (sys.version_info >= (3, 3)):
            cmd = ' '.join(shlex.quote(arg) for arg in cmd)
        else:
            # Python 2.7
            import pipes
            cmd = ' '.join(pipes.quote(arg) for arg in cmd)
        # CC env var overrides sysconfig CC variable in setuptools
        os.environ['CC'] = cmd

    # C extension
    extensions = []
    for std in C_VERSIONS:
        if not MSVC:
            cflags = CFLAGS + ['-std=%s' % std]
        else:
            cflags = CFLAGS + ['/std:%s' % std]
        c_ext = Extension(
            'test_pythoncapi_compat_cext_%s' % std,
            sources=['test_pythoncapi_compat_cext.c'],
            extra_compile_args=cflags)
        extensions.append(c_ext)

    if TEST_CXX:
        # C++ extension
        for name, std_flags in CXX_VERSIONS:
            flags = list(CXXFLAGS)
            if std_flags is not None:
                flags.extend(std_flags)
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
