'''Setup file for seddy.'''

from setuptools import setup, find_packages

setup(
    name = 'seddy',
    version = '0.1.0',
    license = 'BSD',
    description = 'An IRC bot for tubes.',

    author='Thomas Mannay',
    author_email='tfm@airmail.cc',
    url='https://github.com/sys-fs/seddy',

    packages=find_packages(where='src'),
    package_dir={'': 'src'},

    entry_points={
        'console_scripts': [
            'seddy = seddy.main:main',
        ]
    },
)
