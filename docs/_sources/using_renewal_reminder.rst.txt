######################
Using Renewal Reminder
######################
**renewal_reminder** can be used in many ways:

* invoked on the command-line
* invoked via Python
* invoked via Docker/docker-compose

.. note::
   This portion of the documentation does not cover installation.
   See the :ref:`Installation` section for how to install the project.

*********************
Environment Variables
*********************
Before you consider running the application, refer to the below table for required/optional environment variables used:

.. list-table:: Environment Variables
   :header-rows: 1

   * - Name
     - Description
     - Required?
     - Example
   * - APP_DAYS_NOTICE
     - Days notice before renewal is due.
     - Yes
     - 30
   * - APP_FILE_PATH
     - Csv file path containing members information.
     - Yes
     - /app/example.csv
   * - APP_LOG_LEVEL
     - App log level. Default INFO.
     - No
     - INFO
   * - TELEGRAM_BASE_URL
     - Telegram API base url. Default in example.
     - No
     - https://api.telegram.org/bot
   * - TELEGRAM_CHAT_ID
     - Telegram chat id.
     - Yes
     - 200200200:dsa8219knkncsa
   * - TELEGRAM_TOKEN_ID
     - Telegram bot token id.
     - Yes
     - 100100100

************
Using Poetry
************
After setting the :ref:`Environment Variables`, use

.. code-block:: bash

    # cd PROJECT_ROOT_DIR
    make install
    python renewal_reminder/app.py

************
Using Docker
************
After setting the :ref:`Environment Variables`, use

.. code-block:: bash

    docker run -v $(PWD)/example.csv:/app/file_name.csv wondercipher/renewal_reminder

.. note::
   The file path provided in environment variable APP_FILE_PATH, must be mounted in container.
   The mounted file and the environment variable filepath must match.