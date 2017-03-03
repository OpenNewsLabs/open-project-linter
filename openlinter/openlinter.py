#!usr/bin/env python3
"""
openlinter.py

Console entry point for the openlinter package.

Functions
---------
main
    Main function of the linter--set up state and call checks.

get_current_script_dir
    Inspect the stack to find the directory the current module is in.

parse_linter_args
    Parse command-line arguments and set up the console interface.

get_rule_set
    Read and parse the configuration file.

check_for_git_branches
    Call the checks related to git branching and print the results.

check_multiple_git_commits
    Call the check for multiple commits per branch and print the result.
"""

from __future__ import absolute_import

import argparse
import inspect
import os

import yaml

import openlinter.rules as rules


# FIXME: this could be more functional and testable.
def main():
    # Get command-line args and configuration data
    args = parse_linter_args()
    rule_set = get_rule_set(args)

    # Check directory/repository against rules
    #######
    # TODO: Consider architecture: how to handle the result (print to stdout
    #       as we go, or pass around a result object?), how to handle interface
    #       strings (hard-coded or able to change/localize easily).
    #######

    # Check for the presence of specified files
    if 'files_exist' in rule_set:
        # FIXME: also unfortunately nested, breaking out functions will help
        for files_to_check in rule_set['files_exist']:
            for f in files_to_check:
                for name in files_to_check[f]:
                    result = rules.check_file_presence(name, args.directory)
                    # If one exists with content, great, stop checking
                    if result:
                        output = '  {} exists and has content'.format(name)
                        print(output)
                        break
                    # Otherwise note that none of the names exist?
                    elif result is None:
                        output = '! {} exists but is empty'.format(name,
                            args.directory)
                    else:
                        output = '! {} not found in {}'.format(name, args.directory)
                    print(output)

    # Check for the presence of any code
    if 'code_exists' in rule_set:
        code_exists = rules.check_for_code(args.directory)
        if code_exists:
            output = '  code files detected'
        else:
            output = '! no code files found'
        print(output)

    # Check for the presence of version control and git repo features
    if 'version_control' in rule_set:
        vcs = rules.detect_version_control(args.directory)
        if vcs:
            output = '  version control using {}'.format(vcs)
        else:
            output = '! version control system not detected'
        print(output)

        # Might be better with a try/except with git.InvalidGitRepositoryError
        if 'detect_git_branches' in rule_set['version_control'] and vcs == 'git':
            git_branch_info = check_for_git_branches(args, rule_set)
        elif 'detect_git_branches' in rule_set['version_control']:
            print('! no git repository detected, could not check for git branches')
        else:
            pass

        if 'multiple_git_commits' in rule_set['version_control'] and vcs == 'git':
            # Currently doesn't return anything
            multiple_commits = check_multiple_git_commits(args)
        elif 'multiple_git_commits' in rule_set['version_control']:
            print('! no git repository detected, could not check for multiple commits')
        else:
            pass

    #######
    # Checks with new rules get added here
    #######


def get_current_script_dir():
    """Inspect the stack to find the directory the current module is in.

    Returns
    -------
    string
        a string containing the path to the module location
    """
    module_location = os.path.abspath(inspect.stack()[0][1])
    return os.path.dirname(module_location)


def parse_linter_args():
    """Parse command-line arguments and set up the command-line
    interface and help.

    Defaults to current working directory for the directory arg and the
    copy of rules.py in the directory this module is in for the rules arg.

    Returns
    -------
    argparse.Namespace
        object subclass with arguments as attributes for each given argument
    """
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d', '--directory', help="The local path to your repository's base directory. Defaults to the current working directory.",
       default=os.getcwd()
    )
    parser.add_argument('-r', '--rules', help='The path to the rules configuration file, a YAML file containing the rules you would like to check for. Defaults to path/to/openlinter/rules.yml.',
        default=os.path.join(get_current_script_dir(), 'rules.yml')
    )
    parser.add_argument('-v', '--version', action='version', version='1.0')
    return parser.parse_args()


def get_rule_set(args):
    """Read and parse the config file at the location given when the
    linter script is run.

    Parameters
    ----------
    args : argparse.Namespace
        Arguments input when script is called from the console

    Returns
    -------
    dict
        Contains structured data from the parsed configuration file
    """
    with open(args.rules, 'r') as f:
        text = f.read()
    rule_set = yaml.safe_load(text)
    return rule_set


def check_for_git_branches(args, rule_set):
    """Call the checks related to git branching (multiple branches and
    appropriately named develop/feature branch) and print the results
    to stdout.

    Parameters
    ----------
    args : argparse.Namespace
        Arguments input when script is called from the console
    rule_set : dict
        Contains the structured data from the parsed configuration file

    Returns
    -------
    None
    """
    branches = rules.check_multiple_branches(args.directory)
    if branches:
        output = '  multiple git branches found'
    else:
        output = '! fewer than 2 git branches found'
    print(output)

    # check for a dev/feature branch
    # TODO: pull some of this out into a function
    develop = False
    for name in rule_set['dev_branch_names']:
        if rules.check_for_develop_branch(args.directory, name):
            develop = True
            output = '  development branch "{}" found'.format(name)
            print(output)
    if not develop:
        output = '! no development branch found'
        print(output)


def check_multiple_git_commits(args):
    """Call the check for multiple commits on a branch and print the
    result to stdout.

    Parameters
    ----------
    args : argparse.Namespace
        Arguments input when script is called from the console

    Returns
    -------
    None
    """
    multiple_commits = rules.check_for_multiple_commits(args.directory)
    if multiple_commits:
        output = '  multiple commits on a branch found'
    else:
        output = '! one or fewer commits on each branch'
    print(output)


if __name__ == '__main__':
    main()
