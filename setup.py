from distutils.core import setup
from sentinel import __version__ as VERSION

with open('README.rst') as readme:
    long_description = readme.read()

setup(
    name='sentinel',
    version=VERSION,
    url='https://github.com/eddieantonio/sentinel',
    license='MIT',
    author='Eddie Antonio Santos',
    author_email='easantos@ualberta.ca',
    description='Create sentinel and singleton objects',
    long_description=long_description,
    py_modules=['sentinel'],
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
    ],
    download_url = 'https://github.com/eddieantonio/sentinel/tarball/v' + VERSION,
)
