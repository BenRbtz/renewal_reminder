# Renewal Reminder
Application sends a notification when a member is due for a licence renewal. Application is written using a
hexagonal architecture within the `renewal_reminder` directory.

## Requirements
Depending on how the application will be run, source or docker, the following dependencies are required:
* make
* python >= 3.8
* poetry >= 1.0.0

or

* make
* docker

## Usage
### Environment Variables  
Before you consider running the application, refer to the below table for required/optional environment variables used:

| Name | Description | required | Example |
|:------:|:-----------:|:--------:|:-------:|
| APP_DAYS_NOTICE   | Days notice before renewal is due.            | yes | 30 |
| APP_FILE_PATH     | Csv file path containing members information. | yes | /app/example.csv |
| APP_LOG_LEVEL     | App log level. Default INFO.                  | No  | INFO |
| TELEGRAM_BASE_URL | Telegram API base url. Default in example.    | No  | https://api.telegram.org/bot | 
| TELEGRAM_CHAT_ID  | Telegram chat id.                             | yes | 200200200:dsa8219knkncsa | 
| TELEGRAM_TOKEN_ID | Telegram bot token id.                        | yes | 100100100 |
 
### Run Application
After setting the [environment variables](#environment-variables), the app can be run with one of the following options:

#### Source
```bash
# cd PROJECT_ROOT_DIR
make install
python renewal_reminder/app.py
```
#### Docker
```bash
docker run -v $(PWD)/example.csv:/app/file_name.csv wondercipher/renewal_reminder
```
NOTE - the provided filepath provided in environment variable APP_FILE_PATH, must mount be mounted in container and matching

## Development

### Tests
The following sub-sections will detail how to set up and run different test levels from the CLI.
#### Unit
```bash
make run-unit-tests
```
#### Component
```bash
make dev-services-up # Start local docker services needed
make run-component-tests
make dev-services-down # Stop local docker services after finishing
```