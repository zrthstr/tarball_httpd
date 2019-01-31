#!/bin/bash

rm -rf dist/tarball*

python3 setup.py sdist bdist_wheel

twine upload --repository pypi dist/*

#twine upload --repository testpypi dist/*

# cd 
# sudo python3 -m pip uninstall tarball_httpd
# sudo python3 -m pip install --index-url https://test.pypi.org/simple/ tarball_httpd
