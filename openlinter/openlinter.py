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

def main():
    # Set up parser and CLI
    parser = argparse.ArgumentParser()
    # TODO: make these mutually exclusive
    parser.add_argument('--url',
        help='The URL to the GitHub repository to check. Defaults to none.')
    parser.add_argument('--dir', help="The local path to your repository's base directory. Defaults to the current working directory.",
       # default=TODO, you can get this with os
    )
    parser.add_argument('--rules', help='The path to the rules config file, a YAML(???tktk) file containing the rules you would like to check for. Defaults to tktkTODO',
        # default=TODO (cwd/rules.yml for now)
    )
    parser.parse_args()

    # Identify directory/repository

    # Read in rules
    # parse the YAML to call them probably

    # Check directory/repository against rules
    # This should return some sort of pass/fail + message result

    # Print results to stdout


if __name__ == '__main__':
    main()
