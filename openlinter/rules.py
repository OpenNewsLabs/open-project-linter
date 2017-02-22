#!usr/bin/env python3
"""
rules.py

Early implementation for criteria for the linter to check the project against.

See https://github.com/OpenNewsLabs/open-project-linter/issues/21 .
"""

import os

import git
import pygments.lexers as lexers

# Pygments lexer names that will parse files that are not code
NOT_CODE = ['markdown','BBCode', 'Groff', 'MoinMoin/Trac Wiki markup',
            'reStructuredText', 'TeX','Gettext Catalog', 'HTTP', 'IRC logs',
            'Todotxt']

def check_file_presence(keyword, directory):
    """
    Checks whether a given directory contains a file whose name contains
    a given string.

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
        if os.path.isfile(os.path.join(directory, f)):
            # in case there's anything in the path that matches keyword,
            # only match the filename
            filename = os.path.split(f)[1]
            if keyword in filename:
                return True
    # if loop finishes, file name not found
    return False


def check_for_file_content(filepath):
    """Return True if the file has > 0 B, False otherwise."""
    # note this gives FileNotFoundError if there is no file at filepath
    return os.path.getsize(filepath) > 0


def check_for_code(directory):
    """Return True if a code file is present (not just structured text)."""
    code_present = False
    for root, dirs, files in os.walk(directory):
        for f in files:
            code_present = guess_code_present(os.path.join(root, f))
            if code_present:
                return True
    return False

def guess_code_present(filepath):
    text = get_file_text(filepath)
    filename = os.path.split(filepath)[1]
    try:
        lexer = lexers.guess_lexer_for_filename(filename, text)
        if lexer.name not in NOT_CODE:
            return True
        else:
            return False
    except lexers.ClassNotFound:
        return False


def get_file_text(filepath):
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except UnicodeDecodeError:
        return None


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


def check_for_multiple_commits(repository):
    """ Return True if any branch has more than 2 commits ( in git log)"""
    repo = git.Repo(repository)
    branches = repo.branches
    multiple_commits = False
    for branch in branches:
        commit_log = [x for x in branch.log() if 'commit' in x.message]
        if len(commit_log) > 1:
            multiple_commits = True
    return multiple_commits


# TODO: figure out how to do this, flesh this out
def check_for_signed_commits(repository):
    repo = git.Repo(repository)
    branches = repo.branches
    for branch in branches:
        pass
