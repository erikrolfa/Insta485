"""Insta485 model (database) API."""
import hashlib
import sqlite3
import flask
import insta485


class InvalidUsage(Exception):
    """Class respresenting invalid usage."""

    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        """Initialize error."""
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """Format error message."""
        rve = dict(self.payload or ())
        rve['message'] = self.message
        rve['status code'] = self.status_code
        return rve


@insta485.app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    """Handle invalid usage."""
    response = flask.jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def authentication():
    """Authenticate user and password."""
    print(flask.request.full_path)
    if 'username' in flask.session:
        print(1)
        username = flask.session['username']
        return username
    if flask.request.authorization:
        print(2)
        username = flask.request.authorization['username']
        password = flask.request.authorization['password']
        curse = get_db()
        cur = curse.execute("SELECT * FROM users WHERE users.username = ?",
                            (username, ))
        pup = cur.fetchall()
        if len(pup) == 0:
            raise InvalidUsage("Forbidden", status_code=403)
        userpasswor = {}
        cur = curse.execute('''SELECT users.password
                            FROM users WHERE users.username = ?''',
                            (username, ))
        userpasswor = cur.fetchall()
        hashed_pass_full = userpasswor[0]['password']
        hashed_pass = hashed_pass_full.split("$")

        algorith = 'sha512'
        salt = hashed_pass[1]
        hash_obj = hashlib.new(algorith)
        passwor_salted = salt + password
        hash_obj.update(passwor_salted.encode('utf-8'))
        passwor_hash = hash_obj.hexdigest()
        password_db_string2 = "$".join([algorith,
                                        salt, passwor_hash])

        if hashed_pass_full != password_db_string2:
            raise InvalidUsage("Forbidden", status_code=403)

        close_db(curse)
        return username
    print(9)
    raise InvalidUsage("Forbidden", status_code=403)


def dict_factory(cursor, row):
    """Convert database row objects to a dictionary keyed on column name.

    This is useful for building dictionaries which are then used to render a
    template.  Note that this would be inefficient for large queries.
    """
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def get_db():
    """Open a new database connection.

    Flask docs:
    https://flask.palletsprojects.com/en/1.0.x/appcontext/#storing-data
    """
    if 'sqlite_db' not in flask.g:
        db_filename = insta485.app.config['DATABASE_FILENAME']
        flask.g.sqlite_db = sqlite3.connect(str(db_filename))
        flask.g.sqlite_db.row_factory = dict_factory

        # Foreign keys have to be enabled per-connection.  This is an sqlite3
        # backwards compatibility thing.
        flask.g.sqlite_db.execute("PRAGMA foreign_keys = ON")

    return flask.g.sqlite_db


@insta485.app.teardown_appcontext
def close_db(error):
    """Close the database at the end of a request.

    Flask docs:
    https://flask.palletsprojects.com/en/1.0.x/appcontext/#storing-data
    """
    assert error or not error  # Needed to avoid superfluous style error
    sqlite_db = flask.g.pop('sqlite_db', None)
    if sqlite_db is not None:
        sqlite_db.commit()
        sqlite_db.close()


def get_all_posts(user, size, page, lte):
    """Return the ten newest posts."""
    curse = get_db()
    cur = curse.execute('''SELECT
                        posts.postid FROM
                        posts JOIN users
                        ON posts.owner =
                        users.username
                        JOIN following
                        ON users.username
                        = following.username2
                        WHERE
                        following.username1 = ? OR
                        posts.owner = ? GROUP BY
                        posts.postid ORDER BY
                        posts.postid DESC''',
                        (user, user, ))
    latest = cur.fetchall()
    print("bugs", latest)
    if lte == 0:
        lte = latest[0]['postid']
    offset_num = (size * page) + (latest[0]['postid'] - lte)
    cur = curse.execute('''SELECT
                        posts.postid FROM
                        posts JOIN users
                        ON posts.owner =
                        users.username
                        JOIN following ON
                        users.username
                        = following.username2
                        WHERE
                        following.username1 = ? OR
                        posts.owner = ? GROUP BY
                        posts.postid ORDER BY
                        posts.postid DESC LIMIT ? OFFSET ?''',
                        (user, user, size, offset_num, ))
    resp = cur.fetchall()
    close_db(curse)
    return resp


def get_comments_for_post(postid):
    """Get comments info."""
    curse = get_db()
    cur = curse.execute('''SELECT
                        comments.commentid, comments.owner,
                        comments.text FROM comments WHERE
                        comments.postid = ?''',
                        (postid, ))
    resp = cur.fetchall()
    close_db(curse)
    return resp


def get_post_info(postid):
    """Get post info."""
    curse = get_db()
    cur = curse.execute('''SELECT
                        posts.created, posts.filename, posts.owner
                        FROM posts WHERE posts.postid = ?''',
                        (postid, ))
    resp = cur.fetchall()
    close_db(curse)
    return resp


def get_owner_url(owner):
    """Get owner url info."""
    curse = get_db()
    cur = curse.execute('''SELECT
                        users.filename FROM users WHERE
                        users.username = ?''',
                        (owner, ))
    resp = cur.fetchall()
    close_db(curse)
    return resp


def get_like_count(postid):
    """Get like count."""
    curse = get_db()
    cur = curse.execute('''SELECT
                        * FROM likes WHERE likes.postid
                        = ?''', (postid, ))
    resp = cur.fetchall()
    close_db(curse)
    return len(resp)


def get_like_owner(postid, logname):
    """See if liked post."""
    curse = get_db()
    cur = curse.execute('''SELECT likes.owner, likes.likeid
                        FROM likes WHERE likes.postid = ?
                        AND likes.owner = ?''', (postid, logname))
    resp = cur.fetchall()
    close_db(curse)
    return resp


def insert_comment_from_data(postid, user, text):
    """Add one comment to post."""
    curse = get_db()
    cur = curse.execute('''INSERT INTO comments (owner,
                            postid, text) VALUES (?, ?, ?)
                            ''', (user, postid, text, ))

    cur = curse.execute('''SELECT last_insert_rowid() FROM comments
                        WHERE comments.postid = ?
                        AND comments.owner = ?''', (postid, user, ))
    resp = cur.fetchall()
    close_db(curse)
    return resp


def is_user(user, postid):
    """Check if is user."""
    curse = get_db()
    cur = curse.execute('''SELECT comments.owner FROM comments WHERE
                        comments.postid = ? ''', (postid, ))
    resp = cur.fetchall()
    close_db(curse)
    if resp == user:
        return True
    return False


def get_postid(postid):
    """Fetch postid."""
    curse = get_db()
    cur = curse.execute('''SELECT posts.postid FROM posts
                        WHERE posts.postid = ?''', (postid, ))
    resp = cur.fetchall()
    close_db(curse)
    return resp


def get_like(user, postid):
    """Check if like exists."""
    curse = get_db()
    cur = curse.execute('''SELECT * FROM likes
                        WHERE likes.owner = ? AND
                        likes.postid = ?''', (user, postid, ))
    resp = cur.fetchall()
    close_db(curse)
    return resp


def create_like(user, postid):
    """Create a like in postid for a user."""
    curse = get_db()
    cur = curse.execute('''INSERT INTO likes (owner, postid)
                        VALUES (?, ?)''', (user, postid, ))
    cur = curse.execute('''SELECT likes.likeid FROM likes
                        WHERE likes.owner = ? AND
                        likes.postid = ?''', (user, postid, ))
    resp = cur.fetchall()
    close_db(curse)
    return resp


def delete_like(likeid):
    """Delete like."""
    curse = get_db()
    cur = curse.execute('''DELETE FROM likes WHERE
                        likes.likeid = ?''',
                        (likeid, ))
    resp = cur.fetchall()
    close_db(curse)
    return resp


def check_like(likeid):
    """Check if likeid exists."""
    curse = get_db()
    cur = curse.execute('''SELECT likes.likeid, likes.owner FROM likes
                        WHERE likes.likeid = ?''', (likeid, ))
    resp = cur.fetchall()
    close_db(curse)
    return resp


def post_exists(postid):
    """Check if post exists."""
    curse = get_db()
    cur = curse.execute('''SELECT * FROM posts
                        WHERE posts.postid = ?''',
                        (postid, ))
    resp = cur.fetchall()
    close_db(curse)
    if len(resp) == 0:
        raise InvalidUsage("Not Found", status_code=404)
    return 0


def check_comment(commentid):
    """Check if comment exists."""
    curse = get_db()
    cur = curse.execute('''SELECT * FROM comments
                        WHERE comments.commentid = ?''',
                        (commentid, ))
    resp = cur.fetchall()
    close_db(curse)
    return resp


def delete_comment(commentid):
    """Delete comment."""
    curse = get_db()
    cur = curse.execute('''DELETE FROM comments WHERE
                        comments.commentid = ?''',
                        (commentid, ))
    resp = cur.fetchall()
    close_db(curse)
    return resp
