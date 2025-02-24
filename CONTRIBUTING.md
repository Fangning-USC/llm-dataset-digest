# Contributing to Llm Dataset Digest

Welcome to the Llm Dataset Digest! Our project
is licensed under [TGS license],
and we warmly welcome all forms of contributions - from bug reports,
feature ideas, to pull requests. This guide will assist you in making
your contribution valuable and seamless.

Here are some key resources for your quick reference:

- [Source Code]
- [Documentation]
- [Work Items]

[tgs license]: https://dev.azure.com/TGSCloud/Datascience/_git/llm-dataset-digest?path=/LICENSE
[source code]: https://dev.azure.com/TGSCloud/Datascience/_git/llm-dataset-digest
[documentation]: https://dsdocs.cloud.tgs.com/llm-dataset-digest/source/index.html
[work items]: https://dev.azure.com/TGSCloud/Datascience/_workitems/

## Bug Reporting Guide

If you find a bug, please raise an issue in [work items].
When filing an issue, make sure to answer these questions:

Should you encounter a bug, we appreciate your contribution in
[reporting it here](work items). Please provide the following
information to expedite the resolution process:

- Operating System and Python version.
- Version of Llm Dataset Digest you are using.
- Action description leading to the bug.
- Your expected and actual outcomes.
- A minimal Python code snippet or detailed reproduction guide.

Format your code using markdown for better readability:

````markdown
```python
import llm_dataset_digest

for a in range(5):
    print(a)

# rest of your code.
```
````

## Suggesting Features

Feature requests can be submitted through [work items].

## Contributing Code or Documentation

### Cloning the Repository

Clone the repository using git, and add the remote branch.

```shell
$ git clone https://dev.azure.com/TGSCloud/Datascience/_git/llm-dataset-digest
$ cd llm-dataset-digest
$ git remote add origin https://dev.azure.com/TGSCloud/Datascience/_git/llm-dataset-digest
```

### Set Up Development Environment

To work with the Llm Dataset Digest source code, it is
recommended to use [Poetry] to install and manage all of
Llm Dataset Digest dependencies.

First, ensure Python 3.10+ is installed, along with the following tools:

- [Poetry]
- [Tox]

With the tools in place, navigate to the root of the cloned
Llm Dataset Digest repository and follow these
instructions:

> ℹ️ **Virtual Environment Configuration**
> By default, Poetry will generate the virtual environment in a
> folder within your home directory. If you prefer to create the
> virtual environment inside your project directory, specifically
> in a folder named .venv, we suggest configuring this through the
> global Poetry configuration. Here's the recommended command:
>
> ```shell
> poetry config virtualenvs.in-project true
> ```

Install the package and its dependencies in a virtual environment:

```shell
$ poetry install
```

If you'll be using notebooks during development, you can install the
optional notebook dependency group:

```shell
$ poetry install --with notebook
```

You can now run an interactive Python session or use the command-line
interface:

```shell
$ poetry run python
$ poetry run llm-dataset-digest
```

Verify your development environment is functioning correctly by running
the unit tests:

```shell
$ tox -e py
```

To add or update dependencies, utilize the [Poetry] command-line
interface. For details, consult the [Poetry] documentation. Some
examples:

```shell
$ poetry add new_dependency
$ poetry add new_dev_dependency@version --group dev
```

[poetry]: https://python-poetry.org/
[tox]: https://tox.wiki/

### Creating and Managing Branches

Before starting any new task or submitting a pull request, we suggest
opening an item in [work items] to discuss the bug fix or feature
you'd like to implement.

Synchronize your local copy with the origin (remote) repository,
then create a new, separate branch for each piece of work you want to do.

```shell
$ git checkout main
$ git fetch origin
$ git rebase origin/main
$ git push
$ git checkout -b shiny-new-feature
$ git push -u origin shiny-new-feature
```

To update this branch with latest code from Llm Dataset Digest,
you can fetch changes from the main branch and perform a rebase:

```shell
$ git fetch origin
$ git rebase origin/main
```

This will replay your commits on top of the latest
Llm Dataset Digest git main. Alternatively, you can merge
the changes in from origin/main instead of rebasing, which can
sometimes be simpler:

```shell
$ git fetch origin
$ git merge origin/main
```

If any merge conflicts occur, resolve them before submitting a pull request.

### Running Tests

To execute the full test suite:

```shell
$ tox
```

To list the available Tox sessions:

```shell
$ tox list
```

You can also run a specific Tox session. For example, invoke the unit
test suite for all Python versions, run this:

```shell
$ tox -e py
```

This action will execute the tests and save a coverage report.

Unit tests are located in the _tests_ directory, and are written using
the [pytest] testing framework.

[pytest]: https://pytest.readthedocs.io/

### Maintaining Code Quality

We recommend installing `pre-commit` as a Git hook to check code formatting
and linting before committing your changes:

```shell
$ pre-commit install
```

It is recommended to open an issue before starting work on anything.
This will allow a chance to talk it over with the owners and validate
your approach.

### Testing Coverage

Llm Dataset Digest maintains 100% test coverage. Ensure
your contributions maintain this standard. To check coverage, run:

```shell
$ tox -e py,coverage
```

This command will run the test suite with coverage and produce a coverage report.

### Building Documentation

User-facing classes and functions need to adhere to the [Google Style] for docstrings,
with sections specifically dedicated to Parameters and Examples. It's crucial that
all examples are executable and pass as doctests. By using [Tox] to run the test suite,
doctests are also executed.

For documentation, Llm Dataset Digest employs [MkDocs]. The documentation
is written using Markdown (.md files) located in the `docs` folder. This
documentation comprises both narrative and API documentation. It's important to include
all user-facing classes and functions in the API documentation, found under the
`docs/reference.md`. The API documentation will be automatically generated from
docstrings using [mkdocstrings]. Remember to incorporate any modifications in the release
notes, located in `CHANGELOG.md`.

The documentation can be built locally by running:

```shell
$ tox -e docs-build
$ open site/index.html
```

The built documentation will be accessible in the `./site` directory upon completion.

[MkDocs] can also serve a live version of the documentation. If you're editing the
documentation and want it to auto-update with every change you make, initiate the
session as follows:

```shell
$ tox -e docs
```

[mkdocs]: https://www.mkdocs.org/
[mkdocstrings]: https://mkdocstrings.github.io/python/
[google style]: https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings

## Submitting Changes

To propose modifications to this project, please initiate a [pull request].

The following are the prerequisites for your pull request to be considered:

- Your submission should pass the entire [Tox] test suite without any errors or warnings.
- Ensure that you incorporate unit tests, as this project aims for a full 100% code coverage.
- In case your modifications introduce new features, make sure to update the documentation accordingly.
- Make sure that changes have been properly documented in "Unreleased" section of `CHANGELOG.md`.

Please don't hesitate to submit early as we can always refine it through collaboration.

[pull request]: https://dev.azure.com/TGSCloud/Datascience/_git/llm-dataset-digest/pullrequests

## Release Procedure

### When to Make a Release

Ideally, release bug fixes that don't modify the public API immediately whenever possible.
Micro releases containing just a single bug fix are acceptable.

The decision for a minor release is left to the judgement of the core developers. There are
no strict guidelines - it's perfectly acceptable to initiate a minor release to introduce a
single new feature, just as it's okay to include several modifications in such a release.

Major updates, due to their potential to disrupt existing code or impact data compatibility,
require careful thought and planning. These updates should be as rare as possible to avoid
unnecessary disruptions.

### Publishing a New Release

Creating a version tag triggers the release process.

Ensure that `CHANGELOG.md` contains adequate documentation for all pull
requests to be included in the release prior to deployment.

First ensure the `main` branch `pyproject.toml` has the correct version. To
ensure consistency, we can use [poetry version] command to bump the version.

To initiate a new release, navigate to [source code] and generate a new tag. The
tag should consist of the version number, prefixed by a 'v' (for instance, v0.0.1).
Use suitable suffixes for pre-releases (such as v0.0.1a1 or v0.0.1rc2).

Assign the following description to the release tag:

```markdown
Changelog: https://dsdocs.cloud.tgs.com/llm-dataset-digest/source/changelog.html
```

Upon creation of the tag, the wheel is automatically uploaded to the
Datascience [Azure Artifacts Feed].

[poetry version]: https://python-poetry.org/docs/cli/#version
[azure artifacts feed]: https://dev.azure.com/TGSCloud/Datascience/_artifacts/feed/Datascience
