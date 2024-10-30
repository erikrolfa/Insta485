"""
Insta485 logout view.

URLs include:
/accounts/
/accounts/logout/
"""
import uuid
import hashlib
import pathlib
import os
import flask
import insta485


@insta485.app.route('/accounts/', methods=['POST'])
def account_update():
    """Display /accounts/ route."""
    print(000)
    op_type = flask.request.form.get('operation')

    if op_type == "login":
        return operation_login()
    if op_type == "delete":
        return operation_delete()
    if op_type == "edit_account":
        return operation_edit()
    if op_type == "create":
        return operation_create()
    return operation_password()


@insta485.app.route('/accounts/auth/')
def account_auth():
    """Display /accounts/auth/ route."""
    if 'username' not in flask.session:
        flask.abort(403)
    else:
        return flask.Response(status=200)


def operation_login():
    """Operates login."""
    user = flask.request.form.get('username')
    passwd = flask.request.form.get('password')

    # check if user or pw fields are empty
    if not user:
        flask.abort(400)
    if not passwd:
        flask.abort(400)
    # check if user/pw authentificaton fails
    # response = account_auth()
    curse = insta485.model.get_db()
    cur = curse.execute("SELECT * FROM users WHERE users.username = ?",
                        (user, ))
    pup = cur.fetchall()
    # print(pup)
    if len(pup) == 0:
        flask.abort(403)
    userpassword = {}
    passwd = flask.request.form.get('password')
    cur = curse.execute('''SELECT users.password
                        FROM users WHERE users.username = ?''',
                        (user, ))
    userpassword = cur.fetchall()
    hashed_pass_full = userpassword[0]['password']
    hashed_pass = hashed_pass_full.split("$")

    algorithm = 'sha512'
    salt = hashed_pass[1]
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + passwd
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string1 = "$".join([algorithm,
                                    salt, password_hash])

    if hashed_pass_full != password_db_string1:
        flask.abort(403)

    insta485.model.close_db(curse)
    flask.session['username'] = flask.request.form['username']
    username = flask.session['username']
    print(username)
    return flask.redirect(flask.request.args.get('target',
                                                 default='/'))


def operation_create():
    """Operates create."""
    user = flask.request.form.get('username')
    passwd = flask.request.form.get('password')
    fullname = flask.request.form.get('fullname')
    email = flask.request.form.get('email')

    fileobj = flask.request.files["file"]
    filename = fileobj.filename

    stem = uuid.uuid4().hex
    suffix = pathlib.Path(filename).suffix.lower()
    uuid_basename = f"{stem}{suffix}"

    path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
    fileobj.save(path)

    # check if any fields are empty
    if not user:
        flask.abort(400)
    if not passwd:
        flask.abort(400)
    if not fullname:
        flask.abort(400)
    if not email:
        flask.abort(400)
    if not filename:
        flask.abort(400)

    # check if user tries to create acc with existing username
    curse = insta485.model.get_db()
    cur = curse.execute('''SELECT users.username FROM users
                        WHERE users.username = ?''', (user, ))
    check = cur.fetchall()
    if len(check) != 0:
        flask.abort(409)

    # store cookie
    flask.session['username'] = flask.request.form['username']
    username = flask.session['username']
    print(username)

    # insert into db
    cur = curse.execute('''INSERT INTO
                        users (username, fullname,
                        email, filename, password)
                        VALUES (?, ?, ?, ?, ?) ''',
                        (user, fullname, email, filename,
                            hash_func(passwd)))

    insta485.model.close_db(curse)
    return flask.redirect(flask.request.args.get('target', default='/'))


def hash_func(passwd):
    """Hash function."""
    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + passwd
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string


def operation_delete():
    """Operate delete."""
    if 'username' not in flask.session:
        flask.abort(403)
    user = flask.session['username']
    print(user)
    # filename = flask.request.form.get('file')
    # print(filename)
    # fileobj = flask.request.form.get('file')
    # file = fileobj.filename
    # print(file)
    curse = insta485.model.get_db()
    post_list = {}
    cur = curse.execute("SELECT filename FROM posts WHERE posts.owner = ?",
                        (user, ))
    post_list = cur.fetchall()
    print(post_list)
    for post in post_list:
        file = post['filename']
        path = os.path.join(insta485.app.config["UPLOAD_FOLDER"],
                            file)
        os.remove(path)

    pup = cur.fetchall()
    print(pup)
    # cur = curse.execute("SELECT * FROM users WHERE users.username = ?"
    #                     , (user, ))
    # pup1 = cur.fetchall()
    # print(pup1)
    cur = curse.execute("DELETE FROM users WHERE users.username = ?",
                        (user, ))
    curse.commit()
    # cur = curse.execute("SELECT * FROM users WHERE users.username = ?"
    #                     , (user, ))
    # pup2 = cur.fetchall()
    # print(pup2)
    insta485.model.close_db(curse)
    flask.session.clear()
    return flask.redirect(flask.url_for('account_create'))


def operation_edit():
    """Operate edit."""
    fullname = flask.request.form.get('fullname')
    email = flask.request.form.get('email')
    fileobj = flask.request.files['file']
    user = flask.session['username']

    if 'username' not in flask.session:
        flask.abort(403)
    if not fullname:
        flask.abort(400)
    if not email:
        flask.abort(400)

    curse = insta485.model.get_db()
    cur = curse.execute('''UPDATE users
                        SET fullname = ?,
                        email = ?
                        WHERE username = ?''',
                        (fullname, email, user, ))
    if fileobj:
        filename2 = fileobj.filename
        cur = curse.execute('''SELECT users.filename
                            FROM users
                            WHERE username = ?''',
                            (user, ))
        old_file = cur.fetchall()
        old_path = os.path.join(insta485.app.config["UPLOAD_FOLDER"],
                                old_file[0]['filename'])
        os.remove(old_path)

        stem = uuid.uuid4().hex
        suffix = pathlib.Path(filename2).suffix.lower()
        uuid_basename = f"{stem}{suffix}"

        path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
        fileobj.save(path)
        cur = curse.execute('''UPDATE users
                            SET
                            filename = ?
                            WHERE username = ?''',
                            (uuid_basename, user, ))

        insta485.model.close_db(curse)
    return flask.redirect(flask.request.args.get('target',
                                                 default='/'))


def operation_password():
    """Operate password."""
    if 'username' not in flask.session:
        flask.abort(403)
    passwd = flask.request.form.get('password')
    passwd1 = flask.request.form.get('new_password1')
    passwd2 = flask.request.form.get('new_password2')
    user = flask.session['username']
    print(passwd)

    if not passwd:
        flask.abort(400)
    if not passwd1:
        flask.abort(400)
    if not passwd2:
        flask.abort(400)

    print(user)
    userpassword = {}
    curse = insta485.model.get_db()
    cur = curse.execute('''SELECT users.password
                        FROM users WHERE users.username = ?''',
                        (user, ))
    userpassword = cur.fetchall()
    print(userpassword)

    hashed_pass_full = userpassword[0]['password']
    hashed_pass = hashed_pass_full.split("$")

    algorithm = 'sha512'
    salt = hashed_pass[1]
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + passwd
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm,
                                  salt, password_hash])

    if hashed_pass_full != password_db_string:
        flask.abort(403)

    if passwd1 != passwd2:
        flask.abort(401)

    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + passwd1
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm,
                                   salt, password_hash])

    cur = curse.execute("UPDATE users SET password = ?",
                        (password_db_string, ))
    curse.commit()
    insta485.model.close_db(curse)

    return flask.redirect(flask.request.args.get('target',
                                                 default='/'))
