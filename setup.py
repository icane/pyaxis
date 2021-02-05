# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='pyaxis',
    version='0.3.3',
    author='Instituto Cántabro de Estadística',
    author_email='icane@cantabria.es',
    packages=['pyaxis', 'pyaxis.test'],
    url='https://github.com/icane/pyaxis',
    license='Apache License 2.0',
    description='Library to handle PC-Axis data in python using pandas '
                'DataFrames.',
    long_description=open('README.rst').read(),
    install_requires=[
        'numpy', 'requests', 'pandas', 'pyjstat'
    ],
    test_suite='pyaxis.test',
    keywords=['pcaxis', 'json-stat', 'statistics', 'dataframe', 'converter'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries'
        ],
)
