import sys
from setuptools import setup, find_packages

if sys.version_info < (2, 7):
    sys.exit("TrackerDash requires python 2.7 installed.")

setup(
    name='TrackerDash',
    version='0.2',
    description=(
        'Live Information Dashboard Written In Python Using Twisted-Klein'),
    url='https://github.com/wedgieedward/TrackerDash',
    author='Edward Thomason',
    author_email='edward@thomason.me.uk',
    license='Beerware',
    packages=find_packages(exclude=["unittests"]),
    install_requires=[
        "Twisted>=12.1",
        "werkzeug",
        "klein",
        "pymongo",
        "colander",
        "requests"],
    zip_safe=False,
    test_suite='unittests')
