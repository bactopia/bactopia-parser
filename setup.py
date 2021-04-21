#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = []

setup_requirements = []

test_requirements = []

setup(
    author="Robert A. Petit III",
    author_email='robbie.petit@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A Python package for working with Bactopia results.",
    entry_points={
        'console_scripts': [
            'bactopia-summary=bactopia.cli.summary:main',
            'bactopia-jsonify=bactopia.cli.jsonify:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='bactopia',
    name='bactopia',
    packages=find_packages(include=['bactopia', 'bactopia.parsers', 'bactopia.cli']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/rpetit3/bactopia-py',
    version='0.1.2',
    zip_safe=False,
)
