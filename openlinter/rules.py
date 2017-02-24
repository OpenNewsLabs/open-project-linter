#!usr/bin/env python3
"""
rules.py

Functions that the project linter can use to check whether the project
meets desired criteria. Generally called in `openlinter.py`.

Functions
---------
check_file_presence
    Checks whether a directory contains a file whose name contains a keyword.

check_for_code
    Returns True if a directory contains a "code"-containing file.

check_for_develop_branch
    Returns True if a repository contains a branch with a certain name.

check_for_file_content
    Returns True if a directory contains at least one "code" file.

check_for_multiple_commits
    Returns True if a git repository has at least one branch with more than
    one commit.

check_multiple_branches
    Returns True if a git repository has more than one branch.

detect_version_control
    Identifies the version control system, if any. Currently checks for git.

get_file_text
    Returns the text of a given file, if it has UTF-8-decodable text.

guess_code_present
    Uses Pygments to guess for the type of code in a file.


Constants
---------
NOT_CODE
    lexer.name from the Pygments lexers that correspond to "structured
    text", not "code".
"""
import os

import git
import pygments.lexers as lexers

# Pygments lexer names that will parse files that are not code
NOT_CODE = ['markdown','BBCode', 'Groff', 'MoinMoin/Trac Wiki markup',
            'reStructuredText', 'TeX','Gettext Catalog', 'HTTP', 'IRC logs',
            'Todotxt']

def check_file_presence(keyword, directory):
    """Checks whether a given directory contains a file whose name contains
    a given keyword and whether that file has content.

    Parameters
    ----------
    keyword : string
        a string containing the term to search for
    directory : string
        a string containing the path to the directory to search in

    Returns
    -------
    boolean or None
        True if the keyword is found in the filenames present in
            the directory and the corresponding file has content
        None if the keyword is found in the filenames present in the
            directory but the file has size 0 B
        False if the keyword is not found in the filenames
            present in the directory
    """
    # TODO: minor refactoring, this should be a separate check than
    # the check for file content, should not return True/None/False
    files = os.listdir(directory)
    # this is unfortunately nested, FIXME?
    for f in files:
        if os.path.isfile(os.path.join(directory, f)):
            # in case there's anything in the path that matches keyword,
            # only match the filename
            filename = os.path.split(f)[1]
            if keyword in filename:
                if check_for_file_content(os.path.join(directory,f)):
                    return True
                else:
                    return None
    # if loop finishes, file name not found
    return False


def check_for_file_content(filepath):
    """Check whether a given file has content (is > 0 bytes).

    Parameters
    ----------
    filepath : string
        Path to the file to check for content.

    Returns
    -------
    boolean
        True if the file size is > 0 bytes, False otherwise

    Raises FileNotFound error if there is no file at the given path.
    """
    return os.path.getsize(filepath) > 0


def check_for_code(directory):
    """Check whether a directory contains at least one file that is
    likely to be code (as judged by Pygment's guess_lexer functionality).

    Parameters
    ----------
    directory : string
        Path to a directory.

    Returns
    -------
    boolean
        True if the directory probably has code files, False otherwise.
    """
    code_present = False
    for root, dirs, files in os.walk(directory):
        for f in files:
            code_present = guess_code_present(os.path.join(root, f))
            if code_present:
                return True
    return False

def guess_code_present(filepath):
    """Guess whether a file contains "code" or not. Structured text
    (as listed in NOT_CODE) does not count as "code", but anything else
    that the Pygments lexer-guesser finds a probable lexer for counts
    as "code" for these purposes.

    Parameters
    ----------
    filepath : string
        Path to the file that may contain code.
    Returns
    -------
    boolean
        True if the file contains "code" (as a best guess), False otherwise
    """
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
    """Return the text of a file in a given location, if it has text.

    Parameters
    ----------
    filepath : string
        Path to file to read

    Results
    -------
    string
        String containing text of file (Unicode string, UTF-8 decoded)

    Raises
    ------
    FileNotFoundError if there is no file at filepath
    """
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except UnicodeDecodeError:
        return None


def detect_version_control(directory):
    """Check for repository subfolders to detect whether a directory is
    under version control.

    Parameters
    ----------
    directory : string
        Path to directory

    Results
    -------
    string or None
        Returns a string containing the name of the version control
        system, or None if none of the systems checked for are found
        Current possibilities: 'git'
    """
    # possibly in the future could recurse and see if it's a subfolder?
    version_control_system = None

    if os.path.isdir(os.path.join(directory, '.git/')):
        version_control_system = 'git'

    # Could add checks for others here: CVS, svn, hg

    return version_control_system


def check_multiple_branches(repository):
    """Check whether a git repository has more than one branch.

    Parameters
    ----------
    repository : string
        Path to a git repository

    Results
    -------
    boolean
        True if the repository has more than 1 branch, False otherwise

    Raises
    ------
    git.InvalidGitRepositoryError if repository is a path to a directory
        but not a git repository
    git.NoSuchPathError if repository is not a path to a directory
    """
    repo = git.Repo(repository)
    branches = repo.branches
    if len(branches) > 1:
        return True
    else:
        return False


def check_for_develop_branch(repository, dev_branch_name):
    """Check whether a git repository has a branch with a specific name.

    Parameters
    ----------
    repository : string
        Path to a git repository

    dev_branch_name : string
        Desired branch name to check for

    Results
    -------
    boolean
        True if any of the repository's branches are named dev_branch_name

    Raises
    ------
    git.InvalidGitRepositoryError if repository is a path to a directory
        but not a git repository
    git.NoSuchPathError if repository is not a path to a directory
    """
    repo = git.Repo(repository)
    branches = repo.branches
    for branch in branches:
        if dev_branch_name in branch.name:
            break
    else:
        return False

    return True


def check_for_multiple_commits(repository):
    """Check for multiple commits on a branch in a given git repository.

    Parameters
    ----------
    repository : string
        Path to a git repository

    Results
    -------
    boolean
        True if any branch in the repository has more than one commit

    Raises
    ------
    git.InvalidGitRepositoryError if repository is a path to a directory
        but not a git repository
    git.NoSuchPathError if repository is not a path to a directory
    """
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
