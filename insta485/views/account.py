"""
Insta485 logout view.

URLs include:
/accounts/logout/
"""
import flask
import insta485


@insta485.app.route('/accounts/logout/', methods=['POST'])
def account_logout():
    """Display /accounts/logout/ route."""
    flask.session.clear()
    return flask.redirect(flask.url_for('show_login'))


@insta485.app.route('/accounts/create/')
def account_create():
    """Display /accounts/create/ route."""
    if 'username' not in flask.session:
        context = {}
        return flask.render_template("create.html", **context)
    return flask.redirect(flask.url_for('account_edit'))


@insta485.app.route('/accounts/edit/')
def account_edit():
    """Display /accounts/edit/ route."""
    logname = flask.session['username']

    curse = insta485.model.get_db()

    cur = curse.execute('''SELECT users.filename,
                        users.fullname, users.email
                        FROM users WHERE
                        users.username = ?''',
                        (logname, ))
    user_content = cur.fetchall()
    insta485.model.close_db(curse)

    context = {"logname": logname, "user_content": user_content}
    return flask.render_template("edit.html", **context)


@insta485.app.route('/accounts/delete/')
def account_delete():
    """Display /accounts/delete/ route."""
    user = flask.session['username']
    context = {"logname": user}
    return flask.render_template("delete.html", **context)


@insta485.app.route('/accounts/password/')
def account_password():
    """Display /accounts/password/ route."""
    logname = flask.session['username']

    context = {"logname": logname}
    return flask.render_template("password.html", **context)
