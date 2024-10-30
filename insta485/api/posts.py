"""REST API for posts."""
import flask
import insta485


@insta485.app.route('/api/v1/posts/', methods=['GET'])
def get_post():
    """Return ten newest posts."""
    print(flask.request.full_path)
    user = insta485.model.authentication()
    # print(flask.request.full_path.rstrip("?"))
    size = flask.request.args.get("size", default=10, type=int)
    lte = flask.request.args.get("postid_lte", default=0, type=int)
    page = flask.request.args.get("page", default=0, type=int)
    if size < 0:
        raise insta485.model.InvalidUsage("Bad Request", status_code=400)
    if page < 0:
        raise insta485.model.InvalidUsage("Bad Request", status_code=400)
    print("size", size)
    print("lte", lte)
    print("page", page)
    if lte == 0:
        print(insta485.model.get_all_posts(user, size, page, lte))
        lte = (insta485.model.get_all_posts(user,
               size, page, lte))[0]['postid']
    # print("lte", lte)
    posts = insta485.model.get_all_posts(user, size, page, lte)

    for row in posts:
        row['url'] = "/api/v1/posts/" + str(row['postid']) + "/"
    print("posts", posts)
    print(len(posts))
    if len(posts) == size:
        nextinline = "/api/v1/posts/?size=" + str(size)
        nextinline += "&page=" + str(page + 1)
        if lte:
            nextinline += "&postid_lte=" + str(lte)
    else:
        nextinline = ""
    print("nextinline", nextinline)
    context = {
        "next": nextinline,
        "results": posts,
        "url": flask.request.full_path.rstrip("?")
    }
    print("context", context)
    return flask.jsonify(**context)


@insta485.app.route('/api/v1/posts/<int:postid_url_slug>/', methods=['GET'])
def get_post_info(postid_url_slug):
    """Get post info."""
    user = insta485.model.authentication()
    postid = postid_url_slug
    insta485.model.post_exists(postid)
    comments = insta485.model.get_comments_for_post(postid)
    for row in comments:
        if row['owner'] == user:
            row['lognameOwnsThis'] = True
        else:
            row['lognameOwnsThis'] = False
        row['ownerShowUrl'] = "/users/" + row['owner'] + "/"
        row['url'] = "/api/v1/comments/" + str(row['commentid']) + "/"

    postinfo = insta485.model.get_post_info(postid)
    profpic = insta485.model.get_owner_url(postinfo[0]['owner'])
    numlikes = insta485.model.get_like_count(postid)
    likeinfo = insta485.model.get_like_owner(postid, user)
    if len(likeinfo):
        isowner = True
        urlowner = "/api/v1/likes/" + str(likeinfo[0]['likeid']) + "/"
    else:
        isowner = False
        urlowner = None
    context = {
        "comments": comments,
        "comments_url": "/api/v1/comments/?postid=" + str(postid),
        "created": postinfo[0]['created'],
        "imgUrl": "/uploads/" + postinfo[0]['filename'],
        "likes": {
            "lognameLikesThis": isowner,
            "numLikes": numlikes,
            "url": urlowner
        },
        "owner": postinfo[0]['owner'],
        "ownerImgUrl": "/uploads/" + profpic[0]['filename'],
        "ownerShowUrl": "/users/" + postinfo[0]['owner'] + "/",
        "postShowUrl": "/posts/" + str(postid) + "/",
        "postid": postid,
        "url": "/api/v1/posts/" + str(postid) + "/"
    }
    return flask.jsonify(**context)


@insta485.app.route('/api/v1/')
def get_services():
    """Return a list of services."""
    context = {
      "comments": "/api/v1/comments/",
      "likes": "/api/v1/likes/",
      "posts": "/api/v1/posts/",
      "url": "/api/v1/"
    }
    return flask.jsonify(**context), 200
