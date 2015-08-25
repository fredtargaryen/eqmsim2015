# -*- coding: utf-8 -*-

# A simple setup script to create an executable using PyQt4. This also
# demonstrates the method for creating a Windows executable that does not have
# an associated console.
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

options = {'build_exe': {'includes': 'atexit', 
						'include_files':['assets/double arrow h.png',
											'assets/double arrow v.png',
											'assets/jamie\'s cross.png',
											'assets/jamie\'s tick.png']
						}
			}

executables = [Executable('gui/main.py', base=base)]

setup(name='Equilibrium Simulator 2015',
      version='1.1',
      description='Software for simulating reversible chemical reactions',
	  author='James Curran',
	  author_email='lggy@hotmail.co.uk',
	  url='https://github.com/fredtargaryen/eqmsim2015',
      options=options,
      executables=executables,
	  packages=['chem', 'gui'],
	  py_modules=['ReactionFile']
      )