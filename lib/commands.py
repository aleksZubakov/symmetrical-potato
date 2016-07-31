import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler
import random


from globals import CURRENT_CHATS
from muzis_api_requests import *



# helpers
# deactivate chat
def deactivate_conv( chat_id ):
    if chat_id > 0:
        try:
            active = CURRENT_CHATS[chat_id]
            active['conv_active'] = False
            active['messages'] = str()

        except (KeyError, IndexError):
            pass



def on_start_command(bot, update):

    chat_id = update.message.chat_id

    active = CURRENT_CHATS[chat_id] = dict()
    active['conv_active'] = True
    active['messages'] = str()
    active['fav_genre'] = 7

    if chat_id > 0:
        user_name = update.message.from_user['first_name'] + ' ' + update.message.from_user['last_name']
        invitation = 'Hey there, ' + user_name + '!'
        # main_text = 'i\'m Grandfather FreidBot and i\'m going to help you :)'
        main_text = 'I am Grandfather FreidBot, and I am going to help you\n' \
                    'Type /help if you want to learn more\n' \
                    'Type /random to get a random track\n' \
                    'Type /hey to start talking to me\n' \
                    'But first, choose your favourite genre if you want to ;)'

        inline_buttons = [[
            InlineKeyboardButton('rock', callback_data='0 rock'),
            InlineKeyboardButton('metal', callback_data='1 metal'),
            InlineKeyboardButton('r&b', callback_data='2 r&b')
        ],[
            InlineKeyboardButton('hip-hop', callback_data='3 hip-hop'),
            InlineKeyboardButton('soul', callback_data='4 soul'),
            InlineKeyboardButton('jazz', callback_data='5 jazz')
        ], [
            InlineKeyboardButton('pop', callback_data='6 pop'),
            InlineKeyboardButton('all', callback_data='7 all')
        ]
        ]

        reply_inline = InlineKeyboardMarkup(inline_buttons)

        bot.sendMessage(chat_id=chat_id,
                        text=invitation + main_text,
                        reply_markup=reply_inline)



    # bot.sendMessage(chat_id=chat_id, text=invitation + main_text)


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
    chat_status['msg_count'] = 0
    chat_status['limit'] = limit
    chat_status['messages'] = str()

    # print(CURRENT_CHATS)





def on_get_command(bot, update):

    chat_id = update.message.chat_id

    deactivate_conv(chat_id)

    # keyboard = [[
    #     "/random",
    #     "/init",
    # ]]
    bot.sendMessage(chat_id=update.message.chat_id,
                     text="What's up?"
                     # reply_markup=telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
                    )


def on_help_command(bot, update):
    chat_id = update.message.chat_id

    deactivate_conv(chat_id)

    if (chat_id <= 0):
        message = """Hi there! This is Music FreudBot, and I'm here to help you with some music. I will give you music after some number of messages. Just call me with /init and a number of how many messages I should wait.
Enjoy some good music, provided by http://muzis.ru/"""
    else:
        message = """Hi there! This is Music FreudBot, and I'm here to help you with some music. Just call me with /hey command and tell me how you feel, and I will find something special for you :)
Enjoy some good music, provided by http://muzis.ru/"""

    bot.sendMessage( chat_id=chat_id,
                     text=message)


def get_random_soundtrack(bot, update):
    chat_id = update.message.chat_id

    deactivate_conv(chat_id)


    bot.sendMessage(chat_id=chat_id,
                    text="Please wait a few seconds, i'm sending you an audio :)")

    url, performer, title = get_random(CURRENT_CHATS[chat_id]['fav_genre'])
    bot.sendAudio(chat_id=chat_id, audio=url, performer=performer, title=title)


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


    fav_genre = CURRENT_CHATS[chat_id]['fav_genre']

    active = CURRENT_CHATS[ chat_id ] = {}
    active['conv_active'] = True
    active['messages'] = str()
    active['fav_genre'] = fav_genre

    bot.sendMessage(chat_id=chat_id,
                    text=invitation + " " + random.choice(answers))

    print(CURRENT_CHATS)


def on_genre_command(bot, update):

    chat_id = update.message.chat_id

    inline_buttons = [[
        InlineKeyboardButton('rock', callback_data='rock'),
        InlineKeyboardButton('metal', callback_data='metal'),
        InlineKeyboardButton('r&b', callback_data='r&b')
    ],[
        InlineKeyboardButton('hip hop', callback_data='hip hop'),
        InlineKeyboardButton('soul', callback_data='soul'),
        InlineKeyboardButton('jazz', callback_data='jazz')
    ], [
        InlineKeyboardButton('pop', callback_data='pop'),
        InlineKeyboardButton('all', callback_data='all')
    ]
    ]

    reply_inline = InlineKeyboardMarkup(inline_buttons)

    bot.sendMessage(chat_id=chat_id,
                    text="Choose your favourite genre, or select all to get everything!!!",
                    reply_markup = reply_inline)



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
                   CommandHandler('hey', on_hey_command),
                   CommandHandler('genre', on_genre_command)
                   ]