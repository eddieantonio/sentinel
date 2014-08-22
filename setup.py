from distutils.core import setup
from sentinel import __version__ as VERSION


setup(
    name='sentinel',
    version=VERSION,
    url='https://github.com/eddieantonio/perfection',
    license='MIT',
    author='Eddie Antonio Santos',
    author_email='easantos@ualberta.ca',
    description='Create sentinel objects',
    long_description=open('README.rst').read(),
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
