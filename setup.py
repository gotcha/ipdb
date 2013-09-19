# Copyright (c) 2007, 2010, 2011, 2012 Godefroid Chapelle
#
# This file is part of ipdb.
# GNU package is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# GNU package is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.

from setuptools import setup, find_packages
from sys import version_info

version = '0.7.1'

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
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Software Development :: Debuggers',
      ],
      keywords='pdb ipython',
      author='Godefroid Chapelle',
      author_email='gotcha@bubblenet.be',
      url='https://github.com/gotcha/ipdb',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      test_suite='tests',
      install_requires=[
          'ipython >= 0.10',
      ],
      entry_points={
          'console_scripts': ['%s = ipdb.__main__:main' % console_script]
      },
      use_2to3=True,
)
