from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Home path.
    path('', views.index, name="index"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('profile', views.profile, name="profile"),
    path('editProfile', views.editProfile, name="editProfile"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),


    # Actor paths.
    path('actors', views.actors, name="actors"),
    path('singleActorSearchResult', views.singleActorSearchResult, name="singleActorSearchResult"),
    path('allActorsJson', views.allActorsJson, name="allActorsJson"),
    path('searchedActors', views.searchedActors, name="searchedActors"),
    path('actor/<str:actor_id>/', views.actor, name="actor"),
    path('createActor', views.createActor, name="createActor"),
    path('update_actor/<str:actor_id>/', views.updateActor, name="update_actor"),
    path('delete_actor/<str:actor_id>/', views.deleteActor, name="delete_actor"),

    # Director paths.
    path('directors', views.directors, name="directors"),
    path('singleDirectorSearchResult', views.singleDirectorSearchResult, name="singleDirectorSearchResult"),
    path('allDirectorsJson', views.allDirectorsJson, name="allDirectorsJson"),
    path('searchedDirectors', views.searchedDirectors, name="searchedDirectors"),
    path('director/<str:director_id>/', views.director, name="director"),
    path('createDirector', views.createDirector, name="createDirector"),
    path('update_director/<str:director_id>/', views.updateDirector, name="update_director"),
    path('delete_director/<str:director_id>/', views.deleteDirector, name="delete_director"),

    # Producer paths.
    path('producers', views.producers, name="producers"),
    path('singleProducerSearchResult', views.singleProducerSearchResult, name="singleProducerSearchResult"),
    path('allProducersJson', views.allProducersJson, name="allProducersJson"),
    path('searchedProducers', views.searchedProducers, name="searchedProducers"),
    path('producer/<str:producer_id>/', views.producer, name="producer"),
    path('createProducer', views.createProducer, name="createProducer"),
    path('update_producer/<str:producer_id>/', views.updateProducer, name="update_producer"),
    path('delete_producer/<str:producer_id>/', views.deleteProducer, name="delete_producer"),

    # Movie paths.
    path('movies', views.movies, name="movies"),
    path('singleMovieSearchResult', views.singleMovieSearchResult, name="singleMovieSearchResult"),
    path('allMoviesJson', views.allMoviesJson, name="allMoviesJson"),
    path('searchedMovies', views.searchedMovies, name="searchedMovies"),
    path('movie/<str:movie_id>/', views.movie, name="movie"),
    path('createMovie', views.createMovie, name="createMovie"),
    path('update_movie/<str:movie_id>/', views.updateMovie, name="update_movie"),
    path('delete_movie/<str:movie_id>/', views.deleteMovie, name="delete_movie"),
    path('rateMovie/<str:movie_id>/<str:star_value>/', views.rateMovie, name="rateMovie"),
    path('ratedMovies', views.ratedMovies, name="ratedMovies"),
    path('favoriteMovie/<str:movie_id>/', views.favoriteMovie, name="favoriteMovie"),
    path('unfavoriteMovie/<str:movie_id>/', views.unfavoriteMovie, name="unfavoriteMovie"),
    path('favoritedMovies', views.favoritedMovies, name="favoritedMovies"),

    # Genre paths.
    path('createGenre', views.createGenre, name="createGenre"),

    path('createComment/<str:movie_id>/', views.createComment, name="createComment"),
    path('createReply/<str:comment_id>/', views.createReply, name="createReply"),

]

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)