# Урок 11. CSS и шаблонизация

import json
from flask import Flask, request, render_template, redirect
app = Flask(__name__)


@app.route('/')
def index_():
    with open("users.json", "r", encoding="utf-8") as read_file:
        users = json.load(read_file)
    # return users[1]['name']
    return render_template('index.html', users=users)


@app.route('/search/')
def search_():
    with open("users.json", "r", encoding="utf-8") as read_file:
        users = json.load(read_file)

    search_name = request.args.get('name')
    found_users = []
    if search_name:
        for user in users:
            if search_name.lower() in user['name'].lower():
                found_users.append(user)
    return render_template('search.html', users=found_users, found=len(found_users))


@app.route('/add_user/', methods=['GET', 'POST'])
def add_user_():
    if request.method == "GET":
        return render_template('add_user.html')
    elif request.method == "POST":

        with open("users.json", "r", encoding="utf-8") as read_file:
            users = json.load(read_file)

        if request.form.get("name") == "":
            message_ = "Имя - обязательное поле!"
            return render_template('add_user.html', message=message_)

        save_user = {}
        save_user["name"] = request.form.get("name")
        if request.form.get("age") != "":
            save_user["age"] = int(request.form.get("age"))
        if request.form.get("is_blocked") == "on":
            save_user["is_blocked"] = True
            if request.form.get("unblock_date") != "":
                save_user["unblock_date"] = request.form.get("unblock_date")
        else:
            save_user["is_blocked"] = False

        users.append(save_user)

        with open("users.json", "w", encoding="utf-8") as write_file:
            json.dump(users, write_file, ensure_ascii=False)

        url_ = '/search/?name=' + save_user['name']
        return redirect(url_)


app.run()
