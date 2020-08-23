###########################
Developing Renewal Reminder
###########################

.. note::
   This portion of the documentation does not cover installation.
   See the :ref:`Installation` section for how to install the project.

*****
Tests
*****
The following sub-sections will detail how to set up and run different test levels from the CLI.

Unit
=====
To execute the tests, use

.. code-block:: bash

  make run-unit-tests

Component
=========

:Precondition: :ubuntu:`docker-compose` is installed

To start the required local docker services needed, use

.. code-block:: bash

  make dev-services-up

To execute the tests, use

.. code-block:: bash

  make run-component-tests

To stop the required local docker services after finis, use

.. code-block:: bash

  make dev-services-down
