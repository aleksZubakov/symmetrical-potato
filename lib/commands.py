import telegram
from telegram.ext import CommandHandler
import random

from globals import CURRENT_CHATS
from muzis_api_requests import get_track_url



# helpers
# deactivate chat
def deactivate_conv( chat_id ):
    if chat_id > 0:
        try:
            active = CURRENT_CHATS[chat_id]
            active['conv_active'] = False
            active['messages'] = []

        except (KeyError, IndexError):
            pass



def on_start_command(bot, update):
    user_name = update.message.from_user['first_name'] + ' ' + update.message.from_user['last_name']
    invitation = 'Hello ' + user_name + '!'
    main_text = ''' i'm Grandfather FreidBot and i'm going to help you :)
                '''

    chat_id = update.message.chat_id
    bot.sendMessage(chat_id=chat_id, text=invitation + main_text)


def on_init_command(bot, update, args):

    chat_id = update.message.chat_id

# POSSIBLE ERRORS HANDLERS
    # check if only one argument is passed
    if len(args) > 1:
        bot.sendMessage( chat_id=chat_id,
                         text="Sorry, to many arguments, pass only one number like 30")
        return

    # check if this argument is a number or if any numbers have been passe
    try:
        limit = int(args[0])
    except ValueError:
        bot.sendMessage( chat_id=chat_id,
                         text="Sorry, but argument must be a number" )
        return
    except IndexError:
        bot.sendMessage( chat_id=chat_id,
                         text="Sorry, but you didn't passed any arguments. Try '/init 15', it might work :)")
        return


    # initiating new chat in global variable
    chat_status = CURRENT_CHATS[ chat_id ] = {}
    chat_status['limit'] = limit
    chat_status['messages'] = list()

    # print(CURRENT_CHATS)





def on_get_command(bot, update):

    chat_id = update.message.chat_id

    deactivate_conv(chat_id)

    keyboard = [[
        "/random",
        "/init",
    ]]
    bot.sendMessage(chat_id=update.message.chat_id,
                     text="What's up?",
                     reply_markup=telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))


def on_help_command(bot, update):
    chat_id = update.message.chat_id

    deactivate_conv(chat_id)

    if (chat_id <= 0):
        message = """Hi there! This is Music FreidBot, and I'm here to help you with some music. I will give you music after some number of messages. Just call me with /init and a number of how many messages I should wait.
Enjoy some good music, provided by http://muzis.ru/"""
    else:
        message = """Hi there! This is Music FreidBot, and I'm here to help you with some music. Just call me with /hey command and tell me how you feel, and I will find something special for you :)
Enjoy some good music, provided by http://muzis.ru/"""

    bot.sendMessage( chat_id=chat_id,
                     text=message)


def get_random_soundtrack(bot, update):
    url = get_track_url()
    chat_id = update.message.chat_id

    deactivate_conv(chat_id)

    wait_text = "Please wait a few seconds, i'm sending you an audio :)"
    bot.sendMessage(chat_id=chat_id, text=wait_text)

    bot.sendAudio(chat_id=chat_id, audio=url)


def on_hey_command(bot, update):

    answers = [
        "How are you?",
        "How it's going?",
        "How was you day?",
        "How is everything going so far?",
        "What's up?",
        "What's new?"
    ]

    user_name = update.message.from_user['first_name'] + ' ' + update.message.from_user['last_name']
    invitation = 'Hello ' + user_name + '!'

    chat_id = update.message.chat_id

    if chat_id < 0:
        bot.sendMessage(chat_id=chat_id,
                        text="Sorry, but /hey only available in one-on-one talks with the great Doctor @MusicFreid_bot")
        return

    active = CURRENT_CHATS[ chat_id ] = {}
    active['conv_active'] = True
    active['messages'] = list()

    bot.sendMessage(chat_id=chat_id,
                    text=invitation + " " + random.choice(answers))

    print(CURRENT_CHATS)




# on_start_handler = CommandHandler( 'start', on_start_command )
# on_init_handler = CommandHandler('init', on_init_command, pass_args=True)
# on_get_handler = CommandHandler('get', on_get_command)
# on_help_handler = CommandHandler('help', on_help_command)
# get_audio_handler = CommandHandler('random', get_random_soundtrack)

COMMAND_EXPORT = [ CommandHandler('start', on_start_command),
                   CommandHandler('init', on_init_command, pass_args=True),
                   CommandHandler('get', on_get_command),
                   CommandHandler('help', on_help_command),
                   CommandHandler('random', get_random_soundtrack),
                   CommandHandler('hey', on_hey_command)
                   ]