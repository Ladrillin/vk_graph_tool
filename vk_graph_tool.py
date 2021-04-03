import networkx as nx
import matplotlib.pyplot as mpl
from api import vk


def if_closed(user_list):
    info = vk.users.get(user_ids=user_list)
    check_if_closed = dict()
    for user in info:
        user_id = user['id']
        if 'deactivated' in user:
            check_if_closed[user_id] = False
            continue
        user_closed_state = user["can_access_closed"]
        check_if_closed[user_id] = user_closed_state
    return check_if_closed  # Словарь вида 'id': True/False - закрыт/открыт профиль (либо удален)


def graph_drawer(root_id, root_friendlist):
    graph_network = nx.Graph()
    graph_network.add_node(root_id)
    edge_counter = 0
    check_if_closed = if_closed(root_friendlist['items'])

    for friend_id in root_friendlist['items']:  # Связь рута со всеми его друзьями
        print('Drawing the first layer of Graph')
        graph_network.add_edge(root_id, friend_id)

    for root_mutual_friend_id in root_friendlist['items']:  # Связи между друзьями рута
        print('Drawing the second layer of Graph')
        if check_if_closed[root_mutual_friend_id]:
            get_mutual = vk.friends.getMutual(source_uid=root_id,
                                              target_uid=root_mutual_friend_id)
            for mutual_friend in get_mutual:
                graph_network.add_edge(root_mutual_friend_id, mutual_friend)
                edge_counter += 1
        else:
            continue
    nx.draw(graph_network, with_labels=True,
            font_color='g', font_size=12, font_weight='bold')
    print(edge_counter)
    return mpl.show()


def find_hidden_friends(root_id, root_friendlist):  # Очень долго
    print('Getting into hidden layer')
    for friend_layer1 in root_friendlist['items']:
        print('Признаки жизни')
        try:
            layer1_list = vk.friends.get(user_id=friend_layer1)
        except:
            continue
        for friend_layer2 in layer1_list['items']:
            try:
                layer2_list = vk.friends.get(user_id=friend_layer2)
            except:
                continue
            if root_id in layer2_list['items'] and friend_layer2 not in root_friendlist['items']:
                print(friend_layer2)


source_id = 141498951
source_friends = vk.friends.get(user_id=source_id,)
graph_drawer(source_id, source_friends)
