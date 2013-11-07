sshh - multi-host shell helper
==============================

Manage large number of hosts by placing them and their addresses to text or
JSON files. ``sshh`` is a command-line utility that allows finding the right
hosts and opens an SSH connectio to them.

Features:

* Automatically detects if running under ``screen`` and opens multiple SSH
  connections in separate named windows, requires use of the ``-a`` switch.
* Uses the hostname (or FQDN) to connect if it resolves to the same IP address
  as specified in a host configuration file. If the address resolves
  differently, the IP specified in the configuration file is used.
* URLs are opened into the browser.

Example Configuration
---------------------
``$HOME/.sshh/config.json``::

    {
        "files": [
            { "path": "{HOME}/git/some-hosting-env/nodes.json",
              "type": "json", "domain": "my.domain.com" },
            { "path": "hosting.txt" }
        ]
    }

``$HOME/.sshh/hosting.txt``::

    load-balancer xyz webui https://10.0.0.10
    dc01 http proxy 10.2.0.1

``$HOME/git/some-hosting-env/nodes.json``::

    {
      "nodes": [
        {"name": "http-server-a01", "ipv4": "10.0.1.1"},
        {"name": "http-server-b01", "ipv4": "10.0.1.1"},
        {"name": "db-server-a01", "ipv4": "10.0.2.1"}
        ]
    }

Usage Examples
--------------
* Show all hosts: ``sshh`` or ``sshh -q``
* Open SSH connection to the DB server: ``sshh db-server``
* Open SSH connections to all http servers: ``sshh -a http``
* Open the load-balancer webui in browser: ``sshh load web`` (multiple match
  patterns)
* Just query, don't open any connections: ``sshh -q db``

Open-Source License
-------------------
MIT, see ``LICENSE``
