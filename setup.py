from setuptools import setup

setup(name='xively-python',
      version='0.1.0-rc2',
      description="Xively API wrapper",
      long_description="This is the official pythonic wrapper library for the Xively V2 API.",
      url='http://github.com/xively/xively-python',
      packages=['xively'],
      install_requires=[
          'requests >= 1.1.0',
      ],
      test_suite='nose.collector',
      tests_require=[
          'nose', 'mock', 'doctest-ignore-unicode',
      ],
      zip_safe=False)
