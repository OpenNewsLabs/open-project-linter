# Open Project Linter

##About this project
The Open Project Linter is an automated checklist that new (or experienced
but forgetful) open source maintainers can use to make sure that they're
using good practices in their documentation, code, and project resources.

The project started as a way to automate
[this checklist for newsroom developers](https://docs.google.com/document/d/1kTtHAgzlyteODMia1JmIGbKkjGugxKMZfxoWEGdku_Q/edit#),
but these are good practices for most open source projects!

This is written in and supported on Python 3.

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
Once you have installed the package, you should be able to run it from the
command line (see [Example usage](#Example usage)).

###Example usage
Once you have installed the package, if you want to check a local repository,
make sure your virtual enviroment is activated and run:
```
$ openlinter -d path/to/repository/
```

For more help, run `$ openlinter --help`.

####Using configuration files
Open Project Linter is configurable, so that you can decide what project
features you want to check for and what file names you want to make sure
exist. The default configuration file is located at
`path/to/openlinter/rules.yml`.

You can also use the `-r` flag to specify where your desired configuration file
is, like so:
```
$ openlinter -r path/to/rules.yml -d path/to/repository/
```
to use the file located at `path/to/rules.yml` to check the repository at
`path/to/repository/`.

## Contributing
###How to set up the dev environment
To set this up for development, fork this repository, then clone it to
your development machine using `git clone`.

Once you've committed your changes and pushed them to your fork of the
repository, file a pull request to get your contribution into the main
repository.

##Changelog
###version 1.0
* Update `ROADMAP.md` with pre-NICAR status
* Fix the KeyError issue when default config was changed ([#27](https://github.com/OpenNewsLabs/open-project-linter/issues/27))
* Split some of the main linter logic out into functions and improve module
  documentation
* Add test fixtures for the git-related tests ([#22](https://github.com/OpenNewsLabs/open-project-linter/issues/22))

###version 0.4dev
* Now installs Pygments automatically when installed with pip, with or
  without pulling versions from `requirements.txt`
* Now includes `rules.yml` in the package and uses a correct default path
  to it

###version 0.3dev
* Improve documentation
* Fix accidental return value change in file content checker

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

##About
This linter was designed and written by [Frances Hocutt](https://franceshocutt.com/cv/) via [Changeset Consulting](http://changeset.nyc/), a project management and maintainership consultancy focusing on open source. Sumana Harihareswara of Changeset Consulting attended the initial [OpenNews](https://opennews.org/) documentation sprint for [The Field Guide to Open Source in the Newsroom](http://fieldguide.opennews.org/) and suggested development of a companion tool to automate the guidebook's checklists as much as possible.

We look forward to seeing the community add new linter rules to help new maintainers.

##Contributors
* Frances Hocutt - https://franceshocutt.com https://github.com/fhocutt/
* Sumana Harihareswara - https://changeset.nyc

##License
The Open Project Linter is available under v. 2.0 of the Apache license.
See `LICENSE` for more information.
