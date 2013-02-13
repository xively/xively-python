from setuptools import setup

setup(name='cosm-python',
      version='0.1',
      description="Cosm API wrapper",
      long_description=file("README.md").read(),
      url='http://github.com/cosm/cosm-python',
      packages=['cosm'],
      install_requires=[
          'requests >= 1.1.0',
      ],
      test_suite='nose.collector',
      tests_require=[
          'nose', 'mock'
      ],
      zip_safe=False)
