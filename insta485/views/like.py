"""
Insta485 like view.

URLs include:
/likes/
"""
import flask
import insta485


@insta485.app.route('/likes/', methods=['POST'])
def like_update():
    """Create/delete a like."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))
    user = flask.session['username']
    opr = flask.request.form.get('operation')
    ptid = flask.request.form.get('postid')
    # print(op)
    # print(user)

    curse = insta485.model.get_db()

    if opr == "unlike":
        # check if they are unliking a post they have not liked
        cur = curse.execute('''SELECT likes.owner FROM
                            likes WHERE likes.postid = ? AND
                            likes.owner = ?''', (ptid, user, ))
        check = cur.fetchall()
        if len(check) == 0:
            flask.abort(409)

        cur = curse.execute('''DELETE FROM likes WHERE
                            likes.owner = ? AND likes.postid
                            = ?''', (user, ptid, ))
    else:
        # check if they are liking a post they already liked
        cur = curse.execute('''SELECT likes.owner FROM
                            likes WHERE likes.postid = ? AND
                            likes.owner = ?''', (ptid, user, ))
        check = cur.fetchall()
        if len(check) != 0:
            flask.abort(409)

        cur = curse.execute('''INSERT INTO likes
                            (owner, postid) VALUES(?, ?)''',
                            (user, ptid, ))

    insta485.model.close_db(curse)
    return flask.redirect(flask.request.args.get('target',
                                                 default='/'))
