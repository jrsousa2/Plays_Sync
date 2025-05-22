# A dummy code just to force Github to classify this repo as a Python type
from cx_Freeze import setup, Executable
 
# Paths to include
include_files = ["D:\\Python\\iTunes" , "D:\\Python\\WMP", "D:\\Python\\Plays_Sync"]

# Dependencies are automatically detected, but it might need fine tuning.
build_options = {'packages': ["win32com.client"], 'excludes': ["sqlite3"], "include_msvcr": True}
 
import sys
base = 'Win32GUI' if sys.platform=='win32' else None
 
executables = [Executable("D:\\Python\\Plays_Sync\Main.py", base="Win32GUI", target_name = "Main.exe")]
 
setup(name="The Plays Sync Tool",
      version = "1.0",
      description = "Sync WMP and iTunes Plays",
      options = {'build_exe': build_options},
      executables = executables)
