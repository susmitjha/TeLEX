from setuptools import setup, find_packages

EXCLUDE_FROM_PACKAGES = ["tests","build","docs"]

setup(name='TeLEX',
      version = '0.1',
      description = 'Temporal Logic Extractor',
      author = 'Susmit Jha',
      author_email = 'jha@eecs.berkeley.edu',
      license = '',
      install_requires=[
          'parsimonious',
          'numpy',
          'pandas',
          'singledispatch'
      ],
      packages=find_packages(),
)
