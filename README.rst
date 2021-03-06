cisco_olt_client
================

.. image:: https://travis-ci.org/Vnet-as/cisco-olt-client.png
   :target: https://travis-ci.org/Vnet-as/cisco-olt-client
   :alt: Latest Travis CI build status


.. image:: https://codecov.io/gh/Vnet-as/cisco-olt-client/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/Vnet-as/cisco-olt-client
   :alt: Test coverage status from latest build


.. image:: https://pyup.io/repos/github/vnet-as/cisco-olt-client/shield.svg
   :target: https://pyup.io/repos/github/vnet-as/cisco-olt-client/
   :alt: Updates


Python wrapper for cisco's olt boxes commands executed via ssh


Usage
-----

Get global dhcp config:

.. code-block:: python

    >>> from cisco_olt_client.client import OltClient
    >>> from cisco_olt_client.command import Command
    >>>
    >>> with OltClient('host', 'username', 'password') as client:
    ...     cmd = client.execute('/dhcp/global/show')
    ...     print(cmd.output)
    ...
    Global DHCP circuit ID Template String:
    "$accessnodeid PON $rack/$subrack/$slot/$port:$onuid.$svid"



Get type for each of configured services:

.. code-block:: python

    >>> with OltClient('host', 'username', 'password') as client:
    ...     cmd = client.execute('/services/showconfig')
    ...     for config_command in map(Command, cmd.output.splitlines()):
    ...         print(config_command.args['type'])
    ...
    mac bridge
    unicast
    multicast
    unicast
    multicast
    mac bridge



Installation
------------

:TODO: Upload to pypi :)

.. code-block:: bash

    $ pip install -r https://raw.githubusercontent.com/Vnet-as/cisco-olt-client/master/requirements.txt
    $ pip install -e git+https://github.com/Vnet-as/cisco-olt-client.git#egg=cisco_olt_client

Development
-----------

Create and activate `virtualenv <https://virtualenv.pypa.io/en/stable/>`_ then proceed with:

.. code-block:: bash

    $ pip install -r requirements.txt


For running tests you will need `tox <https://tox.readthedocs.io/en/latest/>`_ and everything in ``test-requirements.txt``:

.. code-block:: bash

    $ pip install tox
    $ pip install -r test-requirements.txt


Run tests:

.. code-block:: bash

    $ tox


Dependencies
============

- `paramiko (2.1.1) <http://www.paramiko.org/>`_


Compatibility
=============

Tests run against Python versions:

- 2.7
- 3.4
- 3.5
- 3.5-dev
- 3.6-dev


Licence
-------

MIT
