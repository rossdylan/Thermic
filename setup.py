try:
    from distutils.core import setup
except ImportError:
    from setuptools import setup


readme = open('./README', 'r').read()
setup(
    name="heat",
    description="Pure python interface for linux temperature sensing",
    long_description=readme,
    version='0.1.0',
    packages=['heat'],
    zip_safe=False
)
