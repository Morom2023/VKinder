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

    def get_age(self, user_id, massege):
        """ПОЛУЧЕНИЕ ГРАНИЦЫ ДЛЯ ПОИСКА"""
        self.write_msg(user_id, massege)
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                age = event.text
                if age.isdigit() and int(age)>=16 and int(age)<=65:
                    return age
                else:
                    self.write_msg(user_id, 'Вы ввели не верный возраст!')


    def user(self, user_id):
        """ПОЛУЧЕНИЕ ИМЕНИ ПОЛЬЗОВАТЕЛЯ, КОТОРЫЙ НАПИСАЛ БОТУ"""
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'user_ids': user_id,
                  'fields': 'sex,city,bdate',
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_dict = response['response']
            return information_dict[0]
        except KeyError:
            self.write_msg(user_id, 'При выборе данных произошла ошибка.Наши специалисты уже работают над ней!!!')

    def get_sex(self, user_id, sex):
        """МЕНЯЕТ ПОЛ НА ПРОТИВОПОЛОЖНЫЙ"""
        if sex == 2:
            find_sex = 1
            return find_sex
        elif sex == 1:
            find_sex = 2
            return find_sex


    def get_high_search(self, user_ids,user_id):
            information_list = self.user(user_ids)
            date = information_list['bdate']
            city = information_list['city']['title']
            date_list = date.split('.')
            if len(date_list) == 3:
                year = int(date_list[2])
                year_now = int(datetime.date.today().year)
                yearlater = year_now - year
            else:
                yearlater = 0
            dataList = [yearlater,city]
            return dataList
    
    def find_user(self,user_id, currentUser):
        """ПОИСК ЧЕЛОВЕКА ПО ПОЛУЧЕННЫМ ДАННЫМ"""
        age_from = self.get_age(user_id,'Введите нижний порог возраста (min - 16): ')
        age_to = self.get_age(user_id, 'Введите верхний порог возраста (max - 65): ')
        searchList =[]
        if age_from <= age_to:
             url = f'https://api.vk.com/method/users.search'
             params = {'access_token': user_token,
                       'v': '5.131',
                       'sex': self.get_sex(user_id, currentUser["sex"]),
                       'age_from': age_from,
                       'age_to': age_to,
                       'city': currentUser["city"]["id"],
                       'fields': 'is_closed, id, first_name, last_name',
                       'status': '1' or '6',
                       'count': 1000}
             resp = requests.get(url, params=params)
             resp_json = resp.json()
             try:
                 dict_1 = resp_json['response']
             except KeyError:
                 self.write_msg(user_id, 'При выборе данных произошла ошибка.Наши специалисты уже работают над ней!!!')
                 return False
             seen_users = select()
             list_1 = dict_1['items']
             for person_dict in list_1:
                 if person_dict.get('is_closed') == False: 
                     if len(searchList) >= 20:
                         break
                     first_name = person_dict.get('first_name')
                     last_name = person_dict.get('last_name')
                     vk_id = str(person_dict.get('id'))
                     vk_link = 'vk.com/id' + str(person_dict.get('id'))
                     if vk_id not in seen_users:
                        foundUser = [first_name, last_name, vk_id, vk_link]
                        searchList.append(foundUser)
                     else:
                        continue
                 else:
                     continue
             return searchList

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
        except KeyError:
            self.write_msg(user_id, 'При выборе данных произошла ошибка.Наши специалисты уже работают над ней!!!')
            return False
        list_1 = dict_1['items']
        for i in list_1:
            photo_id = str(i.get('id'))
            i_likes = i.get('likes')
            if i_likes.get('count'):
                likes = i_likes.get('count')
                dict_photos[likes] = photo_id
        list_of_ids = sorted(dict_photos.items(), reverse=True)
        return list_of_ids
        

    def get_photo(self, user_id,nomber):
        """ПОЛУЧЕНИЕ ID ФОТОГРАФИИ"""
        list = self.get_photos_id(user_id)
        count = 0
        for i in list:
            count += 1
            if count == nomber:
                return i[1]

    def send_photo(self, user_id, message, offset,nomber,person_id):
        """ОТПРАВКА ФОТОГРАФИИ"""
        self.vk.method('messages.send', {'user_id': user_id,
                                         'access_token': user_token,
                                         'message': message,
                                         'attachment': f'photo{person_id}_{self.get_photo(person_id,nomber)}',
                                         'random_id': get_random_id()})

   
    def find_persons(self, user_id, offset, searchList):
        self.write_msg(user_id, self.found_person_info(offset, user_id, searchList))        
        insert_data_seen_users(searchList[offset][0], searchList[offset][1], searchList[offset][2], searchList[offset][3])
        number = 0
        while number < 3:
            number += 1
            if self.get_photo(searchList[offset][2],number) != None:
                self.send_photo(user_id, 'Фото номер ' + str(number), offset, number, searchList[offset][2])            
            else:
                self.write_msg(user_id, f'Больше фотографий нет')

    def found_person_info(self, offset,user_id, searchList):
        """ВЫВОД ИНФОРМАЦИИ О НАЙДЕННОМ ПОЛЬЗОВАТЕЛИ"""
        tuple_person = searchList[offset]
        dataList = self.get_high_search(tuple_person[2],user_id)
        return f'Нашел для тебя пару \n {tuple_person[0]} {tuple_person[1]}\n Возраст - {dataList[0]}\n Город - {dataList[1]}\n ссылка - {tuple_person[3]}'


    
    def find_favorites(self, vkId):
        insert_data_favorites(vkId) 
    
    def found_favorites_info(self, offset,user_id):
        """ВЫВОД ИНФОРМАЦИИ О ИЗБРАННЫХ ПОЛЬЗОВАТЕЛЯХ"""
        tuple_person = selectfavorites(offset)
        list_person = []
        try:
            for i in tuple_person:
                list_person.append(i)
            dataList = self.get_high_search(list_person[2],user_id)
            return f'{list_person[0]} {list_person[1]}\n Возраст - {dataList[0]}\n Город - {dataList[1]}\n ссылка - {tuple_person[3]}'
        except:
           return True

    
    def find_vievfavorites(self, user_id, offsetis):
        soob = self.found_favorites_info(offsetis,user_id)
        if isinstance(soob,str):
            self.write_msg(user_id, soob)
            number = 0
            while number < 3:
                number += 1
                person_id = selectfavorites(offsetis)[2]
                if self.get_photo(person_id,number) != None:
                    self.send_photo(user_id, 'Фото номер ' + str(number), offsetis,number, person_id)            
                else:
                    self.write_msg(user_id, f'Больше фотографий нет')  
        else:
            return soob


bot = VKBot()
               