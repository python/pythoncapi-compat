#!/usr/bin/env python3
import os.path


TEST_CPP = False
SRC_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))

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
CPPFLAGS = COMMON_FLAGS + [
    # no C++ option yet
]

def main():
    from distutils.core import setup, Extension
    import sys

    if len(sys.argv) >= 3 and sys.argv[2] == '--build-cppext':
        global TEST_CPP
        TEST_CPP = True
        del sys.argv[2]

    cflags = ['-I' + SRC_DIR]
    cppflags = list(cflags)
    # Windows uses MSVC compiler
    if os.name != "nt":
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
        cpp_ext = Extension(
            'test_pythoncapi_compat_cppext',
            sources=['test_pythoncapi_compat_cppext.cpp'],
            extra_compile_args=cppflags,
            language='c++')
        extensions.append(cpp_ext)

    setup(name="test_pythoncapi_compat",
          ext_modules=extensions)


if __name__ == "__main__":
    main()
