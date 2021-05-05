from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

GENDERS = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)


class User(AbstractUser):
    photo = models.ImageField(upload_to='image/%y')


class UserProfile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='profile')
    photo = models.ImageField(upload_to='image/%y')


class Country(models.Model):
    country_name = models.CharField(max_length=100, primary_key=True)

    class Meta:
        managed = False
        db_table = 'country'

    def __str__(self):
        return self.country_name


class Actor(models.Model):
    actor_id = models.AutoField(primary_key=True)
    gender = models.CharField(max_length=6, choices=GENDERS)
    fname = models.CharField(max_length=50)
    mname = models.CharField(max_length=2, blank=True, null=True)
    lname = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    image = models.ImageField(upload_to='image/%y')
    country_name = models.ForeignKey(Country, on_delete=models.SET_NULL, db_column='country_name', null=True)
    description = models.TextField()
    instagram = models.CharField(max_length=100)
    twitter = models.CharField(max_length=100)
    linkedin = models.CharField(max_length=100)
    movies = models.ManyToManyField('Movie', through='ManyMovieHasManyActor', blank=True)

    class Meta:
        managed = False
        db_table = 'actor'

    def __str__(self):
        if self.mname:
            return f"{self.fname} {self.mname} {self.lname}"
        else:
            return f"{self.fname} {self.lname}"


class Director(models.Model):
    director_id = models.AutoField(primary_key=True)
    gender = models.CharField(max_length=6, choices=GENDERS)
    fname = models.CharField(max_length=50)
    mname = models.CharField(max_length=2, blank=True, null=True)
    lname = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    image = models.ImageField(upload_to='image/%y')
    country_name = models.ForeignKey(Country, on_delete=models.SET_NULL, db_column='country_name', null=True)
    description = models.TextField()
    instagram = models.CharField(max_length=100)
    twitter = models.CharField(max_length=100)
    linkedin = models.CharField(max_length=100)
    movies = models.ManyToManyField('Movie', through='ManyMovieHasManyDirector', blank=True)

    class Meta:
        managed = False
        db_table = 'director'

    def __str__(self):
        if self.mname:
            return f"{self.fname} {self.mname} {self.lname}"
        else:
            return f"{self.fname} {self.lname}"


class Producer(models.Model):
    producer_id = models.AutoField(primary_key=True)
    gender = models.CharField(max_length=6, choices=GENDERS)
    fname = models.CharField(max_length=50)
    mname = models.CharField(max_length=2, blank=True, null=True)
    lname = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    image = models.ImageField(upload_to='image/%y')
    country_name = models.ForeignKey(Country, on_delete=models.SET_NULL, db_column='country_name', null=True)
    description = models.TextField()
    instagram = models.CharField(max_length=100)
    twitter = models.CharField(max_length=100)
    linkedin = models.CharField(max_length=100)

    movies = models.ManyToManyField('Movie', through='ManyMovieHasManyProducer', blank=True)

    class Meta:
        managed = False
        db_table = 'producer'

    def __str__(self):
        if self.mname:
            return f"{self.fname} {self.mname} {self.lname}"
        else:
            return f"{self.fname} {self.lname}"


class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    date_of_release = models.DateField()
    title = models.CharField(max_length=100)
    budget = models.IntegerField(blank=True, null=True)
    income = models.IntegerField(blank=True, null=True)
    trailer = models.CharField(max_length=100, null=True)
    description = models.TextField()
    image = models.FileField(upload_to='image/%y')
    runtime = models.IntegerField()
    plot_keywords = ArrayField(models.TextField())
    genres = models.ManyToManyField('Genre', through='ManyMovieHasManyGenre', blank=True)
    actors = models.ManyToManyField('Actor', through='ManyMovieHasManyActor', blank=True)
    producers = models.ManyToManyField('Producer', through='ManyMovieHasManyProducer', blank=True)
    directors = models.ManyToManyField('Director', through='ManyMovieHasManyDirector', blank=True)

    class Meta:
        managed = False
        db_table = 'movie'

    def __str__(self):
        return self.title


class Genre(models.Model):
    name = models.CharField(primary_key=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'genre'

    def __str__(self):
        return self.name


class ManyMovieHasManyActor(models.Model):
    id = models.AutoField(primary_key=True)
    movie_id_movie = models.ForeignKey(Movie, on_delete=models.CASCADE, db_column='movie_id_movie')
    actor_id_actor = models.ForeignKey(Actor, on_delete=models.CASCADE, db_column='actor_id_actor')

    class Meta:
        managed = False
        db_table = 'many_movie_has_many_actor'


class ManyMovieHasManyDirector(models.Model):
    id = models.AutoField(primary_key=True)
    movie_id_movie = models.ForeignKey(Movie, on_delete=models.CASCADE, db_column='movie_id_movie')
    director_id_director = models.ForeignKey(Director, on_delete=models.CASCADE, db_column='director_id_director')

    class Meta:
        managed = False
        db_table = 'many_movie_has_many_director'


class ManyMovieHasManyGenre(models.Model):
    id = models.AutoField(primary_key=True)
    movie_id_movie = models.ForeignKey(Movie, on_delete=models.CASCADE, db_column='movie_id_movie')
    name_genre = models.ForeignKey(Genre, models.CASCADE, db_column='name_genre')

    class Meta:
        managed = False
        db_table = 'many_movie_has_many_genre'


class ManyMovieHasManyProducer(models.Model):
    id = models.AutoField(primary_key=True)
    movie_id_movie = models.ForeignKey(Movie, on_delete=models.CASCADE, db_column='movie_id_movie')
    producer_id_producer = models.ForeignKey(Producer, on_delete=models.CASCADE, db_column='producer_id_producer')

    class Meta:
        managed = False
        db_table = 'many_movie_has_many_producer'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'MovieForumApp_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

class Rating(models.Model):
    rating_id=models.AutoField(primary_key=True)
    numeric_rating = models.IntegerField(default=0,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0),
        ]
    )
    movie_id_movie = models.ForeignKey(Movie, models.DO_NOTHING, db_column='movie_id_movie', blank=True, null=True)
    user_id_user = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='user_id_user', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rating'


class Favorite(models.Model):
    favorite_id = models.AutoField(primary_key=True)
    movie_id_movie = models.ForeignKey(Movie, models.DO_NOTHING, db_column='movie_id_movie', blank=True, null=True)
    user_id_user = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='user_id_user', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'favorite'


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    content = models.TextField(blank=True, null=True)
    movie_id_movie = models.ForeignKey('Movie', models.DO_NOTHING, db_column='movie_id_movie', blank=True, null=True)
    user_id_user = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='user_id_user', blank=True, null=True)
    creation_date = models.DateTimeField(default=timezone.localtime(timezone.now()))

    class Meta:
        managed = False
        db_table = 'comment'


class Reply(models.Model):
    reply_id = models.AutoField(primary_key=True)
    content = models.TextField(blank=True, null=True)
    comment_id_comment = models.ForeignKey(Comment, models.DO_NOTHING, db_column='comment_id_comment', blank=True, null=True)
    user_id_user = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='user_id_user', blank=True, null=True)
    creation_date = models.DateTimeField(default=timezone.localtime(timezone.now()))

    class Meta:
        managed = False
        db_table = 'reply'
