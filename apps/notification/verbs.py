from stream_framework.verbs import register
from stream_framework.verbs.base import Verb


class NotificationVerb(Verb):
    id = 6
    infinitive = 'notify'
    past_tense = 'notified'

register(NotificationVerb)