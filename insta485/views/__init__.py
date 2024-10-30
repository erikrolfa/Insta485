"""Views, one for each Insta485 page."""

from insta485.views.index import show_index
from insta485.views.index import download_file
from insta485.views.users import show_user
from insta485.views.users import show_user_follower
from insta485.views.users import show_user_following
from insta485.views.posts import show_post
from insta485.views.explore import show_explore
from insta485.views.like import like_update
from insta485.views.account import account_logout
from insta485.views.account import account_create
from insta485.views.account import account_edit
from insta485.views.account import account_delete
from insta485.views.account import account_password
from insta485.views.accupdate import account_auth
from insta485.views.accupdate import account_update
from insta485.views.accupdate import operation_login
from insta485.views.comment import comment_update
from insta485.views.login import show_login
from insta485.views.posts import post_post
from insta485.views.follow import follow_update
