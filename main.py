from  __future__ import print_function


from telegram.ext import Updater, MessageHandler, Filters


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


freid_handler = MessageHandler([Filters.text], grandfather_freid)
