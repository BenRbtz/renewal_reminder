# Renewal Reminder
Application sends a notification when a member is due for a licence renewal. Application is written using a
hexagonal architecture within the `renewal_reminder` directory.

## Requirements
Depending on how the application will be run, source or docker, the following dependencies are required:
* python >= 3.8
* poetry >= 1.0.0

or

* docker

## Usage
### Environment Variables  
Before you consider running the application, refer to the below table for required/optional environment variables used:

| Name | Description | required | Example |
|:------:|:-----------:|:--------:|:-------:|
| APP_FILE_PATH   | Csv file path containing members information. | yes | /app/example.csv |
| APP_TOKEN_ID    | Telegram bot token id.                        | yes | 100100100 |
| APP_CHAT_ID     | Telegram chat id.                             | yes | 200200200:dsa8219knkncsa | 
| APP_DAYS_NOTICE | Days notice before renewal is due.            | yes | 30 |
| APP_LOG_LEVEL   | App log level. Default INFO.                  | No  | INFO |

 
### Run Application
After setting the [environment variables](#environment-variables), the app can be run with one of the following options:

#### Source
```bash
# cd PROJECT_ROOT_DIR
poetry install
python renewal_reminder/app.py
```
#### Docker
```bash
docker run -v $(PWD)/example.csv:/app/file_name.csv wondercipher/renewal_reminder
```
NOTE - the provided filepath provided in environment variable APP_FILE_PATH, must mount be mounted in container and matching
