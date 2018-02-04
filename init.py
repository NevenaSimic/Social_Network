from flask import Flask, jsonify
from utils import *
import itertools

app = Flask(__name__)

@app.route("/")
def getAllMembers():
    data = read_json_file()
    return jsonify(data)


@app.route('/getFriends/<id>')
def getFriends(id):
    """
    Direct friends: those people who are directly connected to the chosen user (required);
    :param id: id of a friend
    :return: json
    """
    data = read_json_file()
    friends = find_friends(id, data)
    ret_val = get_users_by_ids(friends, data)
    return jsonify(ret_val)


@app.route('/getFriendsOfFriends/<id>')
def getFriendsOfFriends(id):
    """
    Friends of friends: those who are two steps away from the chosen 
    user but not directly connected to the chosen user (required);
    :return: 
    """
    friends_of_friends = []
    data = read_json_file()
    friends = find_friends(id, data)

    # find friends of friends
    for friend in friends:
        for user in data:
            if str(user['id']) == str(friend):
                friends_of_friends.append(user['friends'])

    friends_of_friends = sum(friends_of_friends, [])    # flatten list
    friends_of_friends = list(set(friends_of_friends))  # remove duplicates
    friends_of_friends.remove(int(id))     # remove self from fof
    friends_of_friends = [fof for fof in friends_of_friends if fof not in friends]     # remove friends from fof

    ret_val = get_users_by_ids(friends_of_friends, data)
    return jsonify(ret_val)


@app.route('/getSuggestions/<id>')
def getSuggestions(id):
    ret_val = []

    data = read_json_file()
    friends = find_friends(id, data)

    # ako ima vise od dva prijatelja
    if len(friends) >= 2:
        # nadji sve kombinacije prijatelja
        combinations = list(itertools.combinations(friends, 2))
        # find friends of friends
        for user in data:
            if str(user['id']) != str(id):
                # proveri da li u prijateljima ima neku od kombinacija
                for combination in combinations:
                    if set(combination).issubset(user['friends']) and int(id) not in user['friends']:
                        ret_val.append(user)
    else:
        return "Nema sugestija za korisnika " + str(id)
    return jsonify(ret_val)


if __name__ == "__main__":
    app.run()