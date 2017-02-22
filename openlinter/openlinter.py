#!usr/bin/env python3
"""
openlinter.py

Early implementation for an open source project linter.

See https://github.com/OpenNewsLabs/open-project-linter/issues/21 .
"""

from __future__ import absolute_import

import argparse
import os
import yaml

import openlinter.rules as rules

# FIXME: this is all not very functional or testable.
def main():
    # Set up parser and CLI
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
#    group.add_argument('-u', '--url',
#        help='The URL to the GitHub repository to check. Defaults to None.')
    group.add_argument('-d', '--directory', help="The local path to your repository's base directory. Defaults to the current working directory.",
       default=os.getcwd()
    )
    parser.add_argument('-r', '--rules', help='The path to the rules configuration file, a YAML file containing the rules you would like to check for. Defaults to current-working-directory/openlinter/rules.yml.',
        default=os.path.join(os.getcwd(), 'openlinter/rules.yml')
    )
    parser.add_argument('-v', '--version', action='version', version='0.2dev')
    args = parser.parse_args()

    # Read in rules
    with open(args.rules, 'r') as f:
        text = f.read()

    rule_set = yaml.safe_load(text)

    # Check directory/repository against rules
    if 'files_exist' in rule_set:
        """
        # TODO: Consider architecture: how to handle the result (print to stdout
        #       as we go, or pass around a result object?), how to handle interface
        #       strings (hard-coded or able to change/localize easily).
        """
        # FIXME: also unfortunately nested
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
                    # TODO: could wrangle this a bit
                    # brainwane/sumanah: should this say "no $name type file found"
                    #                    or list the individual ones not present?
                    elif result is None:
                        output = '! {} exists but is empty'.format(name,
                            args.directory)
                    else:
                        output = '! {} not found in {}'.format(name, args.directory)
                    print(output)

    if 'code_exists' in rule_set:
        code_exists = rules.check_for_code(args.directory)
        if code_exists:
            output = '  code files detected'
        else:
            output = '! no code files found'
        print(output)

    if 'version_control' in rule_set:
        vcs = rules.detect_version_control(args.directory)
        if vcs:
            output = '  version control using {}'.format(vcs)
        else:
            output = '! version control system not detected'
        print(output)

    # Conditionals may need work here, TODO
    if 'detect_git_branches' in rule_set['version_control'] and vcs == 'git':
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

    # Conditionals may need work here, TODO
    if 'multiple_git_commits' in rule_set['version_control'] and vcs == 'git':
        multiple_commits = rules.check_for_multiple_commits(args.directory)
        if multiple_commits:
            output = '  multiple commits on a branch found'
        else:
            output = '! one or fewer commits on each branch'
        print(output)

    elif 'detect_git_branches' in rule_set['version_control']:
        print('! no git repository detected, could not check for git branches')

    else:
        pass

    # TODO: can add future checks, also needs refactoring


if __name__ == '__main__':
    main()
