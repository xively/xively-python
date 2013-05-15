from setuptools import setup

setup(name='xively-python',
      version='0.1.0-rc0',
      description="Xively API wrapper",
      long_description=open("README.rst").read(),
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
