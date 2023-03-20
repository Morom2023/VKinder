from ctypes.wintypes import BOOL
from xmlrpc.client import boolean
from keyboard import sender
from main import *

global users,searchList
creating_database()
offsetis = 0
for event in bot.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        request = event.text.lower()
        user_id = str(event.user_id)
        currentUser = bot.user(user_id)
        msg = event.text.lower()
        sender(user_id, 'Выполняю','menu.json')
        if (request == '🔍начать поиск') or (request == '🔍новый поиск'):  
            bot.write_msg(user_id, f'Привет, {currentUser["first_name"]}')
            searchList = bot.find_user(user_id,currentUser)
            if isinstance(searchList,list):
                bot.find_persons(user_id, offset, searchList)
            sender(user_id, 'Жми на кнопку "Вперёд','menusearch.json')
        elif request == '🗺️вперёд':
            for i in line:
                if len(searchList) < offset:
                     sender(user_id, 'Поиск завершон. Необходимо начать новый!','menusearch.json')
                else:
                    offset += 1
                    bot.find_persons(user_id, offset, searchList)                 
                    sender(user_id, 'Жми на кнопку "Вперёд','menusearch.json')
                    break
        elif request == '❤добавить в избранное':
            bot.find_favorites(searchList[offset][2])
            sender(user_id, 'Добавил','menusearch.json')
        elif request == '📕назад':
            sender(user_id, 'Хорошо','menusearch.json')
        elif request == '❤️\u200d🔥посмотреть избранные' or request == 'далее':
            for i in line:                
                Error = bot.find_vievfavorites(user_id, offsetis)
                if Error:
                    sender(user_id, 'Список закончился','error.json')
                    offsetis = 0
                    break
                else:
                    offsetis += 1
                    sender(user_id, 'Жми на кнопку "Далее"','menufavorites.json')
                    break
           
        else:
            bot.write_msg(event.user_id, 'Твоё сообщение непонятно')