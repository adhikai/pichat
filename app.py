from flask import Flask
from flask import request
from flask import redirect
from flask import session
from flask import render_template
import utils.user_helper as user_helper
from flask import jsonify
from wrappers import Authenticated
import utils.globals as universal

app = Flask(__name__)
Flask.secret_key = "SOME SECRET KEY HERE"

universal.client_users = []
universal.pi_users = []
universal.admin_users = []


def sync_users():
    global universal
    universal.client_users = user_helper.load_client_users()
    universal.pi_users = user_helper.load_pi_users()
    universal.admin_users = user_helper.load_admin_users()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        sync_users()
        try:
            data = request.get_json()
            email = data['email']
            password = data['password']
        except AttributeError:
            return jsonify({"error": "Email and Password are required"})

        for user in universal.client_users:
            if user['email'] == email and user['password'] == password:
                session['auth_user'] = user
                break
            else:
                session['auth_user'] = {}

        if session['auth_user'] == {}:
            for user in universal.pi_users:
                if user['email'] == email and user['password'] == password:
                    session['auth_user'] = user
                    break
                else:
                    session['auth_user'] = {}
        if session['auth_user'] != {}:
            return redirect("/chats", 302)
        else:
            return jsonify({"error": "Check your email and password combination"})
    else:
        return render_template('login/user_login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    sync_users()
    if request.method == 'GET':
        return render_template('/signup/signup_client.html')
    else:
        try:
            data = request.get_json()
            first_name = data['first_name']
            last_name = data['last_name']
            email = data['email']
            password = data['password']
        except KeyError:
            return jsonify({"error": "All fields are require and should be valid"})

        is_unique = True
        for user in universal.client_users:
            if user['email'] == email:
                is_unique = False
                break
        for user in universal.pi_users:
            if user['email'] == email:
                is_unique = False
                break
        for user in universal.admin_users:
            if user['email'] == email:
                is_unique = False
                break

        if is_unique:
            status = user_helper.write_client_users({
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": password
            })

            if status:
                return redirect('/login', 302)
            else:
                return jsonify({"error": "Unable to register right now!"})
        else:
            return jsonify({"error": "Account already exists!"})


@app.route('/logout', methods=['GET'])
def logout():
    session['auth_user'] = {}
    return redirect('/login', 302)


@app.route('/chats', methods=['GET'])
@Authenticated.require_authentication
def chat_view():
    return render_template('chats/index.html')


@app.route('/users/active', methods=['GET'])
@Authenticated.require_authentication
def active_users():
    sync_users()
    if 'isPieUser' in session['auth_user']:
        users = []
        for user in universal.client_users:
            if 'isActive' in user:
                users.append(user)
        return jsonify(users)
    else:
        users = []
        for user in universal.pi_users:
            if 'isActive' in user:
                users.append(user)
        return jsonify(users)


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        sync_users()
        try:
            data = request.get_json()
            email = data['email']
            password = data['password']
        except AttributeError:
            return jsonify({"error": "Email and Password are required"})

        for user in universal.admin_users:
            if user['email'] == email and user['password'] == password:
                session['auth_user'] = user
                break
            else:
                session['auth_user'] = {}

        if session['auth_user'] != {}:
            return redirect("/admin", 302)
        else:
            return jsonify({"error": "Check your email and password combination"})
    else:
        return render_template('admin/admin_login.html')


@app.route('/admin', methods=['GET'])
@Authenticated.require_admin_authentication
def admin_show_active_users():
    sync_users()
    client_users = user_helper.load_client_users()
    pie_users = user_helper.load_pi_users()
    admin_users = user_helper.load_admin_users()

    if request.args.get('filter') == 'active':
        active_client_users = []
        for user in client_users:
            if 'isActive' in user:
                active_client_users.append(user)

        active_pi_users = []
        for user in pie_users:
            if 'isActive' in user:
                active_pi_users.append(user)

        active_admin_users = []
        for user in admin_users:
            if 'isActive' in user:
                active_admin_users.append(user)
        client_users = active_client_users
        pie_users = active_pi_users
        admin_users = active_admin_users

    return jsonify({
        "client_users": client_users,
        "pie_users": pie_users,
        "admin_users": admin_users
    })


@app.route('/admin/pi', methods=['GET', 'POST'])
@Authenticated.require_admin_authentication
def admin_add_pie_user():
    sync_users()
    if request.method == 'POST':
        try:
            data = request.get_json()
            first_name = data["first_name"]
            last_name = data['last_name']
            email = data['email']
            password = data['password']
            serial_number = data['serial_number']
        except KeyError:
            return jsonify({"error": "All fields are required"})

        is_unique = True
        for user in universal.client_users:
            if user['email'] == email:
                is_unique = False
                break
        for user in universal.pi_users:
            if user['email'] == email:
                is_unique = False
                break
        for user in universal.admin_users:
            if user['email'] == email:
                is_unique = False
                break

        if is_unique:
            status = user_helper.write_pie_users({
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": password,
                "serial_number": serial_number
            })

            if status:
                return jsonify({"message": "Pi Successfully Registered!"})
            else:
                return jsonify({"error": "Unable to register the pi at the moment!"})
        else:
            return jsonify({"error": "User already registered!"})
    else:
        return render_template('admin/pi_signup.html')
