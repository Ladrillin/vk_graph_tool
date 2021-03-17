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
    edge_counter = 0

    for friend_id in root_friendlist['items']:  # Связь рута со всеми его друзьями
        graph_network.add_edge(root_id, friend_id)

    for root_mutual_friend_id in root_friendlist['items']:  # Связи между друзьями рута
        try:
            get_mutual = vk.friends.getMutual(source_uid=root_id,
                                              target_uid=root_mutual_friend_id)
            for mutual_friend in get_mutual:
                graph_network.add_edge(root_mutual_friend_id, mutual_friend)
                edge_counter += 1
        except vk_api.exceptions.ApiError:  # Эксепшн для случаев, когда профиль юзера закрыт
            continue

    nx.draw(graph_network, with_labels=True, font_color='g', font_size=12)
    print(edge_counter)
    return mpl.show()


with open('access_to_vk.txt', 'r') as access_file:
    login = access_file.readline()
    password = access_file.readline()

vk_session = vk_api.VkApi(login=login,
                          password=password,
                          auth_handler=auth_handler)
try:
    vk_session.auth()
except vk_api.AuthError as error_msg:
    print(error_msg)
vk = vk_session.get_api()

source_id = 142898628
source_friends = vk.friends.get(user_id=source_id,)
parse_friends(source_id, source_friends)
