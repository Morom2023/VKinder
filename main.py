from cgitb import text
from config import user_token, comm_token, offset, line
import vk_api
import requests
import datetime
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
from database import *
from vk_api.utils import get_random_id


class VKBot:
    def __init__(self):
        print('Bot was created')
        self.vk = vk_api.VkApi(token=comm_token)  # АВТОРИЗАЦИЯ СООБЩЕСТВА
        self.longpoll = VkLongPoll(self.vk)  # РАБОТА С СООБЩЕНИЯМИ

    def write_msg(self, user_id, message):
        """МЕТОД ДЛЯ ОТПРАВКИ СООБЩЕНИЙ"""
        self.vk.method('messages.send', {'user_id': user_id,
                                         'message': message,
                                         'random_id': get_random_id()})

    def name(self, user_id):
        """ПОЛУЧЕНИЕ ИМЕНИ ПОЛЬЗОВАТЕЛЯ, КОТОРЫЙ НАПИСАЛ БОТУ"""
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'user_ids': user_id,
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_dict = response['response']
            for i in information_dict:
                for key, value in i.items():
                    first_name = i.get('first_name')
                    return first_name
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена, введите токен в переменную - user_token')

    def get_sex(self, user_id):
        """ПОЛУЧЕНИЕ ПОЛА ПОЛЬЗОВАТЕЛЯ, МЕНЯЕТ НА ПРОТИВОПОЛОЖНЫЙ"""
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'user_ids': user_id,
                  'fields': 'sex',
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_list = response['response']
            for i in information_list:
                if i.get('sex') == 2:
                    find_sex = 1
                    return find_sex
                elif i.get('sex') == 1:
                    find_sex = 2
                    return find_sex
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена, введите токен в переменную - user_token')

    def get_age_low(self, user_id):
        """ПОЛУЧЕНИЕ НИЖНЕЙ ГРАНИЦЫ ДЛЯ ПОИСКА"""
        self.write_msg(user_id, 'Введите нижний порог возраста (min - 16): ')
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                age = event.text
                if age.isdigit() and int(age)>=16:
                    return age
                else:
                    self.write_msg(user_id, 'Вы ввели не верный возраст!')



    def get_age_high(self, user_id):
        """ПОЛУЧЕНИЕ ВЕРХНЕЙ ГРАНИЦЫ ДЛЯ ПОИСКА"""
        self.write_msg(user_id, 'Введите верхний порог возраста (max - 65): ')
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                age = event.text  
                if age.isdigit() and int(age)<=65:
                    return age
                else:
                    self.write_msg(user_id, 'Вы ввели не верный возраст!')

    def get_age_high_search(self, user_ids,user_id):
        url = url = f'https://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'user_ids': user_ids,
                  'fields': 'bdate',
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_list = response['response']
            for i in information_list:
                date = i.get('bdate')
            date_list = date.split('.')
            if len(date_list) == 3:
                year = int(date_list[2])
                year_now = int(datetime.date.today().year)
                return year_now - year
        except KeyError:
             self.write_msg(user_id, 'Ошибка получения токена, введите токен в переменную - user_token')
          
               

    # @staticmethod
    def cities(self, user_id, city_name):
        """ПОЛУЧЕНИЕ ID ГОРОДА ПОЛЬЗОВАТЕЛЯ ПО НАЗВАНИЮ"""
        url = url = f'https://api.vk.com/method/database.getCities'
        params = {'access_token': user_token,
                  'country_id': 1,
                  'q': f'{city_name}',
                  'need_all': 0,
                  'count': 1000,
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_list = response['response']
            list_cities = information_list['items']
            for i in list_cities:
                found_city_name = i.get('title')
                if found_city_name == city_name:
                    found_city_id = i.get('id')
                    return int(found_city_id)
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена')

    def find_city(self, user_id):
        """ПОЛУЧЕНИЕ ИНФОРМАЦИИ О ГОРОДЕ ПОЛЬЗОВАТЕЛЯ"""
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'fields': 'city',
                  'user_ids': user_id,
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_dict = response['response']
            for i in information_dict:
                if 'city' in i:
                    city = i.get('city')
                    id = str(city.get('id'))
                    return id
                elif 'city' not in i:
                    self.write_msg(user_id, 'Введите название вашего города: ')
                    for event in self.longpoll.listen():
                        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                            city_name = event.text
                            id_city = self.cities(user_id, city_name)
                            if id_city != '' or id_city != None:
                                return str(id_city)
                            else:
                                break
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена')
    
    def find_city_name(self, user_id):
        """ПОЛУЧЕНИЕ ИНФОРМАЦИИ О ГОРОДЕ ПОЛЬЗОВАТЕЛЯ"""
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'fields': 'city',
                  'user_ids': user_id,
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_dict = response['response']
            for i in information_dict:
                if 'city' in i:
                    city = i.get('city')
                    id = str(city.get('id'))
                    return str(city.get('title'))                       
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена')
    def find_user(self, user_id):
        """ПОИСК ЧЕЛОВЕКА ПО ПОЛУЧЕННЫМ ДАННЫМ"""
        age_from = self.get_age_low(user_id)
        age_to = self.get_age_high(user_id)
        if age_from <= age_to:
             url = f'https://api.vk.com/method/users.search'
             params = {'access_token': user_token,
                       'v': '5.131',
                       'sex': self.get_sex(user_id),
                       'age_from': age_from,
                       'age_to': age_to,
                       'city': self.find_city(user_id),
                       'fields': 'is_closed, id, first_name, last_name',
                       'status': '1' or '6',
                       'count': 500}
             resp = requests.get(url, params=params)
             resp_json = resp.json()
             try:
                 dict_1 = resp_json['response']
                 list_1 = dict_1['items']
                 for person_dict in list_1:
                     if person_dict.get('is_closed') == False:
                         first_name = person_dict.get('first_name')
                         last_name = person_dict.get('last_name')
                         vk_id = str(person_dict.get('id'))
                         vk_link = 'vk.com/id' + str(person_dict.get('id'))
                         insert_data_users(first_name, last_name, vk_id, vk_link)
                     else:
                         continue
                 return f'Поиск завершён'
             except KeyError:
                 self.write_msg(user_id, 'Ошибка получения токена')
        else:
            self.write_msg(user_id, 'Не верно заданы критерия возроста. Конечный возрост не должен быть меньше начального')
            return False

    def get_photos_id(self, user_id):
        """ПОЛУЧЕНИЕ ID ФОТОГРАФИЙ С РАНЖИРОВАНИЕМ В ОБРАТНОМ ПОРЯДКЕ"""
        url = 'https://api.vk.com/method/photos.getAll'
        params = {'access_token': user_token,
                  'type': 'album',
                  'owner_id': user_id,
                  'extended': 1,
                  'count': 25,
                  'v': '5.131'}
        resp = requests.get(url, params=params)
        dict_photos = dict()
        resp_json = resp.json()
        try:
            dict_1 = resp_json['response']
            list_1 = dict_1['items']
            for i in list_1:
                photo_id = str(i.get('id'))
                i_likes = i.get('likes')
                if i_likes.get('count'):
                    likes = i_likes.get('count')
                    dict_photos[likes] = photo_id
            list_of_ids = sorted(dict_photos.items(), reverse=True)
            return list_of_ids
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена')

    def get_photo(self, user_id,nomber):
        """ПОЛУЧЕНИЕ ID ФОТОГРАФИИ"""
        list = self.get_photos_id(user_id)
        count = 0
        for i in list:
            count += 1
            if count == nomber:
                return i[1]

    def send_photo(self, user_id, message, offset,nomber):
        """ОТПРАВКА ФОТОГРАФИИ"""
        self.vk.method('messages.send', {'user_id': user_id,
                                         'access_token': user_token,
                                         'message': message,
                                         'attachment': f'photo{self.person_id(offset)}_{self.get_photo(self.person_id(offset),nomber)}',
                                         'random_id': get_random_id()})

   
    def find_persons(self, user_id, offset):
        self.write_msg(user_id, self.found_person_info(offset,user_id))
        insert_data_seen_users(self.person_id(offset), offset) #offset
        number = 0
        while number < 3:
            number += 1
            if self.get_photo(self.person_id(offset),number) != None:
                self.send_photo(user_id, 'Фото номер ' + str(number), offset,number)            
            else:
                self.write_msg(user_id, f'Больше фотографий нет')

    def found_person_info(self, offset,user_id):
        """ВЫВОД ИНФОРМАЦИИ О НАЙДЕННОМ ПОЛЬЗОВАТЕЛИ"""
        tuple_person = select(offset)
        list_person = []
        for i in tuple_person:
            list_person.append(i)
        return f'Нашел для тебя пару \n {list_person[0]} {list_person[1]}\n Возраст - {self.get_age_high_search(list_person[2],user_id)}\n Город - {self.find_city_name(list_person[2])}\n ссылка - {list_person[3]}'

    def person_id(self, offset):
        """ВЫВОД ID НАЙДЕННОГО ПОЛЬЗОВАТЕЛЯ"""
        tuple_person = select(offset)
        list_person = []
        for i in tuple_person:
            list_person.append(i)
        return str(list_person[2])

    def person_idusers(self, offset):
        """ВЫВОД ID НАЙДЕННОГО ПОЛЬЗОВАТЕЛЯ"""
        tuple_person = selectusers()
        list_person = []
        for i in tuple_person:
            list_person.append(i)
        return str(list_person[1])
    
    def find_favorites(self, offset):
        insert_data_favorites(self.person_idusers(offset)) 
    
    def found_favorites_info(self, offset,user_id):
        """ВЫВОД ИНФОРМАЦИИ О ИЗБРАННЫХ ПОЛЬЗОВАТЕЛЯХ"""
        tuple_person = selectfavorites(offset)
        list_person = []
        try:
            for i in tuple_person:
                list_person.append(i)
            return f'{list_person[0]} {list_person[1]}\n Возраст - {self.get_age_high_search(list_person[2],user_id)}\n Город - {self.find_city_name(list_person[2])}\n ссылка - {list_person[3]}'
        except:
           return True

    
    def find_vievfavorites(self, user_id, offset):
        soob = self.found_favorites_info(offset,user_id)
        if isinstance(soob,str):
            self.write_msg(user_id, soob)
            number = 0
            while number < 3:
                number += 1
                if self.get_photo(self.person_id(offset),number) != None:
                    self.send_photo(user_id, 'Фото номер ' + str(number), offset,number)            
                else:
                    self.write_msg(user_id, f'Больше фотографий нет')  
        else:
            return soob


bot = VKBot()
               