from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from . import forms
from . import models


def minimal_context(request):
    search_form = forms.SearchForm()

    return {
            'is_authenticated': request.user.is_authenticated,
            'search_form': search_form,
    }


def do_search_if_requested(call_view):
    def view_wrapper(request, *args, **kwargs):
        if request.method == 'POST' and 'searching' in request.POST:
            return redirect('search', request.POST['searching'])

        return call_view(request, *args, **kwargs)

    return view_wrapper


@do_search_if_requested
def root(request):
    return redirect('home')


@do_search_if_requested
def index(request):
    context = minimal_context(request)
    return render(request, 'portfolios/index.html', context)


@do_search_if_requested
def about(request):
    context = minimal_context(request)
    return render(request, 'portfolios/about.html', context)


@login_required
@do_search_if_requested
def profile(request):
    return redirect('user', request.user.username)


@do_search_if_requested
def user(request, username=None):
    if not username:
        return redirect('home')

    user = User.objects.get(username=username)
    profile = models.Profile.objects.get(user_id=user)

    context = minimal_context(request)
    context['username'] = user.username
    context['first_name'] = user.first_name
    context['last_name'] = user.last_name
    context['email'] = user.email

    context['middle_name'] = profile.middle_name

    if profile.birthdate:
        import locale
        import datetime
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        context['birthdate'] = profile.birthdate.strftime("%d %B, %Y")

    def make_preview(descr):
        preview = ''
        descr_words = descr.split(' ')

        for word in descr_words:
            if len(preview) + len(word) >= 200:
                break
            preview += ' ' + word

        if not (preview[-1].isalpha() or preview[-1].isdigit()):
            preview = preview[:-1]

        return preview + '...'

    portfolios = models.Portfolio.objects.filter(user_id=user)
    context['portfolios'] = []
    for portfolio in portfolios:
        context['portfolios'].append(type("", (), {
            'profession': models. \
                          Profession. \
                          objects.get(id=portfolio.profession_id.id).name,
            'description_preview': make_preview(portfolio.description),
            'id': portfolio.id,
        }))

    context['is_owner'] = user.username == request.user.username

    return render(request, 'portfolios/user.html', context)


@do_search_if_requested
def logout(request):
    auth.logout(request)

    return redirect('home')


@do_search_if_requested
def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        auth_user_form = forms.AuthUserForm(request.POST)

        if auth_user_form.is_valid:
            username = auth_user_form.data['username']
            password = auth_user_form.data['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    return redirect('profile')
                else:
                    pass
            else:
                pass
        else:
            pass
    else:
        auth_user_form = forms.AuthUserForm()

    context = minimal_context(request)
    context['auth_user_form'] = auth_user_form

    return render(request, 'portfolios/login.html', context)


@do_search_if_requested
def join(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        user_form = forms.UserForm(request.POST)
        profile_form = forms.ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            profile = profile_form.save(commit=False)

            user = User.objects.create_user(
                user_form.data['username'],
                user_form.data['email'],
                user_form.data['password'],
            )

            user.first_name = user_form.data['first_name']
            user.last_name = user_form.data['last_name']
            user.save()

            profile.user_id = user
            profile.save()

            return redirect('login')

    else:
        user_form = forms.UserForm()
        profile_form = forms.ProfileForm()

    context = minimal_context(request)
    context['user_form'] = user_form
    context['profile_form'] = profile_form

    return render(request, 'portfolios/join.html', context)


@do_search_if_requested
def search(request, searching=None):
    users= User.objects \
               .filter(username__icontains=searching) \
               .exclude(is_staff=True) \
               .annotate(portfolios_qty=Count('portfolio__id'))

    context = minimal_context(request)
    context['searching'] = searching
    context['users'] = users
    context['users_qty'] = len(users)

    return render(request, 'portfolios/search.html', context)


@do_search_if_requested
@login_required
def create(request):
    context = minimal_context(request)

    if request.method == "POST":
        portfolio_form = forms.PortfolioForm(request.POST)
        profession_name = portfolio_form.data['profession']
        description = portfolio_form.data['description']

        user_portfolios = models \
                          .Portfolio \
                          .objects \
                          .filter(user_id=request.user)
        user_professions = models \
                           .Profession \
                           .objects \
                           .filter(id__in=user_portfolios \
                                          .values('profession_id'))

        if not user_professions.filter(name=profession_name):
            portfolio = models.Portfolio()
            portfolio.user_id = request.user
            portfolio.profession_id = models \
                                      .Profession \
                                      .objects.get(name=profession_name)
            portfolio.description = description
            portfolio.save()

            return redirect('profile')

        context['alert'] = 'Портфолио для такой профессии уже создано'
        context['description'] = description
        context['profession'] = profession_name
    else:
        portfolio_form = forms.PortfolioForm()

    professions = models.Profession.objects.all()

    context['professions'] = professions
    context['portfolio_form'] = portfolio_form

    return render(request, 'portfolios/portfolio_create.html', context)


@do_search_if_requested
def portfolio(request, portfolio_id):
    context = minimal_context(request)
    portfolio = models.Portfolio.objects.get(id=portfolio_id)
    
    if request.method == 'POST':
        post_form = forms.PostForm(request.POST)

        import datetime
        post = models.Post()
        post.portfolio_id = portfolio
        post.title = post_form.data['title']
        post.content = post_form.data['content']
        post.create_time = datetime.datetime.now()
        post.save()

        return redirect('portfolio', portfolio_id)
    else:
        post_form = forms.PostForm()

    profession = models.Profession.objects.get(id=portfolio.profession_id.id)
    profile = models.Profile.objects.get(user_id=portfolio.user_id.id)
    user = User.objects.get(id=portfolio.user_id.id)
    posts_query = models.Post.objects \
                             .filter(portfolio_id=portfolio.id) \
                             .annotate(comments_qty=Count('comment__id'))

    posts = []
    for post_query in posts_query:
        posts.append(type("", (), {
            "create_time": post_query.create_time,
            "update_time": post_query.update_time,
            "title": post_query.title,
            "content": str(post_query.content).split('\n'),
            "id": int(post_query.id),
            "comments_qty": post_query.comments_qty,
        }))

    portfolio_descr = str(portfolio.description).split('\n')

    context['profession'] = profession
    context['portfolio'] = portfolio
    context['portfolio_descr'] = portfolio_descr
    context['profile'] = profile
    context['user'] = user
    context['is_owner'] = user.username == request.user.username
    context['posts'] = posts
    context['post_form'] = post_form

    return render(request, 'portfolios/portfolio.html', context)


@do_search_if_requested
def post(request, post_id):
    context = minimal_context(request)

    post_query = models.Post.objects.get(id=post_id)
    portfolio = models.Portfolio.objects.get(id=post_query.portfolio_id.id)
    profession = models.Profession.objects.get(id=portfolio.profession_id.id)
    comments_query = models.Comment.objects.filter(post_id=post_query.id)
    user = User.objects.get(id=portfolio.user_id.id)

    post = type("", (), {
        "create_time": post_query.create_time,
        "update_time": post_query.update_time,
        "title": post_query.title,
        "content": str(post_query.content).split('\n'),
        "id": int(post_query.id),
    })

    comments = []
    for comment_query in comments_query:
        comments.append(type("", (), {
            "user": comment_query.user_id,
            "content": str(comment_query.content).split('\n'),
            "create_time": comment_query.create_time,
        }))

    if request.method == 'POST':
        comment_form = forms.CommentForm(request.POST)

        import datetime
        comment = models.Comment()
        comment.content = comment_form.data['content']
        comment.user_id = request.user
        comment.post_id = post_query
        comment.create_time = datetime.datetime.now()
        comment.save()

        return redirect('post', post_id)
    else:
        comment_form = forms.CommentForm()

    context['post'] = post
    context['portfolio'] = portfolio
    context['profession'] = profession
    context['user'] = user
    context['comments'] = comments
    context['comment_form'] = comment_form

    return render(request, 'portfolios/post.html', context)
