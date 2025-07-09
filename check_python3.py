#!/usr/bin/env python3
# Python 3 compatibility check for garage door controller

import sys
import importlib.util

def check_python_version():
    if sys.version_info[0] < 3:
        print("Error: Python 3 required. You are using Python {}.{}.".format(
            sys.version_info[0], sys.version_info[1]))
        print("Please run this script with Python 3.")
        return False
    else:
        print("Python version: {}.{}.{}".format(
            sys.version_info[0], sys.version_info[1], sys.version_info[2]))
        return True

def check_module(module_name):
    print(f"Checking for {module_name}...", end="")
    if importlib.util.find_spec(module_name) is not None:
        print(" Found!")
        return True
    else:
        print(" Not found!")
        return False

if __name__ == "__main__":
    if not check_python_version():
        sys.exit(1)
    
    print("\nChecking required modules:")
    required_modules = ["flask", "RPi.GPIO", "OpenSSL", "flask_cors"]
    missing_modules = []
    
    for module in required_modules:
        if not check_module(module):
            missing_modules.append(module)
    
    if missing_modules:
        print("\nMissing modules:")
        print("  " + "\n  ".join(missing_modules))
        print("\nPlease install missing modules with:")
        print("  pip3 install -r requirements.txt")
        sys.exit(1)
    else:
        print("\nAll required modules are installed!")
        print("Your system is ready to run the garage door controller.")
