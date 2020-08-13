try:
    from django.conf.urls import url
except ImportError:
    from django.conf.urls.defaults import url
from django.urls import path
from .views import view_friends, friendship_add_friend, \
    friendship_reject, friendship_cancel, friendship_request_list, \
    friendship_request_list_rejected, friendship_requests_detail, followers,\
    following, follower_add, follower_remove, all_users, friendship_requests_sent_list, remove_friend,\
    friendship_request_cancel, friendship_request_accept, get_friends_list

app_name = 'friendship'

urlpatterns = [
    url(
        regex=r'^getFriendsList/$',
        view=get_friends_list,
        name='get_friends_list',
    ),
    url(
        regex=r'^users/$',
        view=all_users,
        name='friendship_view_users',
    ),
    url(
        regex=r'^friends/(?P<username>[\w-]+)/$',
        view=view_friends,
        name='friendship_view_friends',
    ),
    path(
        'friend/add/<to_username>/',
        view=friendship_add_friend,
        name='friendship_add_friend',
    ),
    path(
        'friend/accept/<from_username>/',
        view=friendship_request_accept,
        name='friendship_request_accept',
    ),
    path(
        'friend/reject/<friendship_request_id>/',
        view=friendship_reject,
        name='friendship_reject',
    ),
    path(
        'friend/cancel_request/<to_username>/',
        view=friendship_request_cancel,
        name='friendship_request_cancel',
    ),
    url(
        regex=r'^friend/requests/$',
        view=friendship_request_list,
        name='friendship_request_list',
    ),
    url(
        regex=r'^friend/sent_requests/$',
        view=friendship_requests_sent_list,
        name='friendship_requests_sent_list',
    ),
    url(
        regex=r'^friend/requests/rejected/$',
        view=friendship_request_list_rejected,
        name='friendship_requests_rejected',
    ),
    url(
        regex=r'^friend/request/(?P<friendship_request_id>\d+)/$',
        view=friendship_requests_detail,
        name='friendship_requests_detail',
    ),
    url(
        regex=r'^followers/(?P<username>[\w-]+)/$',
        view=followers,
        name='friendship_followers',
    ),
    url(
        regex=r'^following/(?P<username>[\w-]+)/$',
        view=following,
        name='friendship_following',
    ),
     path('follower/add/<username>/',
            view = follower_add,
             name="follower_add" ),
     path('follower/remove/<followee_username>/',
            view = follower_remove,
             name="follower_remove" ),
     path('friend/remove/<friend_username>/',
            view = remove_friend,
             name="remove_friend" ),
    
]
