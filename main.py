from  __future__ import print_function
import logging
import credentials
from muzis_api_requests import get_track_url
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

# setup updater, dispatcher, and logging
updater = Updater( token=credentials.token )
dispatcher = updater.dispatcher
logging.basicConfig( format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.WARNING )

# global variables
CURRENT_CHATS = dict()


# wrappers
def add_handlers( handlers ):
    for handler in handlers:
        dispatcher.add_handler( handler )


# def produceHandlers(  ):
#     pass


# handler's functions
def on_start_command(bot, update):
    user_name = update.message.from_user['first_name'] + ' ' + update.message.from_user['last_name']
    invitation = 'Hello ' + user_name + '!'
    main_text = ''' i'm Grandfather FreidBot and i'm going to help you :)
                '''

    chat_id = update.message.chat_id
    bot.sendMessage(chat_id=chat_id, text=invitation + main_text)


def on_init_command(bot, update, args):

    chat_id = update.message.chat_id

    # check if only one argument is passed
    if len(args) > 1:
        bot.sendMessage( chat_id=chat_id,
                         text="Sorry, to many arguments, pass only one number like 30")
        return


    # check if this argument is a number
    try:
        limit = int(args[0])
    except ValueError:
        bot.sendMessage( chat_id=chat_id,
                         text="Sorry, but argument must be a number" )
        return

    # creating new var in global vault
    chat_status = CURRENT_CHATS[ chat_id ] = {}
    chat_status['limit'] = limit
    chat_status['messages'] = list()

    # print(CURRENT_CHATS)


def on_unknown_command(bot, update):
    bot.sendMessage( chat_id=update.message.chat_id,
                     text="Sorry, but I don't know what {0} means".format(update.message.text))


def on_text_message(bot, update):
    message_text = update.message.text

    """
    here will be ibm module
    """
    music_result = 'bla_bla'

    chat_id = update.message.chat_id

    try:
        active = CURRENT_CHATS[ chat_id ]
        active['messages'].append(message_text)
        if ( len(active['messages']) >= 30 ):
            pass
    except IndexError:
        pass

    # print(CURRENT_CHATS)
    # # bot.sendMessage(chat_id=chat_id, text=message_text)

def get_random_soundtrack(bot, update):
    url = get_track_url()
    chat_id = update.message.chat_id

    wait_text = "Please wait a few seconds, i'm sending you an audio :)"
    bot.sendMessage(chat_id=chat_id, text=wait_text)

    bot.sendAudio(chat_id=chat_id, audio=url)

# handlers
on_start_handler = CommandHandler( 'start', on_start_command )
on_init_hanlder = CommandHandler('init', on_init_command, pass_args=True)
on_unknown_handler = MessageHandler( [ Filters.command ], on_unknown_command )
text_message_handler = MessageHandler([Filters.text], on_text_message)
get_audio_handler = CommandHandler('random', get_random_soundtrack)


# assign handlers
add_handlers([text_message_handler, on_start_handler, get_audio_handler, on_init_hanlder, on_unknown_handler])


# start your engines
updater.start_polling()


