#!usr/bin/env python3
"""
rules.py

Early implementation for criteria for the linter to check the project against.

See https://github.com/OpenNewsLabs/open-project-linter/issues/21 .
"""

import os

# TODO: consider errors/failure modes

def check_file_presence(keyword, directory):
    """
    Checks whether a given directory contains a file whose name contains
    a given string, using case insensitive matching.

    Parameters
    ----------
    keyword : a string containing the term to search for
    directory: a string containing the path to the directory to search in

    Returns
    -------
    True if the keyword is found in the filenames present in
        the directory and the corresponding file has content
    None if the keyword is found in the filenames present in the
        directory but the file has size 0 B
    False if the keyword is not found in the filenames
        present in the directory
    """
    files = os.listdir(directory)
    # this is unfortunately nested, FIXME?
    for f in files:
        if os.path.isfile(f):
            # in case there's anything in the path that matches keyword,
            # only match the filename
            filename = os.path.split(f)[1]
            # FIXME, more complicated than it needs to be, could just
            # return False if it's empty or absent (probably)
            if keyword.casefold() in filename.casefold():
                if check_for_file_content(f):
                    return True
                else:
                    return None

    # if loop finishes, file name not found
    return False


def check_for_file_content(filename):
    """Return True if the file has > 0 B, False otherwise."""
    # note this gives FileNotFoundError if there is no file at filepath
    return os.path.getsize(filename) > 0
