#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup


setup(name='lafeeclotilde-admin',
      version='0.0.1',
      description='lafeeclotilde-admin',
      author='Ghislain Rodrigues',
      license='MIT',
      install_requires=[
          'flask',
          'tornado',
          'requests'
      ],
      entry_points={
          'console_scripts': [
              'lafeeclotilde-admin = app:main'
          ],
      },
      packages=[
          '.',
          'blueprints',
          'controller',
          'static',
          'templates'
      ],
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Environment :: Console',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.6'
      ],
      zip_safe=True)
