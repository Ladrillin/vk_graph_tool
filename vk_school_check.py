import vk_api
from settings import token

fields = "sex, bdate, city, country, home_town, has_mobile, contacts, education, universities, schools, occupation, relatives, relation, personal, connections, activities, interests, music, movies, tv, books, games, about, timezone, maiden_name, career, military"

def get_friends_info(id):
    res = vk.friends.get(user_id=id)
    friend_ids = res["items"]

    return vk.users.get(user_ids=friend_ids, fields=fields)

def get_potencial_schools(info):
    school_counters = {}
    counter = 0

    for info in friends_info:
        school = info.get("schools", [])
        
        if school:
            school_name = school[0]["name"] # вот тут надо на самом деле подумать о том, как взять школу, а не только первую

            c = school_counters.get(school_name, 0)
            school_counters[school_name] = c + 1

            counter += 1

    for school_name, value in school_counters.items():
        school_counters[school_name] = round(value / counter * 100)

    return school_counters

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()

friends_info = get_friends_info(50802341)
school_counters = get_potencial_schools(friends_info)

for name, value in school_counters.items():
    print(f"{name} - {value}")

# best_school_possibility = max(school_counters, key=school_counters.get)

# print(best_school_possibility)
