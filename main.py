import requests
import main_bd
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardButton, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import vk_search
import configparser

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("settings.ini")  # читаем конфиг
TOKEN = config['DEFAULT']['vk_group_token']

keyboard = VkKeyboard(one_time=True)
keyboard.add_button('Поиск', color=VkKeyboardColor.SECONDARY)
keyboard.add_button('🥰Избранное🥰', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button('Далее', color=VkKeyboardColor.POSITIVE)
keyboard.add_button('Добавить в избранное', color=VkKeyboardColor.POSITIVE)

keyboard2 = VkKeyboard(one_time=True)
keyboard2.add_button('Далее', color=VkKeyboardColor.SECONDARY)
keyboard2.add_button('Добавить в избранное', color=VkKeyboardColor.POSITIVE)
keyboard2.add_button('🥰Избранное🥰', color=VkKeyboardColor.POSITIVE)


def get_write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id,
                                'message': message,
                                'random_id': get_random_id(),
                                'keyboard': keyboard.get_keyboard()})


def get_link_mess(user_id, message, link):
    vk.method('messages.send', {'user_id': user_id,
                                'message': message,
                                'attachment': link,
                                'random_id': get_random_id(),
                                'keyboard': keyboard2.get_keyboard()})


def get_save_arg(log_l):
    for event in log_l.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            request = event.text
            msg = event.text
            sender = event.user_id
            if request.lower() != '':
                return request
            break


HELP = """напиши слово  поиск для начала работы бота"""

if __name__ == '__main__':

    vk = vk_api.VkApi(token=TOKEN)
    longpoll = VkLongPoll(vk)
    # db = Service(session)
    print('Бот запущен')
    while True:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                request = event.text
                msg = event.text
                sender = event.user_id
                if request.lower() == 'поиск':
                    get_write_msg(sender, 'Какой у вас город?')
                    city = get_save_arg(longpoll)
                    get_write_msg(sender, 'Какой возраст предпочитаете? ')
                    age = get_save_arg(longpoll)
                    get_write_msg(sender, 'Сейчас поищем...')
                    x = vk_search.search_open_profile(sender, city, age)
                    name_last = vk_search.name_love(x)
                    photos = vk_search.photo_user(x)
                    get_write_msg(sender, f'влюбитесь и радуйтесь https://vk.com/id{x}')
                    get_write_msg(sender, f'{name_last["last_name"]} {name_last["first_name"]}')
                    get_link_mess(sender, " ", photos)
                    linked = f'https://vk.com/id{x}'
                elif request.lower() == 'далее':
                    x = vk_search.search_open_profile(sender, city, age)
                    name_last = vk_search.name_love(x)
                    photos = vk_search.photo_user(x)
                    get_write_msg(sender, f'{name_last["last_name"]} {name_last["first_name"]}')
                    get_write_msg(sender, f'влюбитесь и радуйтесь https://vk.com/id{x}')
                    get_link_mess(sender, " ", photos)

                elif request.lower() == 'добавить в избранное':
                    insert = main_bd.open_base(sender, x, name_last["first_name"], name_last["last_name"], age, linked)
                    get_write_msg(sender, 'Добавил в избранное')


                elif request.lower() == '🥰избранное🥰':
                    liked_users = main_bd.get_liked_user(sender)
                    get_write_msg(sender, f'{liked_users}')
