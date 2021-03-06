from setuptools import setup, find_packages
from codecs import open
from os import path

__version__ = '0.0.6'

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

# Get the dependencies and installs
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

# Construct dependency links for registered packages
install_requires = [x.strip() for x in all_reqs if 'git+' not in x]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if x.startswith('git+')]

setup(
    name='parsetta',
    version=__version__,
    description='Collection of data parsers and utilities functions',
    long_description_content_type='text/markdown',
    long_description=long_description,
    url='https://github.com/Sutton-Research-Lab/parsetta',
    download_url='https://github.com/Sutton-Research-Lab/parsetta/tarball/' + __version__,
    license='MIT',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Programming Language :: Python :: 3',
    ],
    keywords='',
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    author='R. Patrick Xian, Christopher Sutton',
    install_requires=install_requires,
    dependency_links=dependency_links
)
