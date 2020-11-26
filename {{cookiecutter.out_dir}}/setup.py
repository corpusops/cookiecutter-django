#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(
        os.path.join(".", *rnames)
    ).read()
READMES = [a for a in ['README', 'README.rst', 'README.md', 'README.txt']
           if os.path.exists(a)]
long_description = "\n\n".join(READMES)
classifiers = [
    "Programming Language :: Python",
    "Topic :: Software Development"]
name = '{{cookiecutter.lname}}'
version = "1.0"
src_dir = 'src'
install_requires = []
extra_requires = {}
candidates = {}
entry_points = {
    # z3c.autoinclude.plugin": ["target = plone"],
    # "console_scripts": ["foo = foo:main"],
}
setup(name=name,
      version=version,
      namespace_packages=[],
      description=name,
      long_description=long_description,
      classifiers=classifiers,
      keywords="",
      author="foo",
      author_email="foo@foo.com",
      url="{{cookiecutter.git_project_url}}",
      license="GPL",
      packages=find_packages(src_dir),
      package_dir={"": src_dir},
      include_package_data=True,
      install_requires=install_requires,
      extras_require=extra_requires,
      entry_points=entry_points)
# vim:set ft=python:
