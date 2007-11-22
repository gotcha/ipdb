from setuptools import setup, find_packages

version = '0.1'

setup(name='ipdb',
      version=version,
      description="IPython-enabled pdb",
      long_description=file('README.txt').read(),
      classifiers=[], # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      keywords='pdb ipython',
      author='Godefroid Chapelle',
      author_email='gotcha@bubblenet.be',
      url='http://trac.gotcha.python-hosting.com/file/bubblenet/pythoncode/ipdb/README.txt?format=txt',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
          'ipython',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
