import setuptools
import tarball_httpd.__main__ as main

with open('README.rst', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='tarball_httpd',
    version=main.__version__,
    description='Simple http server, streaming directories as tarballs.',
    author='zrthstr',
    author_email='zrth1k@gmail.com',
    url='https://github.com/zrth1k/tarball_httpd',
    packages=setuptools.find_packages(),
    license='PSFL',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    keywords='web http server tarball archive download filesharing stream',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Python Software Foundation License',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: System :: Archiving',
        'Topic :: Utilities',
        'Topic :: Communications :: File Sharing',
        'Operating System :: OS Independent',
    ],
)
