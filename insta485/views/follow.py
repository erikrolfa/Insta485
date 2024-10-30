"""
Insta485 follow view.

URLs include:
/following/<target>/
"""
import flask
import insta485


@insta485.app.route('/following/', methods=['POST'])
def follow_update():
    """Update followers and following."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))
    user = flask.session['username']
    # print(user)
    curse = insta485.model.get_db()
    follw = flask.request.form["username"]
    print(follw)

    followcheck = flask.request.form.get('operation')
    print(followcheck)
    if followcheck == "follow":
        curse.execute('''INSERT or IGNORE INTO following(username1,
                      username2) VALUES(?, ?)''',
                      (user, follw, ))
    else:
        curse.execute('''DELETE FROM
                      following WHERE username2 = ?
                      AND username1 = ? ''',
                      (follw, user, ))

    insta485.model.close_db(curse)
    return flask.redirect(flask.request.args.get('target',
                                                 default='/'))
