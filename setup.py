from setuptools import setup

setup(name='TrackerDash',
      version='0.1',
      description='Live Information Dashboard Written In Python Using Twisted-Klein',
      url='https://github.com/wedgieedward/TrackerDash',
      author='Edward Thomason',
      author_email='edward@thomason.me.uk',
      license='MIT',
      packages=['TrackerDash'],
      install_requires=["Twisted>=12.1", "werkzeug", "klein"],
      zip_safe=False)