from ctypes.wintypes import BOOL
from xmlrpc.client import boolean
from keyboard import sender
from main import *


for event in bot.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        request = event.text.lower()
        user_id = str(event.user_id)
        msg = event.text.lower()
        sender(user_id, 'Выполняю','menu.json')
        if request == '🔍начать поиск':
            creating_database()
            bot.write_msg(user_id, f'Привет, {bot.name(user_id)}')
            if isinstance(bot.find_user(user_id),str):
                bot.find_persons(user_id, offset)
            sender(user_id, 'Жми на кнопку "Вперёд','menusearch.json')
        elif request == '🗺️вперёд':
            for i in line:
                offset += 1
                bot.find_persons(user_id, offset)
                sender(user_id, 'Жми на кнопку "Вперёд','menusearch.json')
                break
        elif request == '🔍новый поиск':
            if isinstance(bot.find_user(user_id),str):
                bot.write_msg(event.user_id, f'Нашёл для тебя пару, жми на кнопку "Вперёд"')
                bot.find_persons(user_id, offset)
            sender(user_id, 'Жми на кнопку "Вперёд','menusearch.json')
        elif request == '❤добавить в избранное':
            bot.find_favorites(user_id)
            sender(user_id, 'Добавил','menusearch.json')
        elif request == '📕назад':
            sender(user_id, 'Хорошо','menusearch.json')
        elif request == '❤️\u200d🔥посмотреть избранные' or request == 'далее':
            for i in line:                
                Error = bot.find_vievfavorites(user_id, offset)
                if Error:
                    sender(user_id, 'Список закончился','error.json')
                    break
                else:
                    offset += 1
                    sender(user_id, 'Жми на кнопку "Далее"','menufavorites.json')
                    break
           
        else:
            bot.write_msg(event.user_id, 'Твоё сообщение непонятно')