from django.apps import AppConfig


class FriendshipConfig(AppConfig):
    name = 'apps.friendship'

    def ready(self):
    #   import apps.friendship.signals
        pass
