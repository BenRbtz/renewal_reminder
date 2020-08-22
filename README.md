# Renewal Reminder
Application sends a notification when a member is due for a licence renewal. Application is written using a
hexagonal architecture within the `renewal_reminder` directory.

## Run Application
`docker run --env-file=env-file -v $(PWD)/example.csv:/app/file_name.csv wondercipher/renewal_reminder`
### Environment Variables  
The below table is a list of environment variables that are used in the application:

| Name | Description | required | Example |
|:------:|:-----------:|:--------:|:-------:|
| APP_FILE_PATH   | File path to the csv containing the members information. MUST MATCH MOUNTED VOLUME FILE PATH | yes | /app/example.csv |
| APP_LOG_LEVEL   | The level of logging to record.                                                              | No | INFO |
| APP_TOKEN_ID    | The token id for the telegram bot                                                            | yes | 100100100 |
| APP_CHAT_ID     | The chat id for the telegram bot to send the notification to.                                | yes | 200200200:dsa8219knkncsa | 
| APP_NOTICE_DAYS | The number of days before a renewal is due to send a notification.                           | yes | 30 |
