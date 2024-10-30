"""
Insta485 explore view.

URLs include:
/explore/
"""
import flask
import insta485


@insta485.app.route('/explore/')
def show_explore():
    """Display /explore/ route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))
    logname = flask.session['username']
    curse = insta485.model.get_db()

    cur = curse.execute('''SELECT following.username2,
                        users.filename from following
                        JOIN users ON
                        following.username2 = users.username
                        WHERE following.username2
                        NOT IN (SELECT following.username2
                        FROM following WHERE
                        following.username1 = ?)
                        GROUP BY following.username2''',
                        (logname, ))
    ex = cur.fetchall()
    print(ex)

    insta485.model.close_db(curse)
    context = {"logname": logname, "not_following": ex}
    return flask.render_template("explore.html", **context)
