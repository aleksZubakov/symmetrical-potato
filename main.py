from  __future__ import print_function
import logging
from telegram.ext import Updater, MessageHandler, Filters

import credentials
from lib.commands import COMMAND_EXPORT
from lib.messages import MESSAGES_EXPORT
from lib.callbacks import CALLBACK_EXPORT

#initialize


# setup updater, dispatcher, and logging
updater = Updater( token=credentials.token )
dispatcher = updater.dispatcher
logging.basicConfig( format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.WARNING )

# wrappers
def add_handlers( handlers ):
    for handler in handlers:
        dispatcher.add_handler( handler )



# unknown command handler
def on_unknown_command(bot, update):
    bot.sendMessage( chat_id=update.message.chat_id,
                     text="Sorry, but I don't know what {0} means".format(update.message.text))

on_unknown_handler = MessageHandler( [ Filters.command ], on_unknown_command )


# assign handlers
add_handlers( COMMAND_EXPORT + MESSAGES_EXPORT + CALLBACK_EXPORT + [ on_unknown_handler ] )



# start your engines
updater.start_polling()