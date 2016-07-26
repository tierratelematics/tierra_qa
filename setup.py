from setuptools import setup, find_packages
import os

version = '0.0.1dev'


setup(name='tierra_qa',
      version=version,
      description="Tierra QA",
      long_description=open("README.md").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pytest",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: Apache Software License",
        ],
      keywords='',
      author='Tierra QA Team',
      author_email='DLQA@tierratelematics.com',
      url='http://tierratelematics.com',
      license='Apache License, Version 2.0',
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'pytest-selenium',
          'pytest-bdd',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      tierra_qa_clone = tierra_qa.scripts:tierra_qa_clone
      """,
      )
