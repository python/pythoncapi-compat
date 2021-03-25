#!/usr/bin/env python3

CFLAGS = ['-Wall', '-Wextra', '-Werror']

def main():
    from distutils.core import setup, Extension

    ext = Extension('test_pythoncapi_compat_cext',
                    sources=['test_pythoncapi_compat_cext.c'],
                    extra_compile_args=CFLAGS)

    setup(name="test_pythoncapi_compat", ext_modules=[ext])


if __name__ == "__main__":
    main()
