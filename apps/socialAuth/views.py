from django.conf import settings

from rest_framework import serializers
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


from requests.exceptions import HTTPError
from django.shortcuts import redirect
from social_django.utils import psa

from apiclient import discovery
import httplib2
import google.oauth2.credentials
import google_auth_oauthlib.flow

from oauth2client import client
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from .models import CredentialsModel

import requests
import os
import json

from rest_framework import authentication
from django.contrib.auth.models import User
from rest_framework import exceptions
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
import os

from apps.users.serializers import UserSerializer

json = os.path.join(settings.KEYFILES_DIR, settings.FIREBASE_KEY)
cred = credentials.Certificate(json)
default_app = firebase_admin.initialize_app(cred)

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

@api_view(['POST'])
@permission_classes([AllowAny])
def exchange_auth_code(request):
        # if not request.headers.get('X-Requested-With'):
        #     abort(403)

        auth_code = request.data['code']

        # Set path to the Web application client_secret_*.json file you downloaded from the
        # Google API Console: https://console.developers.google.com/apis/credentials

        CLIENT_SECRET_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "client_secret.json")

        # Exchange auth code for access token, refresh token, and ID token
        credentials = client.credentials_from_clientsecrets_and_code(
            CLIENT_SECRET_FILE,
            ['https://www.googleapis.com/auth/drive.appdata', 'profile', 'email'],
            auth_code)

        access_token = credentials.token_response['access_token']
        # Call Google API
        # http_auth = credentials.authorize(httplib2.Http())
        # drive_service = discovery.build('drive', 'v3', http=http_auth)
        # appfolder = drive_service.files().get(fileId='appfolder').execute()

        # Get profile info from ID token
        # userid = credentials.id_token['sub']
        # email = credentials.id_token['email']
        # if not request.session.get('credentials'):
        #      request.session['credentials'] = credentials.to_json()
        # else:
        #     print(request.session['credentials'])
        # request.session.modified = True/
        # request.session['']
        # response = redirect('exchange_token', backend='google-oauth2')
        # credentials = json.dumps(credentials)
        # r = requests.post('http://localhost:8000/auth/social/exchange_token/google-oauth2/', data={'access_token': access_token, 'credentials': credentials})
        return Response( {'access_token': access_token, 'credentials': credentials.to_json()},status=status.HTTP_200_OK)
        # return r

def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}



class SocialSerializer(serializers.Serializer):
    """
    Serializer which accepts an OAuth2 access token.
    """
    access_token = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
    )



@api_view(['POST'])
@permission_classes([AllowAny])
@psa()
def exchange_token(request, backend):
    """
    Exchange an OAuth2 access token for one for this site.
    This simply defers the entire OAuth2 process to the front end.
    The front end becomes responsible for handling the entirety of the
    OAuth2 process; we just step in at the end and use the access token
    to populate some user identity.
    The URL at which this view lives must include a backend field, like:
        url(API_ROOT + r'social/(?P<backend>[^/]+)/$', exchange_token),
    Using that example, you could call this endpoint using i.e.
        POST API_ROOT + 'social/facebook/'
        POST API_ROOT + 'social/google-oauth2/'
    Note that those endpoint examples are verbatim according to the
    PSA backends which we configured in settings.py. If you wish to enable
    other social authentication backends, they'll get their own endpoints
    automatically according to PSA.
    ## Request format
    Requests must include the following field
    - `access_token`: The OAuth2 access token provided by the provider
    """
    # credentials = request.data['id_token']
    data = {
        'access_token':request.data['access_token']
    }

    serializer = SocialSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        # set up non-field errors key
        # http://www.django-rest-framework.org/api-guide/exceptions/#exception-handling-in-rest-framework-views
        try:
            nfe = settings.NON_FIELD_ERRORS_KEY
        except AttributeError:
            nfe = 'non_field_errors'

        try:
            # this line, plus the psa decorator above, are all that's necessary to
            # get and populate a user object for any properly enabled/configured backend
            # which python-social-auth can handle.
            user = request.backend.do_auth(serializer.validated_data['access_token'])
        except HTTPError as e:
            # An HTTPError bubbled up from the request to the social auth provider.
            # This happens, at least in Google's case, every time you send a malformed
            # or incorrect access key.
            return Response(
                {'errors': {
                    'token': 'Invalid token',
                    'detail': str(e),
                }},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user:
            if user.is_active:
                # storage = DjangoORMStorage(CredentialsModel, 'id', user, 'credential')
                # if not storage.get():
                #     storage.put(credentials)
                token, _ = Token.objects.get_or_create(user=user)
                

                return Response({'token': token.key, 'user_id': user.id}, status=status.HTTP_200_OK)
            else:
                # user is not active; at some point they deleted their account,
                # or were banned by a superuser. They can't just log in with their
                # normal credentials anymore, so they can't log in with social
                # credentials either.
                return Response(
                    {'errors': {nfe: 'This user account is inactive'}},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            # Unfortunately, PSA swallows any information the backend provider
            # generated as to why specifically the authentication failed;
            # this makes it tough to debug except by examining the server logs.
            return Response(
                {'errors': {nfe: "Authentication Failed"}},
                status=status.HTTP_400_BAD_REQUEST,
            )


@api_view(['POST'])
@permission_classes([AllowAny])
def authenticate(request):
        data = request.data
        id_token = data['access_token']
        decoded_token = None
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception as e:
            pass

        if not id_token or not decoded_token:
            return None

        uid = decoded_token.get('uid')
        try:
            user = User.objects.get(username=uid)
        except User.DoesNotExist:
            user = User(username=uid)
            try:
                name = data['fullName'].split()    
                user.first_name = name[0]
                user.last_name = name[1]
            except Exception as e:
                user.first_name = data['fullName']
            user.email = data['email']
            # user.avatar_url = data['avatar']  
            user.mobile_number = ''  
            user.save()
            
        token, _ = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)    
        return Response( {'token': token.key, 'user': user_serializer.data},status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_phone_number(request):
    data = request.data
    username = data['username']
    user = User.objects.get(username = username)

    mobile_number = user.mobile_number

    if mobile_number and len(mobile_number) != 0:
        return Response( {'phone_number': mobile_number},status=status.HTTP_200_OK)
    else:
        return Response( {'phone_number': ''},status=status.HTTP_200_OK)
    

    


    