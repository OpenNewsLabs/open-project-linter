#!usr/bin/env python3
"""
rules.py

Early implementation for criteria for the linter to check the project against.

See https://github.com/OpenNewsLabs/open-project-linter/issues/21 .
"""

import os

# TODO: consider object structure for results
# TODO: consider errors/failure modes

def check_readme(directory):
    result = check_file_presence('README', directory)


def check_license(directory):
    result = check_file_presence('LICENSE', directory)

def check_file_presence(filename, directory):
    # check files in directory against given filename
    # this will require mucking with os to read dir contents
    # return true/false if found
    # probably check for case-insensitive substring of file names
    pass
