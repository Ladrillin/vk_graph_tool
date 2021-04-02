import networkx as nx
import matplotlib.pyplot as mpl
from vk_api.exceptions import ApiError
import json

from api import vk


def parse_friends(root_id, root_friendlist):
    graph_network = nx.Graph()
    graph_network.add_node(root_id)
    edge_counter = 0
    check_if_closed = vk.users.get(user_ids=root_friendlist['items'])
    index = 0

    for friend_id in root_friendlist['items']:  # Связь рута со всеми его друзьями
        graph_network.add_edge(root_id, friend_id)

    for root_mutual_friend_id in root_friendlist['items']:  # Связи между друзьями рута
        try:  # Замена try, возможно полетит по пизде в будущем
            get_mutual = vk.friends.getMutual(source_uid=root_id,
                                              target_uid=root_mutual_friend_id)
            for mutual_friend in get_mutual:
                graph_network.add_edge(root_mutual_friend_id, mutual_friend)
                edge_counter += 1
        except:
            continue

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
                graph_network.add_edge(root_id, friend_layer2)
                print(friend_layer2)

    nx.draw(graph_network, with_labels=True,
            font_color='g', font_size=12, font_weight='bold')
    print(edge_counter)
    return mpl.show()


source_id = 141498951
source_friends = vk.friends.get(user_id=source_id,)
parse_friends(source_id, source_friends)
