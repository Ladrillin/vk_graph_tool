import vk_api
from .setting_example import token

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
