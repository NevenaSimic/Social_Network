import json

def find_friends(id, data):
    """
    Finds direct friends of a user with an id - id
    :param id:
    :param data:
    :return:
    """
    friends = []
    for user in data:
        if str(user['id']) == str(id):
            friends = user['friends']
            break
    return friends


def read_json_file(file_name='data.json'):
    with open('data.json') as f:
        data = json.load(f)
    return data


def get_users_by_ids(users, data):
    ret_val = []
    for friend in users:
        for user in data:
            if str(user['id']) == str(friend):
                ret_val.append(user)
    return ret_val
