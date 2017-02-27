"""
A setuptools based setup module for the Open Project Linter.

Based on https://github.com/pypa/sampleproject/blob/master/setup.py
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README
with(open(path.join(here, 'README.md'), encoding='utf-8')) as f:
    long_description = f.read()

setup(
    name='open-project-linter',
    version='0.4dev',
    packages=find_packages(),
    package_data={
        'openlinter': ['*.yml'],
    },
    install_requires=['gitpython', 'pyyaml', 'pygments'],
    license='Apache v2.0',
    description='Automatic checklist for open source project best practices.',
    long_description=long_description,
    url='https://github.com/OpenNewsLabs/open-project-linter',
    author='Frances Hocutt',
    author_email='frances.hocutt+pypi@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'Topic :: Software Development :: Version Control',
    ],
    keywords='project linter setup documentation development',
    entry_points={
        'console_scripts': ['openlinter=openlinter.openlinter:main']
    }
)
