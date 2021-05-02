from api.api import vk

def get_all_likes_from_photos(user_id):
    owner_id = user_id
    photos = vk.photos.getAll(owner_id=owner_id)["items"]

    likes = {}
    for photo in photos:
        liked = vk.likes.getList(type="photo", owner_id=owner_id, item_id=photo["id"])["items"]
        
        for id_ in liked:
            (temp_k, temp_v) = likes.get(id_, (id_, 0))
            likes[id_] = (temp_k, temp_v+1)
    
    return sorted(likes.values(), key=lambda x: x[1], reverse=True) # да да, опять приводим к нормальному виду данные

if __name__ == "__main__":
    user_id = 51422811 # получение 3 самых лайкаюших фотки людей
    likes = get_all_likes_from_photos(user_id)
    print(likes[:3]) 