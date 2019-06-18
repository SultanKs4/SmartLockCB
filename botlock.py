import logging
import telegram
# firebase_cred is file contains config for firebasegit
import firebase_cred
from telegram.ext import (Updater, CommandHandler)
from time import sleep

# Firebase
ref = firebase_cred.ref


def get_data():
    global servo, infrared, confirm
    root_sensor = ref.child('sensors')
    servo = root_sensor.child('servo').get()
    infrared = root_sensor.child('infrared').get()
    confirm = root_sensor.child('confirm').get()


def get_url():
    url = 'YOUR_PHOTO_URL'
    return url


# AllowedUser
user = {usr1, usr2, etc}

# Log
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


# BotCommand
parse_md = telegram.ParseMode.MARKDOWN


def status(bot, update):
    if update.message.chat_id not in user:
        update.message.reply_text('*Sorry*\nOnly allowed user can use this features', parse_mode=parse_md)
    else:
        get_data()
        if infrared == 0:
            status1 = 'Locked'
        else:
            status1 = 'Unlocked'
        update.message.reply_text('*Locker status*: ' + status1, parse_mode=parse_md)


def unlock(bot, update):
    if update.message.chat_id not in user:
        update.message.reply_text('*Sorry*\nOnly allowed user can use this features', parse_mode=parse_md)
    else:
        get_data()
        sensor_ref = ref.child('sensors')
        if infrared == 0:
            sensor_ref.update({
                'infrared': 1
            })
            url = get_url()
            chat_id = update.message.chat_id
            bot.send_photo(chat_id=chat_id, photo=url)
            update.message.reply_text('*Place your finger at place*', parse_mode=parse_md)
            retry = 1
            while retry < 6:
                sleep(2)
                get_data()
                if confirm == 1:
                    update.message.reply_text('*Confirmed*\nUnlocking...', parse_mode=parse_md)
                    sensor_ref.update({
                        'servo': 1
                    })
                    sleep(2)
                    break
                else:
                    if retry == 1:
                        update.message.reply_text('*Sorry i can\'t confirm*\nRetrying...', parse_mode=parse_md)
                    else:
                        update.message.reply_text('Retrying...')
                retry += 1
                sleep(3)
            if retry >= 6 and confirm == 0:
                update.message.reply_text('*Confirmation Failed*\nPlease try again', parse_mode=parse_md)
            else:
                update.message.reply_text('*Locker Unlocked*', parse_mode=parse_md)
                log_ref = ref.child('log')
                log_ref.set({
                    'name': update.message.from_user.full_name,
                    'date': '{}'.format(update.message.date),
                    'chat_id': chat_id
                })
        else:
            update.message.reply_text('Already unlocked', parse_mode=parse_md)


def log(bot, update):
    if update.message.chat_id not in user:
        update.message.reply_text('*Sorry*\nOnly allowed user can use this features', parse_mode=parse_md)
    else:
        log_ref = ref.child('log')
        log_id = log_ref.child('chat_id').get()
        log_date = log_ref.child('date').get()
        log_name = log_ref.child('name').get()
        update.message.reply_text('*Log Locker*\nUser who last unlock locker is:\n\n*User ID*: ' + str(log_id) +
                                  '\n*Name*: ' + log_name + '\n*Date Unlock*: ' + log_date, parse_mode=parse_md)


def main():
    updater = Updater('YOUR_TOKEN')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('unlock', unlock))
    dp.add_handler(CommandHandler('status', status))
    dp.add_handler(CommandHandler('log', log))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
