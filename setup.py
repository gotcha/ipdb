# Copyright (c) 2007-2016 Godefroid Chapelle and ipdb development team
#
# This file is part of ipdb.
# Redistributable under the revised BSD license
# https://opensource.org/licenses/BSD-3-Clause

from setuptools import setup, find_packages
from sys import version_info
import re
import io

version = re.search(
    r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',  # It excludes inline comment too
    io.open('ipdb/__main__.py', encoding='utf_8_sig').read()
    ).group(1)

long_description = (open('README.rst').read() +
    '\n\n' + open('HISTORY.txt').read())


if version_info[0] == 2:
    console_script = 'ipdb'
else:
    console_script = 'ipdb%d' % version_info.major


setup(name='ipdb',
      version=version,
      description="IPython-enabled pdb",
      long_description=long_description,
      classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Software Development :: Debuggers',
        'License :: OSI Approved :: BSD License',
      ],
      keywords='pdb ipython',
      author='Godefroid Chapelle',
      author_email='gotcha@bubblenet.be',
      url='https://github.com/gotcha/ipdb',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      test_suite='tests',
      python_requires=">=2.7",
      install_requires=[
          'setuptools'
      ],
      extras_require={
          ':python_version == "2.7"': ['ipython >= 5.1.0, < 6.0.0'],
          # No support for python 3.0, 3.1, 3.2.
          ':python_version == "3.4"': ['ipython >= 6.0.0, < 7.0.0'],
          ':python_version == "3.5"': ['ipython >= 7.0.0, < 7.10.0'],
          ':python_version == "3.6"': ['ipython >= 7.10.0, < 7.17.0'],
          ':python_version > "3.6"': ['ipython >= 7.17.0'],
      },
      tests_require=[
          'mock'
      ],
      entry_points={
          'console_scripts': ['%s = ipdb.__main__:main' % console_script]
      }
)
