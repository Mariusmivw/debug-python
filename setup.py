from setuptools import setup

setup(name='debug',
      version='1.0',
      description='A tiny Python debugging utility modelled after Python\'s core\'s debugging technique.',
      author='Mariusmivw',
      license='MIT',
      packages=['debug'],
      dependency_links=[
          'http://github.com/Mariusmivw/ms-python/tarball/master'
      ],
      zip_safe=False)
