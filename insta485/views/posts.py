"""
Insta485 posts view.

URLs include:
/posts/
"""
import pathlib
import uuid
import os
import flask
import arrow
import insta485


@insta485.app.route('/posts/<postid>/')
def show_post(postid):
    """Display /posts/<postid> route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))

    curse = insta485.model.get_db()
    username = flask.session['username']

    cur = curse.execute('''SELECT posts.filename,
                        posts.owner, posts.created,
                        posts.postid FROM posts WHERE
                        posts.postid = ?''', (postid, ))
    post_content = cur.fetchall()

    cur = curse.execute('''SELECT users.filename
                        FROM users WHERE
                        users.username = ?''',
                        (post_content[0]['owner'], ))
    post_owner = cur.fetchall()

    comments = {}
    likes = {}
    post_content[0]['created'] = (arrow.get(post_content[0]['created'],
                                            'YYYY-MM-DD HH:mm:ss')).humanize()

    cur = curse.execute('''SELECT COUNT(*) as likecount,
                        likes.postid FROM likes WHERE
                        likes.postid = ?''', (postid, ))
    likes = cur.fetchall()

    cur = curse.execute('''SELECT likes.owner
                        FROM likes WHERE
                        likes.postid = ?''',
                        (postid, ))
    likes_user = cur.fetchall()
    # print(likes_user)

    liked = False
    for lud in likes_user:
        if username == lud['owner']:
            liked = True

    cur = curse.execute('''SELECT comments.commentid,
                        comments.owner, comments.text,
                        comments.postid FROM comments
                        WHERE comments.postid = ?''',
                        (postid, ))
    comments = cur.fetchall()

    insta485.model.close_db(curse)
    print("POST CONTENT", post_content)
    context = {"post_content": post_content, "likes": likes,
               "comments": comments, "logname": username,
               "post_owner": post_owner, "postid": postid,
               "likes_user": likes_user, "liked": liked}
    return flask.render_template("posts.html", **context)


@insta485.app.route('/posts/', methods=['POST'])
def post_post():
    """Create/delete post."""
    opr = flask.request.form.get('operation')
    curse = insta485.model.get_db()

    if opr == "create":
        fileobj = flask.request.files['file']
        filename = fileobj.filename
        print(filename)
        postid_p = flask.request.form.get('postid')
        username_p = flask.session['username']

        if not fileobj:
            flask.abort(400)

        stim = uuid.uuid4().hex
        suffex = pathlib.Path(filename).suffix.lower()
        uuid_basename = f"{stim}{suffex}"

        path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
        fileobj.save(path)

        cur = curse.execute('''INSERT INTO posts
                            (postid, filename, owner)
                            VALUES (?, ?, ?)''',
                            (postid_p, filename, username_p, ))
        return flask.redirect(flask.request.args.get('target',
                                                     default='/users/'
                                                     + username_p + '/'))
    postid_p = flask.request.form.get('postid')
    username_p = flask.session['username']
    cur = curse.execute('''SELECT posts.owner
                        FROM posts WHERE posts.postid = ?''',
                        (postid_p, ))
    check = cur.fetchall()
    if check[0]['owner'] != username_p:
        flask.abort(403)

    cur = curse.execute('''SELECT posts.filename
                        FROM posts WHERE
                        posts.postid = ?''',
                        (postid_p, ))
    fileobj = cur.fetchall()
    file = fileobj[0]['filename']
    print(file)

    path = os.path.join(insta485.app.config["UPLOAD_FOLDER"],
                        file)
    os.remove(path)

    cur = curse.execute("DELETE FROM posts WHERE posts.postid = ?",
                        (postid_p, ))
    return flask.redirect(flask.request.args.get('target',
                                                 default='/users/'
                                                 + username_p + '/'))
