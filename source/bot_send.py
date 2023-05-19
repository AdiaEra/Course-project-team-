import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from source.keyboards import keyboard, keyboard2


class Vkinder:
    def __init__(self, TOKEN):
        self.vk = vk_api.VkApi(token=TOKEN)

    def get_write_msg(self, user_id, message, ):
        self.vk.method('messages.send', {'user_id': user_id,
                                         'message': message,
                                         'random_id': get_random_id(),
                                         'keyboard': keyboard.get_keyboard()})

    def get_link_mess(self, user_id, message, link):
        self.vk.method('messages.send', {'user_id': user_id,
                                         'message': message,
                                         'attachment': link,
                                         'random_id': get_random_id(),
                                         'keyboard': keyboard2.get_keyboard()})

    def get_save_arg(self, log_l):
        for event in log_l.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                request = event.text
                if request.lower() != '':
                    return request
                break
