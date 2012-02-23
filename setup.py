# Copyright (c) 2008 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id: setup.py 44106 2010-07-29 11:12:54Z sylvain $

from setuptools import setup, find_packages
import os

version = '1.1.2dev'

setup(name='silva.system.utils',
      version=version,
      description="command line utils to manage Silva sites",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
          "Environment :: Web Environment",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: Zope Public License",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Framework :: Zope2",
          ],
      keywords='system utils silva',
      author='Infrae',
      author_email='info@infrae.com',
      url='https://hg.infrae.com/silva',
      license='BSD',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      namespace_packages=['silva', 'silva.system'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'Zope2',
        'argparse',
        'infrae.wsgi',
        'setuptools',
        'silva.core.interfaces',
        'silva.core.services',
        'zope.location',
        'zope.security',
        'zope.site',
        ],
      entry_points = """
      [console_scripts]
      silva = silva.system.utils.script:script [script]
      [silva.system.utils]
      listing = silva.system.utils.commands.listing:ListingCommand
      clear_version = silva.system.utils.commands.version:CleanupVersionCommand
      convert_files = silva.system.utils.commands.file:ConvertFileCommand
      pack = silva.system.utils.commands.pack:PackCommand
      find_sources = silva.system.utils.commands.sources:FindSourcesCommand
      """
      )
