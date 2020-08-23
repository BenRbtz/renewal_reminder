############
Installation
############

**********************
Installing with poetry
**********************


:Precondition: :ubuntu:`make` is installed
:Precondition: :ubuntu:`python3.8` (or newer) is installed
:Precondition: :ubuntu:`python3-venv` is installed
:Precondition: :pypi:`poetry` is installed

Execute the following command to install the project

.. code-block:: bash

    make install

To update packages for the project, use

.. code-block:: bash

    make update

To install the developer packages with the project, use

.. code-block:: bash

    make install-dev

**********************
Installing with docker
**********************

:Precondition: :ubuntu:`docker` is installed

Execute the following command to pull the image for the project

.. code-block:: bash

    docker image pull wondercipher/renewal_reminder
