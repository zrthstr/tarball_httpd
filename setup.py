import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='tarball_httpd',
    version='0.0.dev3',
    description='http server based on htto.server allowing directorys to be downloaded as tarballs',
    author='zrthstr',
    author_email='zrth1k@gmail.com',
    url='https://github.com/zrth1k/tarball_httpd',
    packages=setuptools.find_packages(),
    license='PSFL',
    long_description=long_description,
    long_description_content_type='text/markdown',
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
