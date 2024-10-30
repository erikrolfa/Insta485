"""
Insta485 comment view.

URLs include:
/comments/
"""
import flask
import insta485


@insta485.app.route('/comments/', methods=['POST'])
def comment_update():
    """Update comments."""
    user = flask.session['username']
    opr = flask.request.form.get('operation')
    postid = flask.request.form.get('postid')
    commentid = flask.request.form.get('commentid')

    if opr == "create":
        text = flask.request.form.get('text')

        # check if text is empty
        if not text:
            flask.abort(400)

        curse = insta485.model.get_db()
        cur = curse.execute('''INSERT INTO
                            comments(owner, postid, text)
                            VALUES(?, ?, ?)''',
                            (user, postid, text, ))
    elif opr == "delete":
        curse = insta485.model.get_db()
        # check if user is trying to delete comment they do not own
        cur = curse.execute('''SELECT comments.owner
                            FROM comments WHERE
                            comments.commentid = ?''',
                            (commentid, ))
        comment_owner = cur.fetchall()
        # check if comment owner is logged in user
        if user != comment_owner[0]['owner']:
            flask.abort(403)
        cur = curse.execute('''DELETE FROM comments
                            WHERE comments.commentid = ?''',
                            (commentid, ))

    return flask.redirect(flask.request.args.get('target', default='/'))
