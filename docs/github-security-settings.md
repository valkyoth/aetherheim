# GitHub Security Settings

Repository administrators must enable:

- private vulnerability reporting;
- secret scanning and push protection where available;
- Dependabot alerts and security updates;
- branch protection with required CI review;
- CodeQL analysis default setup.

CodeQL default setup is the selected configuration. Do not add an advanced
CodeQL workflow while it is enabled. Review CodeQL and dependency alerts before
every release tag.
