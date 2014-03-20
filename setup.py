import sys
from setuptools import setup

if sys.version_info < (2, 7):
    sys.exit("TrackerDash requires python 2.7 installed.")

setup(name='TrackerDash',
      version='0.2',
      description='Live Information Dashboard Written In Python Using Twisted-Klein',
      url='https://github.com/wedgieedward/TrackerDash',
      author='Edward Thomason',
      author_email='edward@thomason.me.uk',
      license='Beerware',
      packages=['TrackerDash'],
      install_requires=["Twisted>=12.1", "werkzeug", "klein", "pymongo", "colander"],
      zip_safe=False)
