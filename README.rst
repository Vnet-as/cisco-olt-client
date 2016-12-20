cisco_olt_client
================

.. image:: https://travis-ci.org/Vnet-as/cisco-olt-client.png
   :target: https://travis-ci.org/Vnet-as/cisco-olt-client
   :alt: Latest Travis CI build status


.. image:: https://codecov.io/gh/Vnet-as/cisco-olt-client/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/Vnet-as/cisco-olt-client
   :alt: Test coverage status from latest build

Python wrapper for cisco's olt boxes commands executed via ssh


Usage
-----

Get raw output from command as during interactive session. Example usage in
python3 and since output is in bytes it needs to be decoded to utf-8.

.. code-block:: python

    >>> from cisco_olt_client.client import OltClient
    >>>
    >>> with OltClient('host', 'user', 'password') as client:
    ...     command_output = client.raw_exec_command('/dhcp/global/show')
    ...     for line in command_output.splitlines():
    ...         print(line.decode('utf-8'))
    ...
    /dhcp/global/show
    Global DHCP circuit ID Template String:
    "$accessnodeid PON $rack/$subrack/$slot/$port:$onuid.$svid"
    /cli>
    >>>



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


Licence
-------

MIT
