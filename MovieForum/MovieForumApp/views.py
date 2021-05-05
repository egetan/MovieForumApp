from django.core import serializers
from django.db.models import Avg
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *
from .forms import ActorForm, DirectorForm, ProducerForm, MovieForm, GenreForm, CreateUserForm, EditUserForm
from django.db import connection
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

import random

# Index function.
def index(request):
    return render(request, 'MovieForumApp/index.html')


def dashboard(request):
    return render(request, 'MovieForumApp/dashboard.html')


@login_required(login_url='dashboard')
def profile(request):
    return render(request, 'MovieForumApp/user_profile.html')


@login_required(login_url='dashboard')
def editProfile(request):
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            messages.add_message(request, messages.INFO,
                                 "Couldn't update your information. Please make sure all fields are correct.")
            return redirect('profile')


# Utility functions.
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                account = authenticate(username=username, password=password)
                login(request, account)
                return redirect('dashboard')

        context = {'form': form}
    return render(request, 'MovieForumApp/login-register/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, 'Username OR password is incorrect')
                return redirect('dashboard')

        context = {}
    return render(request, 'MovieForumApp/login-register/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('dashboard')


def get_actor_age(id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT age FROM actor WHERE actor_id = %s", [id])
        row = cursor.fetchone()
    return row[0]


def get_director_age(id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT age FROM director WHERE director_id = %s", [id])
        row = cursor.fetchone()
    return row[0]


def get_producer_age(id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT age FROM producer WHERE producer_id = %s", [id])
        row = cursor.fetchone()
    return row[0]


def get_revenue(id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT revenue FROM movie WHERE movie_id = %s", [id])
        row = cursor.fetchone()
    return row[0]


# Actor functions.
# <-------------------------------------------------------------> #
def actor(request, actor_id):
    actor = Actor.objects.get(actor_id=actor_id)
    movies_played = actor.movies.values()
    total_movies = len(movies_played)
    age = get_actor_age(actor_id)
    short_description = actor.description[0:100] + "..."
    return render(request, 'MovieForumApp/actor/actor.html',
                  {'actor': actor,
                   'age': age,
                   'movies': movies_played,
                   'short_description': short_description,
                   'total_movies': total_movies
                   })

def actors(request):
    context = {}
    actors = Actor.objects.all()
    countries = Country.objects.all()
    actor_count = len(actors)
    actors_and_short_descriptions = []
    for actor in actors:
        if actor.description:
            actors_and_short_descriptions.append((actor, actor.description[0:50] + "..."))
        else:
            actors_and_short_descriptions.append((actor, "This actor has no description provided."))
    context['actors_and_short_descriptions'] = actors_and_short_descriptions
    context['actor_count'] = actor_count
    if actors:
        context['featured_actor'] = actors[random.randint(0, len(actors) - 1)]
    context['countries'] = countries
    return render(request, 'MovieForumApp/actor/actors.html', context=context)

@login_required(login_url='dashboard')
def createActor(request):
    form = ActorForm()
    if request.method == 'POST':
        form = ActorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('actors')
    context = {'form': form, 'is_create': True}
    return render(request, 'MovieForumApp/actor/actor_form.html', context=context)

@login_required(login_url='dashboard')
def updateActor(request, actor_id):
    actor = Actor.objects.get(actor_id=actor_id)
    form = ActorForm(instance=actor)

    if request.method == 'POST':
        form = ActorForm(request.POST, request.FILES, instance=actor)
        if form.is_valid():
            form.save()
            return redirect('actors')
    context = {'form': form, 'is_update': True}
    return render(request, 'MovieForumApp/actor/actor_form.html', context=context)

def deleteActor(request, actor_id):
    actor = Actor.objects.get(actor_id=actor_id)
    actor.delete()
    return redirect('actors')

def singleActorSearchResult(request):
    actor = Actor.objects.filter(fname__contains=request.GET['actor_fname'])
    actor_json = serializers.serialize('json', actor)
    return HttpResponse(actor_json, content_type='application/json')

def allActorsJson(request):
    actors = Actor.objects.all()
    actors_json = serializers.serialize('json', actors)
    return HttpResponse(actors_json, content_type='application/json')

def searchedActors(request):
    context = {}
    countries = Country.objects.all()
    country = request.GET['country']
    from_year = request.GET['from_year']
    to_year = request.GET['to_year']
    if country != "" and from_year != "" and to_year != "":
        year_range = [f"{from_year}-01-01", f"{to_year}-01-01"]
        actors = Actor.objects.filter(country_name=country).distinct().filter(date_of_birth__range=year_range)

    if country == "" and from_year != "" and to_year != "":
        year_range = [f"{from_year}-01-01", f"{to_year}-01-01"]
        actors = Actor.objects.filter(date_of_birth__range=year_range)

    if country != "" and from_year == "" and to_year == "":
        actors = Actor.objects.filter(country_name=country).distinct()
        print(actors)

    actor_count = len(actors)
    actors_and_short_descriptions = []
    for actor in actors:
        if actor.description:
            actors_and_short_descriptions.append((actor, actor.description[0:50] + "..."))
        else:
            actors_and_short_descriptions.append((actor, "This producer has no description provided."))
    context['actors_and_short_descriptions'] = actors_and_short_descriptions
    context['actor_count'] = actor_count
    context['countries'] = countries
    if actors:
        context['featured_actor'] = actors[random.randint(0, len(actors) - 1)]
    return render(request, 'MovieForumApp/actor/actors.html', context=context)


# Director functions.
# <-------------------------------------------------------------> #
def director(request, director_id):
    director = Director.objects.get(director_id=director_id)
    movies_directed = director.movies.values()
    total_movies = len(movies_directed)
    age = get_director_age(director_id)

    context = {'director': director,
               'age': age,
               'movies': movies_directed,
               'total_movies': total_movies,
               }

    if director.description:
        short_description = director.description[0:100] + "..."
        context['short_description']: short_description
    return render(request, 'MovieForumApp/director/director.html', context=context)

def directors(request):
    context = {}
    directors = Director.objects.all()
    countries = Country.objects.all()
    director_count = len(directors)
    directors_and_short_descriptions = []
    for director in directors:
        if director.description:
            directors_and_short_descriptions.append((director, director.description[0:50] + "..."))
        else:
            directors_and_short_descriptions.append((director, "This director has no description provided."))
    context['directors_and_short_descriptions'] = directors_and_short_descriptions
    context['director_count'] = director_count
    if directors:
        context['featured_director'] = directors[random.randint(0, len(directors) - 1)]
    context['countries'] = countries
    return render(request, 'MovieForumApp/director/directors.html', context=context)

@login_required(login_url='dashboard')
def createDirector(request):
    form = DirectorForm()
    if request.method == 'POST':
        form = DirectorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('directors')
    context = {'form': form, 'is_create': True}
    return render(request, 'MovieForumApp/director/director_form.html', context=context)

@login_required(login_url='dashboard')
def updateDirector(request, director_id):
    director = Director.objects.get(director_id=director_id)
    form = DirectorForm(instance=director)

    if request.method == 'POST':
        form = DirectorForm(request.POST, request.FILES, instance=director)
        if form.is_valid():
            form.save()
            return redirect('directors')
    context = {'form': form, 'is_update': True}
    return render(request, 'MovieForumApp/director/director_form.html', context=context)

@login_required(login_url='dashboard')
def deleteDirector(request, director_id):
    director = Director.objects.get(director_id=director_id)
    director.delete()
    return redirect('directors')

def singleDirectorSearchResult(request):
    director = Director.objects.filter(fname__contains=request.GET['director_fname'])
    director_json = serializers.serialize('json', director)
    return HttpResponse(director_json, content_type='application/json')

def allDirectorsJson(request):
    directors = Director.objects.all()
    directors_json = serializers.serialize('json', directors)
    return HttpResponse(directors_json, content_type='application/json')

def searchedDirectors(request):
    context = {}
    countries = Country.objects.all()
    country = request.GET['country']
    from_year = request.GET['from_year']
    to_year = request.GET['to_year']
    if country != "" and from_year != "" and to_year != "":
        year_range = [f"{from_year}-01-01", f"{to_year}-01-01"]
        directors = Director.objects.filter(country_name=country).distinct().filter(date_of_birth__range=year_range)

    if country == "" and from_year != "" and to_year != "":
        year_range = [f"{from_year}-01-01", f"{to_year}-01-01"]
        directors = Director.objects.filter(date_of_birth__range=year_range)

    if country != "" and from_year == "" and to_year == "":
        directors = Director.objects.filter(country_name=country).distinct()
        print(directors)

    director_count = len(directors)
    directors_and_short_descriptions = []
    for director in directors:
        if director.description:
            directors_and_short_descriptions.append((director, director.description[0:50] + "..."))
        else:
            directors_and_short_descriptions.append((director, "This producer has no description provided."))
    context['directors_and_short_descriptions'] = directors_and_short_descriptions
    context['director_count'] = director_count
    context['countries'] = countries
    if directors:
        context['featured_director'] = directors[random.randint(0, len(directors) - 1)]
    return render(request, 'MovieForumApp/director/directors.html', context=context)


# Producer functions.
# <-------------------------------------------------------------> #
def producer(request, producer_id):
    producer = Producer.objects.get(producer_id=producer_id)
    movies_produced = producer.movies.values()
    total_movies = len(movies_produced)
    age = get_producer_age(producer_id)

    context = {'producer': producer,
               'age': age,
               'movies': movies_produced,
               'total_movies': total_movies,
               }

    if producer.description:
        short_description = producer.description[0:100] + "..."
        context['short_description']: short_description
    return render(request, 'MovieForumApp/producer/producer.html', context=context)

def producers(request):
    context = {}
    countries = Country.objects.all()
    producers = Producer.objects.all()
    producer_count = len(producers)
    producers_and_short_descriptions = []
    for producer in producers:
        if producer.description:
            producers_and_short_descriptions.append((producer, producer.description[0:50] + "..."))
        else:
            producers_and_short_descriptions.append((producer, "This producer has no description provided."))
    context['producers_and_short_descriptions'] = producers_and_short_descriptions
    context['producer_count'] = producer_count
    context['countries'] = countries
    if producers:
        context['featured_producer'] = producers[random.randint(0, len(producers) - 1)]
    return render(request, 'MovieForumApp/producer/producers.html', context=context)

@login_required(login_url='dashboard')
def createProducer(request):
    form = ProducerForm()
    if request.method == 'POST':
        form = ProducerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('producers')
    context = {'form': form, 'is_create': True}
    return render(request, 'MovieForumApp/producer/producer_form.html', context=context)

@login_required(login_url='dashboard')
def updateProducer(request, producer_id):
    producer = Producer.objects.get(producer_id=producer_id)
    form = ProducerForm(instance=producer)

    if request.method == 'POST':
        form = ProducerForm(request.POST, request.FILES, instance=producer)
        if form.is_valid():
            form.save()
            return redirect('producers')
    context = {'form': form, 'is_update': True}
    return render(request, 'MovieForumApp/producer/producer_form.html', context=context)

@login_required(login_url='dashboard')
def deleteProducer(request, producer_id):
    producer = Producer.objects.get(producer_id=producer_id)
    producer.delete()
    return redirect('producers')

def singleProducerSearchResult(request):
    producer = Producer.objects.filter(fname__contains=request.GET['producer_fname'])
    producer_json = serializers.serialize('json', producer)
    return HttpResponse(producer_json, content_type='application/json')

def allProducersJson(request):
    producers = Producer.objects.all()
    producers_json = serializers.serialize('json', producers)
    return HttpResponse(producers_json, content_type='application/json')

def searchedProducers(request):
    context = {}
    countries = Country.objects.all()
    country = request.GET['country']
    from_year = request.GET['from_year']
    to_year = request.GET['to_year']
    if country != "" and from_year != "" and to_year != "":
        year_range = [f"{from_year}-01-01", f"{to_year}-01-01"]
        producers = Producer.objects.filter(country_name=country).distinct().filter(date_of_birth__range=year_range)

    if country == "" and from_year != "" and to_year != "":
        year_range = [f"{from_year}-01-01", f"{to_year}-01-01"]
        producers = Producer.objects.filter(date_of_birth__range=year_range)

    if country != "" and from_year == "" and to_year == "":
        producers = Producer.objects.filter(country_name=country).distinct()

    producer_count = len(producers)
    producers_and_short_descriptions = []
    for producer in producers:
        if producer.description:
            producers_and_short_descriptions.append((producer, producer.description[0:50] + "..."))
        else:
            producers_and_short_descriptions.append((producer, "This producer has no description provided."))
    context['producers_and_short_descriptions'] = producers_and_short_descriptions
    context['producer_count'] = producer_count
    context['countries'] = countries
    if producers:
        context['featured_producer'] = producers[random.randint(0, len(producers) - 1)]
    return render(request, 'MovieForumApp/producer/producers.html', context=context)


# Movie functions.
# <-------------------------------------------------------------> #
def singleMovieSearchResult(request):
    movie = Movie.objects.filter(title=request.GET['movie_name'])
    movie_json = serializers.serialize('json', movie)
    return HttpResponse(movie_json, content_type='application/json')

@login_required(login_url='dashboard')
def favoriteMovie(request, movie_id):
    auth_user = AuthUser.objects.get(id=request.user.id)
    movie = Movie.objects.get(movie_id=movie_id)
    Favorite.objects.create(movie_id_movie=movie, user_id_user=auth_user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='dashboard')
def unfavoriteMovie(request, movie_id):
    Favorite.objects.filter(movie_id_movie=movie_id).filter(user_id_user=request.user.id).first().delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='dashboard')
def favoritedMovies(request):
    genres = Genre.objects.all()
    auth_user = AuthUser.objects.get(id=request.user.id)
    favorites = Favorite.objects.filter(user_id_user=auth_user)
    movies = []
    for favorite in favorites:
        movies.append(Movie.objects.get(movie_id=favorite.movie_id_movie.movie_id))
    average_ratings = []
    for movie in movies:
        average_ratings.append(Rating.objects.filter(movie_id_movie=movie.movie_id).aggregate(Avg('numeric_rating')))
    return render(request, 'MovieForumApp/movie/movies.html',
                  {'movies': zip(movies, average_ratings), 'genres': genres})

@login_required(login_url='dashboard')
def rateMovie(request, movie_id, star_value):
    auth_user = AuthUser.objects.get(id=request.user.id)
    movie = Movie.objects.get(movie_id=movie_id)
    Rating.objects.create(movie_id_movie=movie, numeric_rating=star_value, user_id_user=auth_user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='dashboard')
def ratedMovies(request):
    genres = Genre.objects.all()
    auth_user = AuthUser.objects.get(id=request.user.id)
    ratings = Rating.objects.filter(user_id_user=auth_user)
    movies = []
    for rating in ratings:
        movies.append(Movie.objects.get(movie_id=rating.movie_id_movie.movie_id))
    average_ratings = []
    for movie in movies:
        average_ratings.append(Rating.objects.filter(movie_id_movie=movie.movie_id).aggregate(Avg('numeric_rating')))
    return render(request, 'MovieForumApp/movie/movies.html',
                  {'movies': zip(movies, average_ratings), 'genres': genres})


def movie(request, movie_id):
    rating = Rating.objects.filter(movie_id_movie=movie_id).filter(user_id_user=request.user.id).first()
    favorite = Favorite.objects.filter(movie_id_movie=movie_id).filter(user_id_user=request.user.id).first()
    print(f"\n\nFound favorite: {favorite}\n\n")
    avg_rating = Rating.objects.filter(movie_id_movie=movie_id).aggregate(Avg('numeric_rating'))
    rating_count = Rating.objects.filter(movie_id_movie=movie_id).count()
    movie = Movie.objects.get(movie_id=movie_id)
    genres = movie.genres.values()
    comments = Comment.objects.filter(movie_id_movie=movie_id)
    auth_users = []
    comments_and_their_replies = []
    for comment in comments:
        replies = Reply.objects.filter(comment_id_comment=comment.comment_id)
        comments_and_their_replies.append((comment, replies))
        auth_user = User.objects.get(id=comment.user_id_user.id)
        auth_users.append(auth_user)
    if comments:
        single_comment = comments[0]
        comment_count = len(comments)
    revenue = get_revenue(movie_id)
    actors = movie.actors.values()
    directors = []
    producers = []
    directors_initials = []
    producers_initials = []
    for producer in movie.producers.values():
        producers.append(producer)
        producers_initials.append(producer['fname'][0] + "" + producer['lname'][0])
    for director in movie.directors.values():
        directors.append(director)
        directors_initials.append(director['fname'][0] + "" + director['lname'][0])
    context = {
        'movie': movie,
        'genres': genres,
        'revenue': revenue,
        'actors': actors,
        'directors_and_initials': zip(directors, directors_initials),
        'producers_and_initials': zip(producers, producers_initials),
    }
    if comments:
        context['single_comment'] = single_comment
        context['comment_count'] = comment_count
        context['users_and_comments'] = zip(comments_and_their_replies, auth_users)
    if movie.directors.values():
        context['star_director'] = movie.directors.values()[0]
    if rating:
        context['rating'] = rating
        context['score'] = range(rating.numeric_rating)
        context['rating_count'] = rating_count
    context['favorite'] = favorite
    context['avg_rating'] = avg_rating


    return render(request, 'MovieForumApp/movie/movie.html', context=context)


def movies(request):
    movies = Movie.objects.all()
    genres = Genre.objects.all()
    average_ratings = []
    for movie in movies:
        average_ratings.append(Rating.objects.filter(movie_id_movie=movie.movie_id).aggregate(Avg('numeric_rating')))
    return render(request, 'MovieForumApp/movie/movies.html',
                  {'movies': zip(movies, average_ratings), 'genres': genres})

def allMoviesJson(request):
    movies = Movie.objects.all()
    movies_json = serializers.serialize('json', movies)
    return HttpResponse(movies_json, content_type='application/json')

def searchedMovies(request):
    all_genres = Genre.objects.all()
    genres = request.GET.getlist('genres')
    from_year = request.GET['from_year']
    to_year = request.GET['to_year']
    if len(genres) and from_year != "" and to_year != "":
        year_range = [f"{from_year}-01-01", f"{to_year}-01-01"]
        movies = Movie.objects.filter(genres__in=genres).distinct().filter(date_of_release__range=year_range)

    if not len(genres) and from_year != "" and to_year != "":
        year_range = [f"{from_year}-01-01", f"{to_year}-01-01"]
        movies = Movie.objects.filter(date_of_release__range=year_range).distinct()

    if len(genres) and from_year == "" and to_year == "":
        movies = Movie.objects.filter(genres__in=genres).distinct()

    average_ratings = []
    for movie in movies:
        average_ratings.append(Rating.objects.filter(movie_id_movie=movie.movie_id).aggregate(Avg('numeric_rating')))

    return render(request, 'MovieForumApp/movie/movies.html',
                  {'movies': zip(movies, average_ratings), 'genres': all_genres})


@login_required(login_url='dashboard')
def createMovie(request):
    form = MovieForm()
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('movies')
    context = {'form': form}
    return render(request, 'MovieForumApp/movie/movie_form.html', context=context)

@login_required(login_url='dashboard')
def updateMovie(request, movie_id):
    movie = Movie.objects.get(movie_id=movie_id)
    form = MovieForm(instance=movie)

    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movies')
    context = {'form': form}
    return render(request, 'MovieForumApp/movie/movie_form.html', context=context)

@login_required(login_url='dashboard')
def deleteMovie(request, movie_id):
    movie = Movie.objects.get(movie_id=movie_id)
    movie.delete()
    return redirect('movies')

@login_required(login_url='dashboard')
def createGenre(request):
    form = GenreForm()
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movies')
    context = {'form': form}
    return render(request, 'MovieForumApp/genre/genre_form.html', context=context)

@login_required(login_url='dashboard')
def createComment(request, movie_id):
    movie = Movie.objects.get(movie_id=movie_id)
    auth_user = AuthUser.objects.get(id=request.user.id)
    if request.method == 'POST':
        comment = request.POST.get('comment')
        Comment.objects.create(movie_id_movie=movie, content=comment, user_id_user=auth_user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='dashboard')
def createReply(request, comment_id):
    auth_user = AuthUser.objects.get(id=request.user.id)
    if request.method == 'POST':
        reply = request.POST.get('reply')
        comment = Comment.objects.filter(comment_id = comment_id).first()
        Reply.objects.create(comment_id_comment=comment, content=reply, user_id_user=auth_user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
