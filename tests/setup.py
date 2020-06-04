#!/usr/bin/env python3

def main():
    from distutils.core import setup, Extension

    ext = Extension('test_pythoncapi_compat',
                    sources=['test_pythoncapi_compat.c'])

    setup(name="test_pythoncapi_compat", ext_modules=[ext])


if __name__ == "__main__":
    main()
