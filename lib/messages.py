import telegram
from telegram.ext import MessageHandler, Filters
import random

from globals import CURRENT_CHATS
from muzis_api_requests import *

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
            active['messages'] += ' ' + message_text
            active['msg_count'] += 1

            if (active['msg_count'] >= active['limit']):


                bot.sendMessage(chat_id=chat_id,
                                text='Music break!')

                url = get_match(active['messages'])
                bot.sendAudio(chat_id=chat_id,
                                      audio=url)

                active['messages'] = str()
                active['msg_count'] = 0
        except (KeyError, IndexError) :
            pass
    else:
        try:
            active = CURRENT_CHATS[ chat_id ]
            if active['conv_active'] == False:

                active['conv_active'] = True
                active['messages'] += ' ' + message_text

                if (len(active['messages'].split(' ')) > 10 ):
                    bot.sendMessage(chat_id=chat_id,
                                    text="Wait a sec for some music ;)")
                    url = get_match(active['messages'])
                    bot.sendAudio(chat_id=chat_id,
                                  audio=url)
                    active['conv_active'] = False
                    active['messages'] = str()
                    return

                bot.sendMessage(chat_id=chat_id,
                                text="Hey, how are you?")
            else:
                active['messages'] += ' ' + message_text

                if (len(active['messages'].split(' ')) > 10 ):
                    bot.sendMessage(chat_id=chat_id,
                                    text="Wait a sec for some music ;)")

                    url = get_match(active['messages'])
                    bot.sendAudio(chat_id=chat_id,
                                  audio=url)
                    active['conv_active'] = False
                    active['messages'] = str()
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