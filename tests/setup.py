#!/usr/bin/env python3
import os.path


SRC_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))

# C compiler flags for GCC and clang
CFLAGS = ['-Wall', '-Wextra', '-Werror']

def main():
    from distutils.core import setup, Extension

    cflags = ['-I' + SRC_DIR]
    if os.name != "nt":
        cflags.extend(CFLAGS)

    ext = Extension('test_pythoncapi_compat_cext',
                    sources=['test_pythoncapi_compat_cext.c'],
                    extra_compile_args=cflags)

    setup(name="test_pythoncapi_compat", ext_modules=[ext])


if __name__ == "__main__":
    main()
