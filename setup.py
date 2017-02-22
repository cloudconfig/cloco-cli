"""
A command line interface for the cloco API.
"""
from setuptools import find_packages, setup

dependencies = ['click', 'requests', 'configparser']

setup(
    name='cloco-cli',
    version='0.1.5',
    license='BSD',
    author='345 Systems',
    author_email='info@345.systems',
    description='A command line interface for the cloco API.',
    url='https://github.com/cloudconfig/cloco-cli',
    download_url='https://github.com/cloudconfig/cloco-cli/tarball/0.1.5',
    keywords=['cloco', 'cloudconfig', 'configuration',
              'configuration-as-a-service', 'devops'],
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'cloco = cloco_cli.cli:main',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Build Tools',
    ]
)
