#!usr/bin/env python3
"""
openlinter.py

Early implementation for an open source project linter.

See https://github.com/OpenNewsLabs/open-project-linter/issues/21 .
"""

import argparse
import os
import yaml

import rules

# FIXME: this is all terribly procedural and not very functional or testable.
def main():
    # Set up parser and CLI
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-u', '--url',
        help='The URL to the GitHub repository to check. Defaults to None.')
    group.add_argument('-d', '--directory', help="The local path to your repository's base directory. Defaults to the current working directory.",
       default=os.getcwd()
    )
    parser.add_argument('-r', '--rules', help='The path to the rules configuration file, a YAML file containing the rules you would like to check for. Defaults to current-working-directory/openlinter/rules.yml.',
        default=os.path.join(os.getcwd(), 'openlinter/rules.yml')
    )
    parser.add_argument('--version', action='version', version='0.1dev')
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
        for f in rule_set['files_exist']:
            for item in f:
                 result = rules.check_file_presence(f[item], args.directory)
                 if result:
                     output = '  {} exists and has content.'
                 elif result is None:
                     output = '! {} exists but is empty.'
                 else:
                     output = '! {} not found in {}.'

                 # print result to stdout
                 print(output.format(f[item], args.directory))

    if 'version_control' in rule_set:
        vcs = rules.detect_version_control(args.directory)
        if vcs:
            output = '  version control using {}'.format(vcs)
        else:
            output = '! version control system not detected'
        print(output)

    if 'detect_git_branches' in rule_set['version_control'] and vcs == 'git':
        branches = check_for_git_branches(args.directory)
        develop = check_for_develop_branch(args.directory, 'develop')

    # TODO: make this the same as other feedback
    print('branches: {}, develop: {}'.format(branches, develop))


    elif 'detect_git_branches' in rule_set['version_control']:
        print('! no git repository detected, could not check for git branches')
    else:
        pass

    # TODO: can add future checks, also needs refactoring


if __name__ == '__main__':
    main()
