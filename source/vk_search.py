import requests
import configparser
from pprint import pprint
import random
import time

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("settings.ini")  # читаем конфиг

TOKEN = config['DEFAULT']['vk_app_token']


class VkbackUp():
    def __init__(self, token: str):
        self.token = token

    def get_list_photo(self, id_album: str, id_user: str):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': id_user,
                  'album_id': id_album,
                  'access_token': self.token,
                  'extended': "1",
                  'count': '10',
                  'v': '5.131'}

        response = requests.get(url, params=params)
        return response.json()

    def get_unpack_photo(self, vk_json):
        """принимает 1 аргумент, json файл от метода photo.get vk
        возвращает список альбомов"""

        album = vk_json['response']['items']

        return album

    def get_list(self, album):
        """принимает 1 аргумет, список альбомов из get_unpack_photo,
        возвращает список словарей с названиями фото по лайкам"""
        vk_sizes = {'s': 1, 'm': 2, 'o': 3, 'p': 4, 'q': 5, 'r': 6, 'x': 7, 'y': 8, 'z': 9, 'w': 10}
        pack = []
        for photo in album:
            name = {}
            name['like'] = photo['likes']['count']
            sizes = max(photo['sizes'], key=lambda x: vk_sizes[x["type"]])
            name['type'] = sizes['type']
            name['url'] = sizes['url']
            pack.append(name)

        return pack

    def get_for_json(self, album):
        vk_sizes = {'s': 1, 'm': 2, 'o': 3, 'p': 4, 'q': 5, 'r': 6, 'x': 7, 'y': 8, 'z': 9, 'w': 10}
        p = []
        for photo in album:
            name = {}
            size = max(photo['sizes'], key=lambda x: vk_sizes[x["type"]])
            name['name'] = photo['likes']['count']
            name['type'] = size['type']
            p.append(name)
        return p

    def get_search_profile(self, sex, age_from, age_to, city):  # id_album: str, id_user: str
        """
        Модуль отправляет запрос на ВК api для поиска пользователей по заданным параметрам
        :param sex: пол ( в реверсе, значение 1 = 2 а 2 = 1 из вк api)
        :param age_from: нижняя граница возраста
        :param age_to: верхняя граница возраста
        :param city: город проживания пользователя
        :return: json файл с найдеными пользователями
        """
        if sex == 1:
            unversary_sex = 2
        elif sex == 2:
            unversary_sex = 1
        url = 'https://api.vk.com/method/users.search'
        params = {'hometown': city,
                  'sex': unversary_sex,
                  'has_photo': '1',
                  'status': '6',
                  'age_from': age_from,
                  'age_to': age_to,
                  'access_token': self.token,
                  'count': '1000',
                  'v': '5.131'}
        response = requests.get(url, params=params)
        with open('../error.txt', 'a') as f:
            f.writelines(f'{str(response.json())}\n')
        return response.json()

    def get_wiew_id(self, vk_json):
        """
        Модуль индификации id пользователя
        :param vk_json: принмает json файл от модуля get_search_profile
        :return: возвращает id одного случайного найденного пользователя
        """
        list_1 = vk_json['response']['items']
        list_id = []
        for dicts in list_1:
            if dicts['is_closed'] == False:
                list_id.append(dicts['id'])
            else:
                continue
        id_s = list_id[random.randint(0, (len(list_id) - 1))]
        pprint(id_s)
        return list_id


    def get_info_user(self, id_user):
        """
        Модуль получает информацию о пользователе по его id vk
        :param id_user: id пользователя
        :return: возвращает пол пользователя
        """
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': str(id_user),
                  'fields': 'city,bdate,sex',
                  'access_token': self.token,
                  'v': '5.131'}
        response = requests.get(url, params=params)
        dict_users = response.json()['response']
        user_list = []
        for user in dict_users:
            user_list.append(user['sex'])
        return user_list

    def get_my_info(self, id_user):
        """
        модуль считывает данные  пользователя бота
        :param id_user: id пользователя
        :return: возвращает Id пользвоателя.
        """
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': str(id_user),
                  'access_token': self.token,
                  'v': '5.131'
                  }
        response = requests.get(url, params=params)
        dict_users = response.json()['response']
        for user_dict in dict_users:
            user_id = user_dict['id']
        return user_id

    def get_all_photo(self, id_user: int):
        """
        Модуль находит все фото на странице искомого человека
        :param id_user:  id где нужно считать фото
        :return: Возвращает json объект
        """
        url = 'https://api.vk.com/method/photos.getAll'
        params = {'owner_id': id_user,

                  'access_token': self.token,
                  'extended': "1",
                  'count': '10',
                  'v': '5.131'}

        response = requests.get(url, params=params)
        return response.json()

    def big_like_photo(self, dict_photo):
        """
        Модуль находит 3 самые популярные фото по кол-ву лайков. если лайков кол-во одинаковое фотографий больше
        :param dict_photo: json файл из модуля get_all_photo
        :return: отформатированная строка для отправки пользователю фотографий
        """
        list_name = []
        for dict_1 in dict_photo['response']['items']:
            for k, v in dict_1.items():
                if k == 'likes':
                    list_name.append(v['count'])
        list_name.sort()
        top_list = list_name[-3:]
        list_1 = []
        for top in top_list:
            for dict_1 in dict_photo['response']['items']:
                if top == dict_1['likes']['count']:
                    list_1.append(f'photo{dict_1["owner_id"]}_{dict_1["id"]}')
        return ','.join(list_1)

    def name_last(self, id_s: int):
        """
        Модуль возвращает имя и фамилию пользователя которого искали
        :param id_s: id пользователя вк
        :return: json файл
        """
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': id_s,
                  'fields': 'first_name,last_name',
                  'access_token': self.token,
                  'extended': "1",
                  'count': '10',
                  'v': '5.131'}
        response = requests.get(url, params=params)
        return response.json()


def search_open_profile(id_user, city, age):
    """
    Функция осуществляет обработку исключений KeyError и  поиск id нужных пользователей
    :param id_user: принимает id пользователя
    :param city: принимает город пользователя
    :param age: принимает возраст в формате age = 32
    :return: возвращает id найденного открытого профиля пользователя
    """
    vk = VkbackUp(TOKEN)
    user = vk.get_info_user(id_user)
    while True:
        try:
            search_love = vk.get_search_profile(user[0], age, age, city)
            search_id = vk.get_wiew_id(search_love)
            time.sleep(1)
            return search_id
        except KeyError:
            continue







def name_love(id_s):
    """
    Имена в формате dict
    :param id: id пользователя в вк
    :return: возвращает в формате словаря фамилию и имя пользователя
    """
    vk = VkbackUp(TOKEN)
    search_profile = vk.name_last(id_s)['response']
    n_m_dict = {}
    for re_list in search_profile:
        n_m_dict['first_name'] = re_list['first_name']
        n_m_dict['last_name'] = re_list['last_name']

    return n_m_dict


def photo_user(id_s):
    """
    Функция возврата фотографий по id вк
    :param id_s: id пользователя вк
    :return: 3 фотографии с максимальным кол-во лайков или более 3 фото если лайков одинаковое кол-во
    """
    vk = VkbackUp(TOKEN)
    all_photo = vk.get_all_photo(id_s)
    bf = vk.big_like_photo(all_photo)

    return bf
