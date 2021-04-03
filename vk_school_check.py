from api import vk

fields = "sex, bdate, city, country, home_town, has_mobile, contacts, education, universities, schools, occupation, relatives, relation, personal, connections, activities, interests, music, movies, tv, books, games, about, timezone, maiden_name, career, military"

def get_friends_info(id):
    res = vk.friends.get(user_id=id)
    friend_ids = res["items"]

    return vk.users.get(user_ids=friend_ids, fields=fields)

def get_school_most_time(schools):
    if len(schools) == 1: 
        return schools[0]["name"]

    max_diff = -1
    school_with_most_time = ""

    for school in schools:
        year_from = school.get("year_from", 0)
        year_to = school.get("year_to", 0)
        diff = year_to - year_from

        if diff > max_diff:
            max_diff = diff
            school_with_most_time = school["name"]
        
    return school_with_most_time

def get_potencial_schools(friends_info):
    school_counters = {}
    counter = 0

    for info in friends_info:
        schools = info.get("schools", [])
        
        if schools:
            school_name = get_school_most_time(schools) # вот тут надо на самом деле подумать о том, как взять школу

            c = school_counters.get(school_name, 0)
            school_counters[school_name] = c + 1

            counter += 1

    for school_name, value in school_counters.items():
        school_counters[school_name] = round(value / counter * 100)

    return school_counters

""" if __name__ == "__main__":
    id = 154623861

    friends_info = get_friends_info(id)
    school_counters = get_potencial_schools(friends_info)

    for name, value in school_counters.items():
        print(f"{value} - {name}") """

# ---------------------------------------------------------------------------
# 2 idea

from vk_group_find import get_group # method to find groups from vk
from dbF.get_groups import get_groups, add_group # method to get and add already parsed groups from vk

id = 51422811

groups = get_groups(id)
print(groups)

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
