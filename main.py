from Dbase import main_bd
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from source import vk_search
import configparser
from source.bot_send import Vkinder
config = configparser.ConfigParser()  # создаём объекта парсера
config.read("settings.ini")  # читаем конфиг
TOKEN = config['DEFAULT']['vk_group_token']




HELP = """нажми на кнопку  [поиск] или напиши "поиск" для начала работы бота"""

if __name__ == '__main__':
    vkt = Vkinder(TOKEN)
    vk = vk_api.VkApi(token=TOKEN)
    longpoll = VkLongPoll(vk)
    viewed = []
    vieved_1 = set()
    print('Бот запущен')
    while True:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                request = event.text
                msg = event.text
                sender = event.user_id
                if request.lower() == 'поиск':
                    vkt.get_write_msg(sender, 'Какой у вас город?')
                    city = vkt.get_save_arg(longpoll)
                    vkt.get_write_msg(sender, 'Какой возраст предпочитаете? ')
                    age = vkt.get_save_arg(longpoll)
                    vkt.get_write_msg(sender, 'Сейчас поищем...')
                    ids_list = vk_search.search_open_profile(sender, city, age)
                    x = ids_list[0]
                    viewed.append(x)
                    vieved_1.add(x)
                    name_last = vk_search.name_love(x)
                    photos = vk_search.photo_user(x)
                    vkt.get_write_msg(sender, f'влюбитесь и радуйтесь https://vk.com/id{x}')
                    vkt.get_write_msg(sender, f'{name_last["last_name"]} {name_last["first_name"]}')
                    vkt.get_link_mess(sender, " ", photos)
                    linked = f'https://vk.com/id{x}'
                elif request.lower() == 'далее':
                    try:
                        ids_list.pop(0)
                        x = ids_list[0]
                    except IndexError:
                        vkt.get_write_msg(sender, f'Не осталось кандидатов Давайте попробуем новый поиск?')
                        break

                    name_last = vk_search.name_love(x)
                    photos = vk_search.photo_user(x)
                    vkt.get_write_msg(sender, f'{name_last["last_name"]} {name_last["first_name"]}')
                    vkt.get_write_msg(sender, f'влюбитесь и радуйтесь https://vk.com/id{x}')
                    vkt.get_link_mess(sender, " ", photos)

                elif request.lower() == 'добавить в избранное':
                    insert = main_bd.open_base(sender, x, name_last["first_name"], name_last["last_name"], age, linked)
                    vkt.get_write_msg(sender, 'Добавил в избранное')


                elif request.lower() == '🥰избранное🥰':
                    liked_users = main_bd.get_liked_user(sender)
                    vkt.get_write_msg(sender, f'{liked_users}')

                else:
                    vkt.get_write_msg(sender, HELP)
