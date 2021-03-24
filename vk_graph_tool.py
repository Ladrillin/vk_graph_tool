import vk_api
import networkx as nx
import matplotlib.pyplot as mpl


def auth_handler():
    code = input('Input auth code: ')
    remember_device = True
    return code, remember_device


def parse_friends(root_id, root_friendlist):
    graph_network = nx.Graph()
    graph_network.add_node(root_id)

    for friend in root_friendlist['items']:  # Связь рута со всеми его друзьями
        graph_network.add_edge(root_id, friend)

    for root_mutual_friend in root_friendlist['items']:  # Связи между друзьями рута
        try:
            mutual_list = vk.friends.getMutual(source_uid=root_id,
                                               target_uid=root_mutual_friend)
            for mutual_friend in mutual_list:
                if graph_network.has_edge(root_mutual_friend, mutual_friend):
                    continue
                graph_network.add_edge(root_mutual_friend, mutual_friend)
#############################################
            friends_of_friend_list = vk.friends.get(user_id=root_mutual_friend)
            for friend_of_friend in friends_of_friend_list['items']:
                level3_friends = vk.friends.get(user_id=friend_of_friend)
                if root_id in level3_friends['items'] and not graph_network.has_edge(root_id, friend_of_friend):
                    graph_network.add_edge(root_id, friend_of_friend)
                    print(friend_of_friend)
#############################################
        except vk_api.exceptions.ApiError:  # Эксепшн для случаев, когда профиль юзера закрыт
            continue

    nx.draw(graph_network, with_labels=True,
            font_color='g', font_size=10, font_weight='bold')
    print(graph_network.number_of_nodes())
    print(graph_network.number_of_edges())
    return mpl.show()


# with open('access_to_vk.txt', 'r') as access_file:
#     login = access_file.readline()
#     password = access_file.readline()

token = '144b6950bfc8fcd8b7d2f98b8b4b30b380dea558040a471d2e1c500b1c6e611198b8d4b0b7d154f392244'
vk_session = vk_api.VkApi(token=token)
# try:
#     vk_session.auth()
# except vk_api.AuthError as error_msg:
#     print(error_msg)
vk = vk_session.get_api()

source_id = 142898628
source_friends = vk.friends.get(user_id=source_id,)
friends_info = vk.users.get(user_ids=source_friends['items'])
print(source_friends)
print('Drawing graph...')
parse_friends(source_id, source_friends)
