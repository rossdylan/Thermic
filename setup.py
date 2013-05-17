try:
    from distutils.core import setup
except ImportError:
    from setuptools import setup


readme = open('./README', 'r').read()
setup(
    name="heat",
    description="Pure python interface for linux temperature sensing",
    long_description=readme,
    author="Ross Delinger",
    author_email="ross.delinger@gmail.com",
    url="https://github.com/rossdylan/heat",
    version='0.1.1',
    packages=['heat'],
    zip_safe=False
)
