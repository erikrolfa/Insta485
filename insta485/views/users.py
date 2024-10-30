"""
Insta485 users view.

URLs include:
/users/
"""
import flask
import insta485


@insta485.app.route('/users/<username>/')
def show_user(username):
    """Display /users/<username> route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))

    curse = insta485.model.get_db()
    loguser = flask.session['username']
    # username = flask.request.get.args('username')

    cur = curse.execute('''SELECT users.username
                       FROM users WHERE users.username
                       = ?''', (username, ))
    check = cur.fetchall()
    # check if user exists
    if len(check) == 0:
        flask.abort(404)
    print(check)

    print(loguser)
    relation = 2

    # display posts
    cur = curse.execute('''SELECT posts.filename,
                        posts.postid FROM posts
                        WHERE owner = ?''',
                        (username, ))
    postuser = cur.fetchall()
    print(postuser)

    # name
    cur = curse.execute('''SELECT users.fullname
                       FROM users WHERE username
                       = ?''', (username, ))
    name = cur.fetchall()
    print(name)

    # relationship
    cur = curse.execute('''SELECT following.username2
                       FROM following WHERE
                       following.username1 = ?''', (username, ))
    follows = cur.fetchall()
    print(follows)

    if username == loguser:
        relation = 0
    else:
        cur = curse.execute("SELECT COUNT(*) from following")
        for follow in follows:
            if follow['username2'] == username:
                relation = 1

    # number of posts
    cur = curse.execute('''SELECT COUNT(posts.postid)
                        as num_posts FROM posts
                        WHERE posts.owner = ?''',
                        (username, ))
    postcount = cur.fetchall()
    # print(postcount)

    # followers
    cur = curse.execute('''SELECT COUNT(following.username1)
                       as num_followers FROM following WHERE
                       following.username2 = ?''', (username, ))
    followers = cur.fetchall()
    print(followers)

    # following
    cur = curse.execute('''SELECT COUNT(following.username2)
                       as num_following FROM following WHERE
                       following.username1 = ?''', (username, ))
    following = cur.fetchall()
    # print(following)

    insta485.model.close_db(curse)
    context = {"logname": loguser, "username": username,
               "total_posts": postcount, "followers": followers,
               "following": following, "posts": postuser,
               "relation": relation, "name": name}
    return flask.render_template("users.html", **context)


@insta485.app.route('/users/<username>/followers/')
def show_user_follower(username):
    """Display /users/<username>/followers route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))
    curse = insta485.model.get_db()

    cur = curse.execute('''SELECT following.username1
                        FROM following WHERE
                        following.username2 = ?''', (username, ))
    followers = cur.fetchall()
    print(followers)

    user_data = {}
    relations = {}
    for follow in followers:
        cur = curse.execute('''SELECT users.filename,
                            users.username FROM users
                            WHERE users.username = ?''',
                            (follow['username1'], ))
        user_data[follow['username1']] = cur.fetchall()
        relations[follow['username1']] = 2
        if follow['username1'] == username:
            relations[follow['username1']] = 0
        else:
            cur = curse.execute('''SELECT following.username2
                                from following WHERE
                                following.username1 = ?''',
                                (username, ))
            following = cur.fetchall()
            for row in following:
                if follow['username1'] == row['username2']:
                    relations[follow['username1']] = 1

    context = {"logname": username, "followers": followers,
               "relations": relations, "user_data": user_data}
    return flask.render_template("followers.html", **context)


@insta485.app.route('/users/<username>/following/')
def show_user_following(username):
    """Display /users/<username>/following/ route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))
    curse = insta485.model.get_db()

    cur = curse.execute('''SELECT following.username2
                        FROM following WHERE
                        following.username1 = ?''',
                        (username, ))
    following = cur.fetchall()

    user_data = {}
    for follow in following:
        cur = curse.execute('''SELECT users.filename,
                            users.username FROM users
                            WHERE users.username = ?''',
                            (follow['username2'], ))
        user_data[follow['username2']] = cur.fetchall()

    print(following)
    print(user_data)

    context = {"logname": username, "following": following,
               "user_data": user_data}
    return flask.render_template("following.html", **context)
