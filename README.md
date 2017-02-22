# Open Project Linter

##About this project
The Open Project Linter is an automated checklist that new (or experienced
but forgetful) open source maintainers can use to make sure that they're
using good practices in their documentation, code, and project resources.

The project started as a way to automate
[this checklist for newsroom developers](https://docs.google.com/document/d/1kTtHAgzlyteODMia1JmIGbKkjGugxKMZfxoWEGdku_Q/edit#),
but these are good practices for most open source projects!

##Getting Started
###Installation
It is recommended that you use a virtual environment in order to avoid
dependency conflicts between projects. For more information,
[a tutorial on virtual environments](http://docs.python-guide.org/en/latest/dev/virtualenvs/).
Once you have set up a python3 virtual environment, activate the environment.
Then you can use pip to install Open Project Linter.
```
$ pip install open-project-linter
```
*NOTE:* until the first release, you will need to use the `--pre` flag when installing:
```
$ pip install --pre open-project-linter
```

Once you have installed the package, you should be able to run it from the
command line (see [Example usage](#Example usage)).

This may work with Python 2.7 as well, although Python 2 is not officially
supported.

###Example usage
Once you have installed the package, if you want to check a local repository,
make sure your virtual enviroment is activated and run:
```
$ openlinter -d path/to/repository/
```

For more help, run `$ openlinter --help`.

## Contributing
###How to set up the dev environment
To set this up for development, fork this repository, then clone it to
your development machine using `git clone`.

Once you've committed your changes and pushed them to your fork of the
repository, file a pull request to get your contribution into the main
repository.

##Changelog
###version 0.2dev
* Add automated tests
* Fix path bug in file content checker

###version 0.1dev
* Command-line application invokable with `openlinter`, with help on
  how to run it
* Given the path to a directory, checks for:
    * the existence of license, contributing, and readme files
    * the presence of code files in the directory and any subdirectories
    * the presence of a git repository, multiple branches,
      multiple commits on any branch, and a named development/feature branch
* Configurable via `rules.yml`

##Meta
Mozilla Open News - https://www.opennews.org/

Contributors:
* Frances Hocutt - https://franceshocutt https://github.com/fhocutt/
* Sumana Harihareswara - https://changeset.nyc

The Open Project Linter is available under v. 2.0 of the Apache license.
See `LICENSE` for more information.
