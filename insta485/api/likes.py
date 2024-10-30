"""REST API for likes."""
import flask
import insta485


@insta485.app.route('/api/v1/likes/', methods=['POST'])
def post_like():
    """Post like."""
    user = insta485.model.authentication()
    postid = flask.request.args.get("postid", type=int)
    # check if postid is out of range
    if len(insta485.model.get_postid(postid)) == 0:
        raise insta485.model.InvalidUsage("Out of Range", status_code=404)
    # check if like already exists, return 200
    likeid = insta485.model.get_like(user, postid)
    if len(likeid) == 1:
        context = {
            "likeid": likeid[0]['likeid'],
            "url": flask.request.path + str(likeid[0]['likeid']) + "/"
        }
        print("context", context)
        print("path", flask.request.path)
        return flask.jsonify(**context), 200
    # if not exists, create like and return 201
    print(201)
    likeid = insta485.model.create_like(user, postid)
    context = {
            "likeid": likeid[0]['likeid'],
            "url": flask.request.path + str(likeid[0]['likeid']) + "/"
    }
    print("context", context)
    return flask.jsonify(**context), 201


@insta485.app.route('/api/v1/likes/<int:likeid>/', methods=['DELETE'])
def delete_like(likeid):
    """Delete like."""
    user = insta485.model.authentication()
    # check if like exists, return 404
    like = insta485.model.check_like(likeid)
    print("like", like)
    if len(like) == 0:
        raise insta485.model.InvalidUsage("Does Not Exist", status_code=404)
    # check if user owns the like
    if like[0]['owner'] != user:
        raise insta485.model.InvalidUsage("User Does Not Own Like",
                                          status_code=403)
    # delete like
    insta485.model.delete_like(likeid)
    context = {}
    return flask.jsonify(**context), 204
