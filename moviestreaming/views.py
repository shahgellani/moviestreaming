from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect

# Create your views here.
from moviestreaming.models import UserC, Movie, Review


def start(request, message=None):
    """

    :param message:
    :param request:
    :return:
    """
    return render(request, "login.html", {'message': message})


def user_login(request):
    """

    :param request:
    :return:
    """
    user_exists = None
    email_address_frm_page = request.GET['email']
    password_from_page = request.GET['password']
    user_exists = authenticate(email=email_address_frm_page, password=password_from_page)

    if user_exists is not None:
        print(user_exists)
        if user_exists.is_superuser:
            login(request, user_exists)
            return redirect('moviestreaming:home')
        else:
            login(request, user_exists)
            return redirect('moviestreaming:user_panel')





    else:
        return start(request, message='Wrong Credentials')


@login_required()
def registration(request):
    """

    :param request:
    :return:
    """

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email_address = request.POST.get('email')
        password = request.POST.get('password')
        user = len(UserC.objects.filter(email=email_address))
        print(user)
        if user != 0:
            return render(request, "home.html", {'error': 'Email already exists'})

        UserC.objects.create_normal_user(first_name=first_name, last_name=last_name, email=email_address,
                                         password=password)

        # user = UserC()
        # user.get_email_field_name()
        return render(request, 'home.html', {'user_added': 'User added'})


@login_required()
def add_movie(request):
    """

    :param request:
    :return:
    """
    if request.method == 'POST':
        title = request.POST.get('movie-title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        year = request.POST.get('year')
        movie_url = request.POST.get('movie-link')
        movie_obj = Movie(title=title, description=description, category=category, year=year, movie_url=movie_url)
        movie_obj.save()
        return render(request, 'home.html', {'movie_added': 'Movie added'})


@login_required(login_url='/')
def show_users(request):
    """
    Method for showing all users

    :return:
    """

    users_data = UserC.objects.all()

    return render(request, 'users_show.html', {'users': users_data})

@login_required()
def edit_users(request):
    """
    Method for editing user on the basis of email ID

    :param request:
    :return:
    """
    user_obj = UserC.objects.filter(email=request.POST.get('email')).get()

    return render(request, 'users_edit.html', {'user': user_obj})


@login_required(login_url='/')
def admin_panel(request):
    return render(request, 'home.html')

@login_required()
def save_edit_users(request):
    """

    :param request:
    :return:
    """
    user_obj = UserC.objects.filter(email=request.POST.get('email')).get()
    user_obj.first_name = request.POST.get('first_name')
    user_obj.last_name = request.POST.get('last_name')
    user_obj.save()

    return show_users(request)

@login_required()
def save_edit_movie_details(request):
    """

    :param request:
    :return:
    """
    movie_obj = Movie.objects.filter(id=request.POST.get('movie-id')).get()
    movie_obj.title = request.POST.get('movie-title')
    movie_obj.description = request.POST.get('description')
    movie_obj.movie_url = request.POST.get('movie-link')
    movie_obj.save()

    return show_movies(request)

@login_required()
def show_movies(request):
    """

    :param request:
    :return:
    """
    movies_list = Movie.objects.all()

    return render(request, 'show_movies.html', {'movies': movies_list})

@login_required()
def edit_movie_detail(request):
    """

    :param request:
    :return:
    """
    movie_obj = Movie.objects.filter(id=request.POST.get('movie_id')).get()

    return render(request, 'edit_movie_detail.html', {'movie': movie_obj})


def delete_movie(request):
    Movie.objects.filter(id=request.POST.get('movie_id')).delete()
    return show_movies(request)


def delete_user(request):
    UserC.objects.filter(email=request.POST.get('email_id')).delete()
    return show_users(request)


@login_required(login_url='/')
def user_panel(request):
    rating_list = []
    total_users = []
    movie_list = Movie.objects.all()
    for m in movie_list:
        total = findRating(m)
        total_user = Review.objects.filter(movie=m).count()

        if total == 0:
            rating_list.append(0)
            total_users.append(total_user)
        else:
            avgrate = total / total_user
            rating_list.append(avgrate)
            total_users.append(total_user)

    zipped_List = zip(movie_list, rating_list, total_users)



    return render(request, "userpanel.html", {'movies': zipped_List })


def rate(request):
    """

    :param request:
    :return:
    """
    current_user = request.user
    movie_id = request.POST.get('movie_id')
    user_id = current_user.id
    rating = request.POST.get('rate')

    try:
        obj = Review.objects.get(movie_id=movie_id, user_id=user_id)
        obj.rating = rating
        obj.save()
        return user_panel(request)

    except Review.DoesNotExist:
        obj = Review.objects.create(movie_id=movie_id, user_id=user_id, rating=rating)
        obj.save()
        return user_panel(request)



def findRating(movie):
    total = 0
    for i in range(5):
        total_user_rating = Review.objects.filter(movie=movie,
                                                  rating=i + 1).count()
        if total_user_rating == 0:
            rating_val = 0
        else:
            rating_val = (i + 1) * total_user_rating
        total = total + rating_val

    return total


def user_logout(request):
    logout(request)
    return redirect('moviestreaming:start')
