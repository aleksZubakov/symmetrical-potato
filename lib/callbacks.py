from telegram.ext import CallbackQueryHandler

from globals import CURRENT_CHATS


def callback(bot, update):

    query = update.callback_query
    chat_id = query.message.chat.id


    splitted = query.data.split()
    print(splitted)
    code = int(splitted[0])
    genre = splitted[1]

    try:
        active = CURRENT_CHATS[chat_id]
        active['fav_genre'] = code
    except (KeyError,IndexError):
        active = CURRENT_CHATS[ chat_id ] = {}
        active['conv_active'] = True
        active['messages'] = str()
        active['fav_genre'] = code

    genre = genre.capitalize()
    print('>>',genre)
    if genre == 'All':
        message = "You will now get TOP 500 music we have. To choose genre in the future just use /genre command"
    else:
        message = "{0} saved as favourite genre. You can change it any time, just use /genre command".format(genre)

    bot.sendMessage(chat_id=chat_id, text=message)
    # print(query.data)
    # print(query.message.chat.id)

CALLBACK_EXPORT = [
    CallbackQueryHandler(callback)
]