# -*- coding: utf-8 -*-
import logging
import telegram
import ast
import list_emoji
# firebase_cred is file contains config for firebase
import firebase_cred
from telegram.ext import (Updater, CommandHandler)
from time import sleep

# Firebase
collection = firebase_cred.smart_lock_col

servo = None
infrared = None
confirm = None
user_ref = None
log_dict = None
sensor_ref = None
log_ref = None
user_id = None
wave = None
pin = None
people = None
lock = None
unlocked = None
no_entry_sign = None
warning = None
mag = None
check = None
x = None
id_emoji = None
date_emoji = None


def get_data():
    # Sensor
    sensor_ref = collection.document(u'sensor')
    sensors = sensor_ref.get()
    sensors_string_dict = '{}'.format(sensors.to_dict())
    sensors_dict = ast.literal_eval(sensors_string_dict)
    confirm = sensors_dict['confirm']
    infrared = sensors_dict['infrared']
    servo = sensors_dict['servo']

    # Log
    log_ref = collection.document(u'log')
    logs = log_ref.get()
    log_string_dict = '{}'.format(logs.to_dict())
    log_dict = ast.literal_eval(log_string_dict)

    # User
    user_ref = log_ref.collection(u'user')
    users = user_ref.stream()
    user_id = {None}
    for doc in users:
        user_id.add(str(doc.id))
    user_id.remove(None)


def get_url():
    url = 'YOUR_PHOTO_URL'
    return url


# Log
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def log_info(name, chat_id, username, text):
    name = name
    chat_id = chat_id
    username = username
    text = text
    logging.info('%s hit by: %s - full name: %s - username: %s',
                 text, chat_id, name, username)


# Emoji
def get_emoji():
    wave = list_emoji.wave
    pin = list_emoji.pin
    people = list_emoji.people
    lock = list_emoji.lock
    unlocked = list_emoji.unlock
    no_entry_sign = list_emoji.no_entry_sign
    warning = list_emoji.warning
    mag = list_emoji.mag
    check = list_emoji.check
    x = list_emoji.x
    id_emoji = list_emoji.id_emoji
    date_emoji = list_emoji.date_emoji


# BotCommand
parse_md = telegram.ParseMode.MARKDOWN


def status(bot, update):
    get_data()
    name = update.message.from_user.full_name
    chat_id = update.message.chat_id
    username = update.message.from_user.username
    text = update.message.text
    if str(chat_id) not in user_id:
        update.message.reply_text(
            no_entry_sign + ' *Only allowed user can use this features*', parse_mode=parse_md)
    else:
        if infrared == 0:
            status1 = lock + ' Locked'
        else:
            status1 = unlocked + ' Unlocked'
        update.message.reply_text(
            '*Locker status*: ' + status1, parse_mode=parse_md)
    log_info(name, chat_id, username, text)


def unlock(bot, update):
    get_data()
    name = update.message.from_user.full_name
    chat_id = update.message.chat_id
    username = update.message.from_user.username
    text = update.message.text
    if str(chat_id) not in user_id:
        update.message.reply_text(
            no_entry_sign + ' *Only allowed user can use this features*', parse_mode=parse_md)
    else:
        if infrared == 0:
            sensor_ref.update({'infrared': 1})
            url = get_url()
            bot.send_photo(chat_id=chat_id, photo=url,
                           caption='*Place your finger at red circle*', parse_mode=parse_md)
            retry = 1
            while retry < 6:
                sleep(2)
                get_data()
                if confirm == 1:
                    update.message.reply_text(
                        check + ' *Confirmed*\nUnlocking...', parse_mode=parse_md)
                    sensor_ref.update({'servo': 1})
                    sleep(2)
                    break
                else:
                    if retry == 1:
                        update.message.reply_text(warning + ' *Sorry i can\'t confirm*\n' + mag + ' Retrying...',
                                                  parse_mode=parse_md)
                    else:
                        update.message.reply_text(mag + ' Retrying...')
                retry += 1
                sleep(3)
            if retry >= 6 and confirm == 0:
                update.message.reply_text(
                    x + ' *Confirmation Failed*\nPlease try again', parse_mode=parse_md)
                sensor_ref.update({'infrared': 0})
            else:
                update.message.reply_text(unlocked + ' *Locker Unlocked*\n' + warning +
                                          ' The lock will automatically locked approximately in *10 Seconds*', parse_mode=parse_md)
                log_ref.set({
                    'name': name,
                    'date': '{}'.format(update.message.date),
                    'chat_id': chat_id,
                    'username': username
                })
        else:
            update.message.reply_text(
                check + ' Already unlocked', parse_mode=parse_md)
    log_info(name, chat_id, username, text)


def log(bot, update):
    get_data()
    name = update.message.from_user.full_name
    chat_id = update.message.chat_id
    username = update.message.from_user.username
    text = update.message.text
    if str(chat_id) not in user_id:
        update.message.reply_text(
            no_entry_sign + ' *Only allowed user can use this features*', parse_mode=parse_md)
    else:
        get_data()
        log_id = log_dict['chat_id']
        log_date = log_dict['date']
        log_name = log_dict['name']
        log_username = log_dict['username']
        update.message.reply_text('*Log Locker*\nUser who last unlock locker is:\n\n' + id_emoji + ' *User ID*: ' +
                                  str(log_id) + '\n' + people + ' *Name*: ' +
                                  log_name + '\n' + people + ' *Username*: '
                                  + log_username + '\n' + date_emoji + ' *Date Unlock*: ' + log_date,
                                  parse_mode=parse_md)
    log_info(name, chat_id, username, text)


def tambahgan(bot, update):
    get_data()
    name = update.message.from_user.full_name
    chat_id = update.message.chat_id
    username = update.message.from_user.username
    text = update.message.text
    if str(chat_id) in user_id:
        update.message.reply_text(x + 'User already in our database')
    else:
        user_ref.document(str(chat_id)).set({
            u'chat_id': chat_id,
            u'full name': name,
            u'is bot': update.message.from_user.is_bot,
            u'username': username
        })
        update.message.reply_text(check + 'User has been added to database')
    log_info(name, chat_id, username, text)


def start(bot, update):
    name = update.message.from_user.full_name
    chat_id = update.message.chat_id
    username = update.message.from_user.username
    text = update.message.text
    update.message.reply_text('Hello {} '.format(update.message.from_user.full_name) + wave +
                              '\nI can help you manage locker, but this bot only accept command from user that '
                              'already registered, if you know my creator in real life please contact him/her '
                              'for register.\n\nYou can control me by using these command:\n\n'
                              + pin + ' /info - info about team who created me & how i created\n\n'
                              '*Manage Locker (registered user only)*\n' + pin +
                              ' /status - show current status of locker\n' + pin +
                              ' /unlock - unlock locker if the locker is locked\n' + pin +
                              ' /log - show who last unlock the locker', parse_mode=parse_md)
    log_info(name, chat_id, username, text)


def info(bot, update):
    name = update.message.from_user.full_name
    chat_id = update.message.chat_id
    username = update.message.from_user.username
    text = update.message.text
    header_text = 'This bot created by `Internet of Things Division of Workshop Riset Informatika ' \
                  'Politeknik Negeri Malang` for Program *Open Project Workshop Riset Informatika 2019*\n\n'
    member = '*Member of this Project*:\n' + people + ' Ardan Anjung Kusuma - @ardanak\n' + people + \
             ' Hafid Sajid - @hafidhsajid\n' + people + ' Nurmayanti Ratna Mustika - \n' + people + \
             ' Sultan Achmad Qum Masykuro NS - @SultanKs4\n\n'
    about_me = '*Info about me:*\n' + pin + ' Based on Python programming language\n' + pin + \
               ' Only for educational purpose only\n' + pin + ' Source code available on ' \
               '[github](https://github.com/SultanKs4/SmartLockCB)'
    update.message.reply_text(header_text + member + about_me,
                              parse_mode=parse_md, disable_web_page_preview=True)
    log_info(name, chat_id, username, text)


def main():
    updater = Updater('YOUR_TOKEN')
    dp = updater.dispatcher
    get_emoji()
    dp.add_handler(CommandHandler('unlock', unlock))
    dp.add_handler(CommandHandler('status', status))
    dp.add_handler(CommandHandler('log', log))
    dp.add_handler(CommandHandler('tambahgan', tambahgan))
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('info', info))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
