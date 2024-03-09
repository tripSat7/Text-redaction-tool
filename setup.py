from setuptools import find_packages, setup


setup(
	name='assignment1',
	version='1.0',
	author='Saatvik Tripathy',
	author_email='satvik.tripathy@ufl.edu',
	packages=find_packages(exclude=('tests', 'docs', 'resources', 'tmp')),
	setup_requires=['pytest-runner'],
	tests_require=['pytest'],
    install_requires=[
        'requests',
    ],
)