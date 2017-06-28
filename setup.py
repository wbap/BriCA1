from setuptools import setup, find_packages
import sys, os

version = '1.0.0'

setup(name='brica1',
      version=version,
      description="",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='ktnyt',
      author_email='kotone [at] sfc.keio.ac.jp',
      url='',
      license='Apache v2',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'numpy',
          'future'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
