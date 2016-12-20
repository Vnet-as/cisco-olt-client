cisco_olt_client
================

.. image:: https://travis-ci.org/Vnet-as/cisco-olt-client.png
   :target: https://travis-ci.org/Vnet-as/cisco-olt-client
   :alt: Latest Travis CI build status

Python wrapper for cisco's olt boxes commands executed via ssh


Usage
-----

Get raw output from command as during interactive session. Example usage in
python3 and since output is in bytes it needs to be decoded to utf-8.

.. code-block:: python

    Python 3.5.2 (default, Aug 20 2016, 15:02:10)
    [GCC 4.9.2] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from cisco_olt_client.client import OltClient
    >>>
    >>> with OltClient('192.168.35.50', 'admin', 'LedaMetis2012') as client:
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

Requirements
^^^^^^^^^^^^

Compatibility
-------------

Licence
-------

MIT
