#!/usr/bin/env python

from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='fortimailapi',
    packages=['fortimailapi'],
    version='0.1.0',
    description='Python modules to interact with FortiMail product from Fortinet using REST API',
    long_description=readme(),
    # Valid Classifiers are here: https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python ',
        'Topic :: Security',
    ],
    keywords='Fortinet fortimail rest api',
    install_requires=['requests'],
    author='M A M A',
    author_email='ma-hidden@ftnt.com',
    url='https://github.com/fortinet-solutions-cse/fortimailapi',
    include_package_data=True
)