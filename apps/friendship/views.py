from django.contrib.auth.decorators import login_required
from django.conf import settings
try:
    from django.contrib.auth import get_user_model
    user_model = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
    user_model = User

from django.shortcuts import render, get_object_or_404, redirect

#rest_framework imports
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .exceptions import AlreadyExistsError
from .models import Friend, Follow, FriendshipRequest
from .serializers import (FriendshipRequestSerializer, FriendSerializer,
                            FollowSerializer, UserSerializer)

get_friendship_context_object_name = lambda: getattr(settings, 'FRIENDSHIP_CONTEXT_OBJECT_NAME', 'user')
get_friendship_context_object_list_name = lambda: getattr(settings, 'FRIENDSHIP_CONTEXT_OBJECT_LIST_NAME', 'users')

@login_required
@api_view(['GET'])
def view_friends(request, username):
    """ View the friends of a user """
    user = get_object_or_404(user_model, username=username)
    friends = Friend.objects.friends(user)
    serializer = FriendSerializer(friends, many = True)
    return Response(serializer.data)


@login_required
@api_view(['POST'])
def friendship_add_friend(request, to_username, template_name='friendship/friend/add.html'):
    """ Create a FriendshipRequest """
    ctx = {'to_username': to_username}

    if request.method == 'POST':
        to_user = user_model.objects.get(username=to_username)
        from_user = request.user
        try:
            Friend.objects.add_friend(from_user, to_user)
        except AlreadyExistsError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_201_CREATED)


@login_required
@api_view(['POST'])
def friendship_accept(request, friendship_request_id):
    """ Accept a friendship request """
    if request.method == 'POST':
        f_request = get_object_or_404(
            request.user.friendship_requests_received,
            id=friendship_request_id)
        f_request.accept()
        # return redirect('friendship:friendship_view_friends', username=request.user.username)

    return Response(status=status.HTTP_202_ACCEPTED)



@login_required
@api_view(['POST'])
def friendship_reject(request, friendship_request_id):
    """ Reject a friendship request """
    if request.method == 'POST':
        f_request = get_object_or_404(
            request.user.friendship_requests_received,
            id=friendship_request_id)
        f_request.reject()
        # return redirect('friendship:friendship_request_list')

    # return redirect('friendship:friendship_requests_detail', friendship_request_id=friendship_request_id)
    return Response(status=status.HTTP_200_OK)


@login_required
@api_view(['POST'])
def friendship_cancel(request, friendship_request_id):
    """ Cancel a previously created friendship_request_id """
    if request.method == 'POST':
        f_request = get_object_or_404(
            request.user.friendship_requests_sent,
            id=friendship_request_id)
        f_request.cancel()


    return Response(status=status.HTTP_200_OK)


@login_required
@api_view(['GET'])
def friendship_request_list(request):
    """ View unread and read friendship requests """
    # friendship_requests = Friend.objects.requests(request.user)
    friendship_requests = FriendshipRequest.objects.filter(rejected__isnull=True,to_user=request.user)
    serializer = FriendshipRequestSerializer(friendship_requests, many=True)

    return Response(serializer.data)

@login_required
@api_view(['GET'])
def friendship_requests_sent_list(request):
    """ View unread and read friendship requests """
    # friendship_requests = Friend.objects.requests(request.user)
    friendship_requests = FriendshipRequest.objects.filter(from_user=request.user)
    serializer = FriendshipRequestSerializer(friendship_requests, many=True)

    return Response(serializer.data)


@login_required
def friendship_request_list_rejected(request, template_name='friendship/friend/requests_list.html'):
    """ View rejected friendship requests """
    friendship_requests = Friend.objects.rejected_requests(request.user)
    # friendship_requests = FriendshipRequest.objects.filter(rejected__isnull=True)

    return render(request, template_name, {'requests': friendship_requests})


@login_required
@api_view(['GET'])
def friendship_requests_detail(request, friendship_request_id, template_name='friendship/friend/request.html'):
    """ View a particular friendship request """
    f_request = get_object_or_404(FriendshipRequest, id=friendship_request_id)
    serializer = FriendshipRequestSerializer(f_request)


    return Response(serializer.data)

@login_required
def remove_friend(request, friend_username):
    """ Remove a particular person as friend """
    friend = user_model.objects.get(username = friend_username)
    user = request.user
    successful = Friend.objects.remove_friend(friend, user)
    if successful:
        return redirect("userprofiles:public_profile", kwargs={'pk':friend.pk})

def followers(request, username, template_name='friendship/follow/followers_list.html'):
    """ List this user's followers """
    user = get_object_or_404(user_model, username=username)
    followers = Follow.objects.followers(user)

    return render(request, template_name, {
        get_friendship_context_object_name(): user,
        'friendship_context_object_name': get_friendship_context_object_name()
    })


def following(request, username, template_name='friendship/follow/following_list.html'):
    """ List who this user follows """
    user = get_object_or_404(user_model, username=username)
    following = Follow.objects.following(user)

    return render(request, template_name, {
        get_friendship_context_object_name(): user,
        'friendship_context_object_name': get_friendship_context_object_name()
    })


@login_required
def follower_add(request, followee_username, template_name='friendship/follow/add.html'):
    """ Create a following relationship """
    ctx = {'followee_username': followee_username}

    if request.method == 'POST':
        followee = user_model.objects.get(username=followee_username)
        follower = request.user
        try:
            Follow.objects.add_follower(follower, followee)
        except AlreadyExistsError as e:
            ctx['errors'] = ["%s" % e]
        else:
            return redirect('friendship:friendship_following', username=follower.username)

    return render(request, template_name, ctx)


@login_required
def follower_remove(request, followee_username, template_name='friendship/follow/remove.html'):
    """ Remove a following relationship """
    if request.method == 'POST':
        followee = user_model.objects.get(username=followee_username)
        follower = request.user
        Follow.objects.remove_follower(follower, followee)
        return redirect('friendship:friendship_following', username=follower.username)

    return render(request, template_name, {'followee_username': followee_username})


@api_view(['GET'])
def all_users(request):
    users = user_model.objects.all()
    serializer = UserSerializer(users, many=True)

    # print(serializer)
    return Response(serializer.data)
