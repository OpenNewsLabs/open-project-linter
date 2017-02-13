#!usr/bin/env python3
"""
rules.py

Early implementation for criteria for the linter to check the project against.

See https://github.com/OpenNewsLabs/open-project-linter/issues/21 .
"""

import os

import git


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
            if keyword.casefold() in filename.casefold():
                if check_for_file_content(os.path.join(directory,f)):
                    return True
                else:
                    return None

    # if loop finishes, file name not found
    return False


def check_for_file_content(filename):
    """Return True if the file has > 0 B, False otherwise."""
    # note this gives FileNotFoundError if there is no file at filepath
    return os.path.getsize(filename) > 0


def detect_version_control(directory):
    """Figure out whether the directory is under version control."""
    # possibly in the future could recurse and see if it's a subfolder?
    version_control_system = None

    if os.path.isdir(os.path.join(directory, '.git/')):
        version_control_system = 'git'

    # Could add checks for others here: CVS, svn, hg

    return version_control_system


def check_multiple_branches(repository):
    repo = git.Repo(repository)
    branches = repo.branches
    if len(branches) > 1:
        return True
    else:
        return False


def check_for_develop_branch(repository, dev_branch_name):
    repo = git.Repo(repository)
    branches = repo.branches
    for branch in branches:
        if dev_branch_name in branch.name:
            break
    else:
        return False

    return True


# TODO: figure out Head API, flesh this out
def check_for_multiple_commits(repository):
    repo = git.Repo(repository)
    branches = Repo.branches
    for branch in branches:
        pass

# TODO: figure out how to do this, flesh this out
def check_for_signed_commits(repository):
    repo = git.Repo(repository)
    branches = repo.branches
    for branch in branches:
        pass
