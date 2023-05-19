from vk_api.keyboard import VkKeyboard, VkKeyboardColor

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
