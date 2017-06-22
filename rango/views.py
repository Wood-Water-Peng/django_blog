from datetime import datetime

from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# from rango.forms import CategoryForm
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from rango.models import Category
from rango.models import Page


def index(request):
    # context_dict = {'boldmessage': "I am bold font from the context"}
    visits = int(request.COOKIES.get('visits', '1'))
    reset_last_visit_time = False

    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    response = render(request, 'rango/index.html', context_dict)
    if 'last_visit' in request.COOKIES:
        # Get the cookie's value
        last_visit = request.COOKIES['last_visit']
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
        # If it's been more than a day since the last visit
        if (datetime.now() - last_visit_time).seconds > 10:
            visits = visits + 1
            reset_last_visit_time = True
    else:
        reset_last_visit_time = True

    context_dict['visits'] = visits
    response = render(request, 'rango/index.html', context_dict)

    if reset_last_visit_time:
        response.set_cookie('last_visit', datetime.now())
        response.set_cookie('visits', visits)
    print ("visits: %s" % visits)
    return response


def about(request):
    # return HttpResponse("Rango says here is aboue page! <br/> <a href='/rango/'>Index</a>")
    context_dict = {'boldmessage': "I am bold font from the context"}

    return render(request, 'rango/about.html', context_dict)


def category(request, category_name_url):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_url)
        category_name = decode_url(category_name_url)
        context_dict['category_name'] = category_name

        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category
        context_dict['category_name_url'] = category_name_url
    except Category.DoesNotExist:
        pass

    return render(request, 'rango/category.html', context_dict)


@login_required
def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})


def decode_url(str):
    return str.replace('_', ' ')


def encode_url(str):
    return str.replace(' ', '_')


@login_required
def add_page(request, category_name_url):
    category_name = decode_url(category_name_url)
    try:
        print ("category_url:" + category_name_url)
        print ("category_name:" + category_name)
        cat = Category.objects.get(slug=category_name)
        print ("cat_name:" + str(cat))
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        print ("POST request coming!!!")
        if form.is_valid():
            print ("Form is valid!!!")
            if cat:
                print ("Entering cat!!!")
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()

                return category(request, category_name_url)
        else:
            print ("Form Errors!!!")
            print form.errors
    else:
        form = PageForm()

    context_dict = {}
    context_dict['form'] = form
    context_dict['category_name_url'] = category_name_url
    context_dict['category_name'] = category_name

    return render(request, 'rango/add_page.html', context_dict)


def register(request):
    registered = False
    if request.session.test_cookie_worked():
        print ">>>> TEST COOKIE WORKED!"
        request.session.delete_test_cookie()

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'rango/register.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    # If the request is a HTTP POST,try to pull out the relevant information
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                # An inactive account was used - no login in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'rango/login.html', {})


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")


@login_required
def user_logout(request):
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/rango/')


@login_required
def like_category(request):
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']
    likes = 0

    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()

    return HttpResponse(likes)

def test(request):

    return render(request, 'rango/test.html')