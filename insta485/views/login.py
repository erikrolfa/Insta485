"""
Insta485 accounts view.

URLs include:
/accounts/login/
"""
import flask
import insta485


@insta485.app.route('/accounts/login/')
def show_login():
    """Display /accounts/login route."""
    if 'username' not in flask.session:
        return flask.render_template("login.html")
    return flask.redirect(flask.url_for('show_index'))
