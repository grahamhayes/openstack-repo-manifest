OpenStack Repo Manifest
=======================

This repo contains a ``default.xml`` for all project hosted on the OpenStack
CI Infrastructure.

This allows users to use the `repo`_ tools to clone and interact with the
projects.

There are also groups assigned to each repository (as noone really needs
to clone **all** of the repos on https://git.openstack.org :) )

The groups are:

* Project name (aka ``designate``)
* Service Type (derived from `os-service-types`_, aka ``dns``)
* Governance Tags (aka ``stable:follows-policy``)
* ``offical`` if the repository is in ``projects.yaml``

A full list of groups is `here`_

Usage
-----

* Install ``repo`` (``apt-get install repo`` on Ubuntu)
* ``repo init -u https://github.com/grahamhayes/openstack-repo-manifest``
* ``repo sync``

To only clone a set of repos add ``-g <group name>``
or``-g <group1 name>,<group2 name>`` to the ``init`` command.

.. _repo: https://source.android.com/setup/using-repo
.. _os-service-types: https://docs.openstack.org/os-service-types/latest/
.. _here: groups.rst