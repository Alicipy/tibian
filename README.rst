Tibian
======

Project 'tibian', also known as the 'TIcket Birthday Announcer',
is a project to announce tickets that it's birthday today.
That means it announces ticket titles and summaries that were created a few
years ago and are still open to a number of channels that you specified before.
For example, the Jira tickets of a project can be published to a Teams channel
regularly and make some people happy (or angry).

Right now, the project is in a very early stage and it's not fully functional.

Installation + Usage
--------------------

To install the package, simply do::

    pip install tibian

which will install the package locally.

Then, configure the credentials and endpoints for your ticket and announcement
system as described in `Configuration`.

Afterwards, you can start the project by running the `tibian` command::

    tibian

Afterwards, it should announce the birthdays of tickets of the current date
as specified.

Configuration
-------------

The configuration file for the project must be located in the working directory
of the executed command. A short (any maybe not complete) description of
the configuration file is given in `config.example.yaml on GitHub`_.

Copy this to a file `config.yaml` in the current directory, add your credentials
and remove parts you don't need.

Detailed information about all config options will be given soon,
but for this version most of the configuration should be self-explanatory.

'type' is the type of source or target you have,
'name' is an internal used name for the source/target, and
'config' is a type-dependant dictionary of types as shown.


Versioning
-----------

We use `semantic versioning`_ to version the project. As we are in some sort of 'beta',
we may (but try not to) do some breaking changes between minor versions to fix some obvious
misbehavior of the project. For example, we may change the configuration file format or
add new options to the configuration file. As we try to prevent this and add a backlog how to
upgrade to newer versions, you maybe want to check the changelog before updating to new versions.


Development
-----------

We are always happy about active support. If you want to actively develop on tibian, follow the next few commands.
We use uv for the development of tibian. You can install it with the following command::

    pip install uv

To install all development dependencies, run::

    uv sync

Afterwards, you have all dependencies (including dev dependencies) installed in a virtualenv, and are able to develop.

To add new dependencies, run::

    uv add <package>

To activate your virtualenv, run::

    . ./venv/bin/activate

Afterwards, you can run all following commands in the virtualenv. In case you don't, you have to add 'uv run' before each
of the next commands to execute it in the virtualenv, or you will get missing requirements errors.

Additionally, we use `pre-commit`_ as our tool to enforce some styling and lint rules. To install pre-commit, run::

    pre-commit install

This will install all hooks and run them automatically on a commit. You can also run these rules manually by doing::

    pre-commit run --all

To run the tests and get some coverage information, run::

    ./scripts/run_tests.sh

.. _uv: https://docs.astral.sh/uv/
.. _pre-commit: https://pre-commit.com/
.. _semantic versioning: https://semver.org/
.. _config.example.yaml on GitHub: https://github.com/Alicipy/tibian/blob/main/config.example.yaml
