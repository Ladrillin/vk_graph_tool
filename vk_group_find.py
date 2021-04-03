from api import vk
from dbF.get_groups import get_groups, add_group # method to get and add already parsed groups from vk

def get_friends(id):
    return vk.friends.get(user_id=id)["items"]

def get_mutual_friends(s_id, t_id):
    try:
        res = vk.friends.getMutual(source_uid=s_id, target_uid=t_id)
        return res
    except:
        print(f"{t_id} profile is private")
        return []

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


def get_groups_by_id(id):
    groups = get_groups(id)

    if len(groups) < 1:
        res = vk.friends.get(user_id=id)["items"]
        
        while len(res) > 0:
            friend_id = res[0]
            group = get_group(id, friend_id)

            res = list(set(res) - set(group))

            if len(group) > 5: # Здесь можно подумать о том, со скольки человек считать некое сообщество залинкованных друзей группой
                groups.append(group)
                add_group(id, group)
        
        return groups

    return list(map(lambda x: [int(y) for y in x[0].split(" ")], groups))


if __name__ == "__main__":
    id = 51422811
    print(get_groups_by_id(id))