from api.api import vk

def get_likes_from_items(owner_id, items, item_type):
    likes = {}
    for item in items:
        liked = vk.likes.getList(type=item_type, owner_id=owner_id, item_id=item["id"])["items"]

        for id_ in liked:
            (temp_k, temp_v) = likes.get(id_, (id_, 0))
            likes[id_] = (temp_k, temp_v+1)
    
    return sorted(likes.values(), key=lambda x: x[1], reverse=True)    

def get_all_likes_from_photos(user_id):
    owner_id = user_id
    photos = vk.photos.getAll(owner_id=owner_id)["items"]

    return get_likes_from_items(owner_id, photos, "photo")

def get_all_likes_from_wall(user_id):
    owner_id = user_id
    wallposts = vk.wall.get(owner_id=owner_id)["items"]

    return get_likes_from_items(owner_id, wallposts, "post")

def get_all_likes_from_user(user_id):
    photo_likes = get_all_likes_from_photos(user_id)
    wall_likes = get_all_likes_from_wall(user_id)
    all_likes = photo_likes + wall_likes

    likes = {}
    for like in all_likes:
        temp = likes.get(like[0], (like[0], 0))
        likes[like[0]] = (like[0], temp[1] + like[1])
    
    return sorted(likes.values(), key=lambda x: x[1], reverse=True)

if __name__ == "__main__":
    user_id = 51422811 # получение 3 самых лайкаюших фотки людей
    likes = get_all_likes_from_user(user_id)
    print(likes[:3]) 