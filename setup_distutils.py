from distutils.core import setup, Extension

import io

module_device = Extension('device',
                        sources = ['device/device.cpp']
                      )

setup (name = 'windows-capture-device-list',
            version = '1.1.0',
            description = 'Get device list with Windows DirectShow',
            long_description_content_type="text/markdown",
            author='yushulx',
            url='https://github.com/yushulx/python-capture-device-list',
            license='MIT',
        ext_modules = [module_device],
        options={'build':{'build_lib':'./device'}},
        classifiers=[
                "Development Status :: 5 - Production/Stable",
                "Environment :: Console",
                "Intended Audience :: Developers",
                "Intended Audience :: Education",
                "Intended Audience :: Information Technology",
                "Intended Audience :: Science/Research",
                "License :: OSI Approved :: MIT License",
                "Operating System :: Microsoft :: Windows",
                "Programming Language :: Python",
                "Programming Language :: Python :: 3",
                "Programming Language :: Python :: 3 :: Only",
                "Programming Language :: Python :: 3.6",
                "Programming Language :: Python :: 3.7",
                "Programming Language :: Python :: 3.8",
                "Programming Language :: Python :: 3.9",
                "Programming Language :: Python :: 3.10",
                "Programming Language :: C++",
                "Programming Language :: Python :: Implementation :: CPython",
                "Topic :: Scientific/Engineering",
                "Topic :: Software Development",
            ],)