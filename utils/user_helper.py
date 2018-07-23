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

def set_status(is_active, type, auth_user):
    if type == 'client_users':
        client_users = load_client_users()
        client_users[:] = [d for d in client_users if d.get('email') != auth_user['email']]
        if is_active:
            auth_user['isActive'] = True
        else:
            del auth_user['isActive']
        client_users.append(auth_user);

        with open('models/client_users.json', 'w') as file:
            json.dump(client_users, file)

        return True
    if type == 'pi_users':
        pie_users = load_pi_users()
        pie_users[:] = [d for d in pie_users if d.get('email') != auth_user['email']]
        if is_active:
            auth_user['isActive'] = True
        else:
            del auth_user['isActive']
        pie_users.append(auth_user)

        with open('models/pi_users.json', 'w') as file:
            json.dump(pie_users, file)

        return True
    if type == 'admin_users':
        admin_users = load_admin_users()
        admin_users[:] = [d for d in admin_users if d.get('email') != auth_user['email']]
        if is_active:
            auth_user['isActive'] = True
        else:
            del auth_user['isActive']
        admin_users.append(auth_user)

        with open('models/admin_users.json', 'w') as file:
            json.dump(admin_users, file)

        return True


def make_user_active(auth_user, type):
    return set_status(True, type, auth_user)

def make_user_offline(auth_user, type):
    return set_status(False, type, auth_user)
