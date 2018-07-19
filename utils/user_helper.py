import json


def load_client_users():
    with open('models/client_users.json') as file:
        return json.load(file)


def load_pi_users():
    with open('models/pi_users.json') as file:
        return json.load(file)


def load_admin_users():
    with open('models/admin_users.json') as file:
        return json.load(file)


def write_client_users(data):
    client_users = load_client_users()
    with open('models/client_users.json', 'w',  encoding='utf-8') as file:
        client_users.append(data)
        json.dump(client_users, file)
        return True


def write_pie_users(data):
    pie_users = load_pi_users()
    with open('models/pi_users.json', 'w') as file:
        pie_users.append(data)
        json.dump(pie_users, file)
        return True


def write_admin_users(data):
    admin_users = load_admin_users()
    with open('models/pi_users.json', 'w') as file:
        admin_users.append(data)
        json.dump(admin_users, file)
        return True
