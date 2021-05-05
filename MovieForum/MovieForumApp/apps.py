from django.apps import AppConfig


class MovieforumappConfig(AppConfig):
    name = 'MovieForumApp'

    def ready(self):
        from MovieForumApp import signals
