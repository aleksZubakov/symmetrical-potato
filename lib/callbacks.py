from telegram.ext import CallbackQueryHandler

from globals import CURRENT_CHATS


def callback(bot, update):

    query = update.callback_query
    chat_id = query.message.chat.id

    try:
        active = CURRENT_CHATS[chat_id]
        active['fav_genre'] = query.data
    except (KeyError,IndexError):
        active = CURRENT_CHATS[ chat_id ] = {}
        active['conv_active'] = True
        active['messages'] = str()
        active['fav_genre'] = query.data

    genre = query.data.capitalize()
    if genre == 'ALL':
        message = "You will now get all music we have. To change genre in the future just use /genre command"
    else:
        message = "{0} saved as favourite genre. You can change it any time, just use /genre command".format(genre)

    bot.sendMessage(chat_id=chat_id, text=message)
    # print(query.data)
    # print(query.message.chat.id)

CALLBACK_EXPORT = [
    CallbackQueryHandler(callback)
]