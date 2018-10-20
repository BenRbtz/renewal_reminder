import configparser
import logging

from telegram import Bot

from renewals.checker import Checker

config = configparser.ConfigParser()
config.read('config.example.ini')

token_id = config['bot']['token_id']
chat_id = config['bot']['chat_id']
file_path = config['general']['file_path']
log_path = config['general']['log_path']

logging.basicConfig(level=logging.DEBUG,
                    filename=log_path,
                    filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

bot = Bot(token=token_id)
checker = Checker(bot, logging)

checker.run(chat_id=chat_id, file_path=file_path)
