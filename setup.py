from setuptools import setup, find_packages

version = '0.2'

long_description = (file('README.txt').read() +
    '\n\n' + file('HISTORY.txt').read())


setup(name='ipdb',
      version=version,
      description="IPython-enabled pdb",
      long_description=long_description,
      classifiers=[],
      keywords='pdb ipython',
      author='Godefroid Chapelle',
      author_email='gotcha@bubblenet.be',
      url='https://trac.bubblenet.be/browser/bubblenet/ipdb/trunk',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'ipython',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
