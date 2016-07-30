import telegram
from telegram.ext import MessageHandler, Filters
import random

from globals import CURRENT_CHATS
from muzis_api_requests import get_track_url

# helpers TODO!!
# def sendMusic(  )


def on_text_message(bot, update):

    more_answers = [
        "Anything else?",
        "What's else on your mind?",
        "Got anything else?",
        "Something else?",
        "Got something else on you mind?"
    ]

    message_text = update.message.text
    chat_id = update.message.chat_id

    if chat_id < 0:
        try:
            active = CURRENT_CHATS[ chat_id ]
            active['messages'].append(message_text)

            if (len(active['messages']) >= active['limit']):

                active['messages'] = list()
                bot.sendMessage(chat_id=chat_id,
                                text='Music break!')
                bot.sendAudio(chat_id=chat_id,
                              audio=get_track_url())
        except (KeyError, IndexError) :
            pass
    else:
        try:
            active = CURRENT_CHATS[ chat_id ]
            if active['conv_active'] == False:

                active['conv_active'] = True
                active['messages'] = [] + message_text.split(" ")

                if ( len(active['messages']) > 10 ):
                    bot.sendMessage(chat_id=chat_id,
                                    text="Wait a sec for some music ;)")
                    bot.sendAudio(chat_id=chat_id,
                                  audio=get_track_url())
                    active['conv_active'] = False
                    active['messages'] = []
                    return

                bot.sendMessage(chat_id=chat_id,
                                text="Hey, how are you?")
            else:
                active['messages'] += message_text.split(" ")

                if (len(active['messages']) > 10):
                    bot.sendMessage(chat_id=chat_id,
                                    text="Wait a sec for some music ;)")
                    bot.sendAudio(chat_id=chat_id,
                                  audio=get_track_url())
                    active['conv_active'] = False
                    active['messages'] = []
                    return
                else:
                    bot.sendMessage(chat_id=chat_id,
                                    text=random.choice(more_answers))
        except (KeyError, IndexError):
            bot.sendMessage(chat_id=chat_id,
                            text="Hey, looks like we've never met! Just type /hey command to me and I will talk to you"
            )


    # print(CURRENT_CHATS)




MESSAGES_EXPORT = [
    MessageHandler([Filters.text], on_text_message)
]