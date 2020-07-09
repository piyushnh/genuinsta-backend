from stream_framework.verbs import register
from stream_framework.verbs.base import Verb


class Post(Verb):
    id = 5
    infinitive = 'post'
    past_tense = 'posted'

register(Post)