# Roadmap for the Open Project Linter
## Project Mission and Summary
The Open Project Linter is an automated checklist that new (or experienced but
forgetful) open source maintainers can use to make sure that they're using
good practices in their documentation, code, and project resources.

The project started as a way to automate
[this checklist for newsroom developers](https://docs.google.com/document/d/1kTtHAgzlyteODMia1JmIGbKkjGugxKMZfxoWEGdku_Q/edit#),
but these are good practices for most open source projects!

## How to Get Involved
Right now, this project is being implemented by Frances Hocutt (@fhocutt) and
Sumana Harihareswara (@brainwane, Changeset Consulting), under contract. If you
want to volunteer to contribute, comment on an issue you're interested in and
ping @brainwane.

## Milestones
Version 1.0 of this tool will be recommended and promoted at
[NICAR](https://www.ire.org/conferences/nicar2017/).

### Short-term
* Fix any bugs that come up during NICAR

### Medium-term
These are the highest-priority additions and improvements.

#### Features
* Add functionality/rules to check for secrets, passwords, keys, and personally
  identifiable information ([#17](https://github.com/OpenNewsLabs/open-project-linter/issues/17))
* Add functionality/rules to check for offensive words in code, comments, and
  documentation ([#18](https://github.com/OpenNewsLabs/open-project-linter/issues/18))
* Add functionality/rules to check whether a git commit is signed with GPG ([#19](https://github.com/OpenNewsLabs/open-project-linter/issues/19))
* Add functionality/rules to check whether a package is signed with GPG ([#20](https://github.com/OpenNewsLabs/open-project-linter/issues/20))

#### Code Improvements
* Refactor to add results to a result object as checks are run instead of only
  printing to stdout
* Ensure that interface messages are stored together and are easy to find
  and modify

### Ideas for the future
Future maintainers and community should decide what their priorities are,
but here are some possible improvements. These are components that could be
added in the future, but are not part of current development efforts. They
involve inessential improvements or more involved work.

#### Features
* Add the ability to check a repository via the Github URL ([#6](https://github.com/OpenNewsLabs/open-project-linter/issues/6))
* Add the ability to check that a Github project is using milestones ([#16](https://github.com/OpenNewsLabs/open-project-linter/issues/16))
* Automated license detection

#### Interface improvements
* Improve console string formatting
* Consider which options belong in the config file vs. the command-line
  interface
* Improve the message text for help and other interface messages
* Add a verbosity option (e.g. show all output vs. show only errors)
* Save the results to a file instead of only printing in the terminal

#### Code improvements/technical debt
* Improve automated test coverage
* Make compatible with Python 2.7
* Make compatible with Windows
* Use path/Path functions for all filepath manipulations (not just strings)
* As the number of rules grows, split functions out into separate submodules
* As the number of automated tests grows, split them into files containing
  similar tests
* Consider separating functions that support rules/linter implementation (that
  do not implement the main logic) into a utils submodule
