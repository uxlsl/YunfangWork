from setuptools import setup, find_packages

setup(name='scrapy-mymodule',
  entry_points={
    'scrapy.commands': [
      'crawlall=fang_info_test.commands:crawlall',
    ],
  },
 )