from django.contrib import admin
from .models import Actor, Director, Producer, Movie, ManyMovieHasManyActor, Genre, ManyMovieHasManyGenre, ManyMovieHasManyProducer

admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(Producer)
admin.site.register(Movie)
admin.site.register(ManyMovieHasManyActor)
admin.site.register(ManyMovieHasManyGenre)
admin.site.register(ManyMovieHasManyProducer)
admin.site.register(Genre)