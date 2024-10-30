"""REST API for comments."""
import json
import flask
import insta485


@insta485.app.route('/api/v1/comments/', methods=['POST'])
def get_comment():
    """Add the comment with the lastest postid."""
    # checking if the comment is from the user that posted it
    commentt = flask.request.data.decode('utf-8')
    data = json.loads(commentt)
    comment_text = data['text']
    print(comment_text)
    postid = flask.request.args['postid']
    insta485.model.post_exists(postid)
    print(commentt)
    user = insta485.model.authentication()
    commenti = insta485.model.insert_comment_from_data(postid,
                                                       user, comment_text)
    print(commenti)
    ownerc = True
    com = str(commenti[0]["last_insert_rowid()"])
    context = {
            "commentid": commenti[0]["last_insert_rowid()"],
            "lognameOwnsThis": ownerc,
            "owner": user,
            "ownerShowUrl": "/users/" + user + "/",
            "text": comment_text,
            "url": "/api/v1/comments/" + com + "/",
    }
    print(context)
    return flask.jsonify(**context), 201


@insta485.app.route('/api/v1/comments/<int:commentid>/', methods=['DELETE'])
def delete_comment(commentid):
    """Delete comment."""
    user = insta485.model.authentication()
    check = insta485.model.check_comment(commentid)
    print(check)
    # check if comment does not exist, return 404
    if len(check) == 0:
        raise insta485.model.InvalidUsage("Does Not Exist", status_code=404)
    # check if user doesn't own the comment, return 403
    if check[0]['owner'] != user:
        raise insta485.model.InvalidUsage("User Does Not Own Comment",
                                          status_code=403)
    # delete comment, return 204
    insta485.model.delete_comment(commentid)
    context = {}
    return flask.jsonify(**context), 204
