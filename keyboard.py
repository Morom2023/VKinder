from main import bot
from vk_api.utils import get_random_id
import json

def sender(user_id,text,id_keyboard):
    bot.vk.method('messages.send', {'user_id': user_id,
                                    'message': text,
                                    'random_id': get_random_id(),
                                    'keyboard': open(id_keyboard, 'r', encoding='UTF-8').read()})

