import telegram
from telegram.ext import MessageHandler, Filters

from globals import CURRENT_CHATS
from muzis_api_requests import get_track_url


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

        if (len(active['messages']) >= active['limit']):

            active['messages'] = list()
            bot.sendMessage(chat_id=chat_id,
                            text='Preparing music')
            bot.sendAudio(chat_id=chat_id,
                          audio=get_track_url())
    except (KeyError, IndexError) :
        pass

    # print(CURRENT_CHATS)




MESSAGES_EXPORT = [
    MessageHandler([Filters.text], on_text_message)
]