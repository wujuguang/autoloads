#!/usr/bin/env python

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    README = f.read()
with open(os.path.join(here, 'CHANGELOG.rst'), encoding='utf-8') as f:
    NEWS = f.read()

version = '0.3.0'

setup(
    name="autoloads",
    version=version,
    description="python web and databases's tools.",
    long_description=README + '\n\n' + NEWS,
    long_description_content_type='text/x-rst',
    license='MIT License',
    author='wuxiaoge',
    author_email='returnliu@gmail.com',
    keywords='autoloads, tornado, sqlalchemy, orm, mako, web',
    url='https://github.com/wujuguang/autoloads',
    packages=find_packages(exclude=[".venv*", "build*", "dist*", "*.egg-info"]),
    python_requires=">=3.11",
    install_requires=["pymysql>=1.2.3", "sqlalchemy>=2.1.3", "tornado>=6.5.10", "mako>=1.4.3", "pipe>=2.2"],
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License'
    ]
)
