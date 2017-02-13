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
Version 1.0 of this tool is due to be finished in mid-February, so that it can
be tested ahead of being recommended and promoted at [NICAR](https://www.ire.org/conferences/nicar2017/).
### Short-term
These will be finished by 15 Feb 2017.

Currently in progress:
* Write a README documenting package purpose, installation, and usage.
* Write a CONTRIBUTING file with how to get involved.
* Write tests for currently available functionality, beginning with
  rules
* Package the application so it is installable through pip; keep `requirements.txt`
  up to date. (#1)

Not currently in progress:
* Add the ability to check a repository via the Github URL (#6)
* Add the ability to check that a Github project is using milestones (#16)
* Refactor to add results to a result object as checks are run instead of only
  printing to stdout.
* Implement code detection (is code in the repository?) (#9)
* Publish project on PyPI (#2)

### Medium-term
These could be worked on now, but are not in progress. They may or may not be
finished by 15 Feb 2017.

* Improve the message text for help and other interface messages
* Ensure that interface messages are stored together and are easy to find
  and modify 
* Add functionality/rules to check for secrets, passwords, keys, and personally
  identifiable information (#17)
* Add functionality/rules to check for offensive words in code, comments, and
  documentation (#18)
* Add functionality/rules to check whether a git commit is signed with GPG (#19)
* Add functionality/rules to check whether a package is signed with GPG (#20)

### Long-term
These are components that could be added in the future, but are not part of
current development efforts. They involve inessential improvements or more
involved work.
* Automated license detection
* Save the results to a file instead of only printing in the terminal
