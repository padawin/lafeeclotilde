#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup


setup(name='lafeeclotilde-api',
      version='0.0.1',
      description='lafeeclotilde-api',
      author='Ghislain Rodrigues',
      license='MIT',
      install_requires=[
          'flask',
          'flask-cors',
          'tornado',
          'psycopg2-binary'
      ],
      entry_points={
          'console_scripts': [
              'lafeeclotilde-api = app:main'
          ],
      },
      packages=[
          '.',
          'blueprints',
          'controller',
          'model',
          'service'
      ],
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Environment :: Console',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.6'
      ],
      zip_safe=True)
