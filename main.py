from  __future__ import print_function
import logging
import credentials
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler


# setup updater, dispatcher, and logging
updater = Updater( token=credentials.token )
dispatcher = updater.dispatcher
logging.basicConfig( format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.WARNING )

# wrappers
def addHandlers( handlers ):
    for handler in handlers:
        dispatcher.add_handler( handler )


# def produceHandlers(  )



def start(bot, update):
    user_name = update.message.from_user['first_name'] + ' ' + update.message.from_user['last_name']
    invitation = 'Hello ' + user_name + '!'
    main_text = ''' i'm Grandfather FreidBot and i'm going to help you :)
                '''

    chat_id = update.message.chat_id
    bot.sendMessage(chat_id=chat_id, text=invitation + main_text)




def grandfather_freid(bot, update):
    message_text = update.messsage.text

    """
    here will be ibm module
    """
    music_result = 'bla_bla'

    chat_id = update.messsage.chat_id
    bot.sendMessage(chat_id=chat_id, text=message_text)

# handlers
onStartCommand = CommandHandler( 'start', start )
freid_handler = MessageHandler([Filters.text], grandfather_freid)

# assign handlers
addHandlers( [ freid_handler, onStartCommand ] )


# start your engines
updater.start_polling()


