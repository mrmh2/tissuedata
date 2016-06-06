import os
from setuptools import setup

version = "0.0.1"

with open('./requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='tissuedata',
    version=version,
    packages=['tissuedata'],
    url='https://github.com/rosscarter3/tissuedata',
    license='MIT',
    author='Matthew Hartley, Ross Carter',
    author_email='matthew.hartley@jic.ac.uk, ross.carter@jic.ac.uk',
    description='tools for dealing with leaf tracking data',
    setup_requires=['numpy'],
    install_requires=required
)