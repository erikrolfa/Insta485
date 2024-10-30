"""
Insta485 index (main) view.

URLs include:
/
"""
import flask
import arrow
import insta485


@insta485.app.route('/')
def show_index():
    """Display / route."""
    print(101)
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))
    user = flask.session['username']
    print(user)

    curse = insta485.model.get_db()

    cur = curse.execute('''SELECT posts.filename,
                        posts.postid, posts.created,
                        posts.owner as postowner, users.filename
                        as profpic FROM posts JOIN users
                        ON posts.owner = users.username
                        JOIN following ON users.username
                        = following.username2 WHERE
                        following.username1 = ? OR
                        posts.owner = ? GROUP BY
                        posts.postid ORDER BY
                        posts.postid''', (user, user, ))
    post_list = cur.fetchall()

    comments = {}
    likes = {}
    likes_user = {}
    for post in post_list:
        post['created'] = (arrow.get(post['created'],
                                     'YYYY-MM-DD HH:mm:ss')).humanize()

        cur = curse.execute('''SELECT COUNT(*) as
                            likecount, likes.postid,
                            likes.owner FROM likes
                            WHERE likes.postid = ?''',
                            (post['postid'], ))
        likes[post['postid']] = cur.fetchall()

        cur = curse.execute('''SELECT comments.commentid,
                            comments.owner, comments.text,
                            comments.postid FROM comments
                            WHERE comments.postid = ?''',
                            (post['postid'], ))
        comments[post['postid']] = cur.fetchall()

        cur = curse.execute('''SELECT likes.owner FROM
                            likes WHERE likes.postid = ?''',
                            (post['postid'], ))
        likes_user = cur.fetchall()

        for lud in likes_user:
            if user == lud['owner']:
                lud['liked'] = True

    size = len(likes_user)
    insta485.model.close_db(curse)
    context = {"logname": user, "post_list": post_list,
               "likes": likes, "comments": comments,
               "likes_user": likes_user if likes_user else [], "size": size}
    return flask.render_template("index.html", **context)


@insta485.app.route('/uploads/<path:filename>')
def download_file(filename):
    """Download file."""
    return flask.send_from_directory(insta485.app.config['UPLOAD_FOLDER'],
                                     filename, as_attachment=True)


if __name__ == '__main__':
    insta485.app.run(debug=True, host='0.0.0.0', port=8000)
