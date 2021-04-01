import vk_api
from settings import token

def get_friends(id):
    return vk.friends.get(user_id=id)["items"]

def get_mutual_friends(s_id, t_id):
    return vk.friends.getMutual(source_uid=s_id, target_uid=t_id)

def get_group(root_id, friend_id):
    potencial_group = get_mutual_friends(root_id, friend_id)
    real_group = set([root_id, friend_id])

    while len(potencial_group) > 0:
        first_user = potencial_group[0]

        user_friends = set(get_mutual_friends(root_id, first_user))
        intersection = user_friends & real_group

        if len(intersection) * 2 >= len(real_group):
            real_group.add(first_user)
            new_potentials = user_friends - set(potencial_group) - real_group
            potencial_group.extend(new_potentials)
        
        potencial_group.pop(0)
    
    return list(real_group)

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()

id = 51422811

friend_ids = get_friends(id)

print(get_group(id, friend_ids[0]))