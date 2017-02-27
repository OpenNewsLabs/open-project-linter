#Contributing to open-project-linter
## Summary
`open-project-linter` is an automated checklist that will make sure that your
open source project has the documentation and structure it needs to be
successful, and that it doesn't contain any information it shouldn't.

## How to get involved
To start with, this project is being implemented by Frances Hocutt (@fhocutt)
and Sumana Hariharewsara (@brainwane, [Changeset Consulting](https://changeset.nyc)),
under contract. If you want to volunteer to contribute, take a look at the
[project roadmap](https://github.com/OpenNewsLabs/open-project-linter/blob/master/ROADMAP.md)
and the [project issue tracker](https://github.com/OpenNewsLabs/open-project-linter/issues)
and then comment on an issue you're interested in. Or, ping @brainwane for more
information.

## Status and plans
See `ROADMAP.md` for more information.

## Specific guidelines
### Adding rules to the linter
To add rules, you will need to:
* add one or more entries to the configuration file (`rules.yml`) so that
  users can to turn the check on or off
* make sure that the rule is called from and output is generated for the body
  of the linter (in `openlinter.py`)
* add one or more functions to `rules.py` to actually run the check

### Adding options to the command-line interface
You may also want to add new options to the command-line interface. This uses
argparse: [argparse docs](https://docs.python.org/3.4/library/argparse.html),
[argparse tutorial](https://docs.python.org/3.4/howto/argparse.html).
