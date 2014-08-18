# =============================================================================
#     Author: Pyran
#     Date:   July 2, 2014
#     Taken From: https://github.com/pyran
#     File:  setup.py
#     Description: This is the cx_Freeze setup file for creating an exe program
# =============================================================================
from cx_Freeze import setup, Executable
# NOTE: you can include any other necessary external imports here aswell
 
includefiles = [] # include any files here that you wish
includes = []
excludes = []
packages = []
 
exe = Executable(
 # what to build
   script = "sgrid.py", # the name of your main python script goes here 
   initScript = None,
   base = None, # if creating a GUI instead of a console app, type "Win32GUI"
   targetName = "sgrid.exe", # this is the name of the executable file
   copyDependentFiles = True,
   compress = True,
   appendScriptToExe = True,
   appendScriptToLibrary = True,
   icon = None # if you want to use an icon file, specify the file name here
)
 
setup(
 # the actual setup & the definition of other misc. info
    name = "Space Grid", # program name
    version = "0.1",
    description = 'A modular text adventure engine',
    author = "Pyran",
    author_email = "pyran@users.noreply.github.com",
    options = {"build_exe": {"excludes":excludes,"packages":packages,
      "include_files":includefiles}},
    executables = [exe]
)
