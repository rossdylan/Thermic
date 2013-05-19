try:
    from distutils.core import setup
except ImportError:
    from setuptools import setup


readme = open('./README', 'r').read()
setup(
    name="thermic",
    description="Pure python interface for linux temperature sensing",
    long_description=readme,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
    ],
    license="MIT",
    author="Ross Delinger",
    author_email="ross.delinger@gmail.com",
    url="https://github.com/rossdylan/thermic",
    version='0.1.2',
    packages=['thermic'],
    zip_safe=False
)
