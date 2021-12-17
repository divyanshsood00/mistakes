from django.contrib.auth.models import User
from django.contrib.messages.api import error
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from users.utils import searchProfiles, paginateProfiles
from blogs.utils import paginateBlogs
from .forms import CustomUserCreationForm, InterestForm, MessageForm, ProfileForm
from django.contrib.auth.decorators import login_required
from .models import Profile


# ++++++++++++ PROFILE VIEWING ++++++++++++++


def profiles(request):
    # searching profiles
    profiles, search_query = searchProfiles(request)
    # paginating profiles
    results = 3
    profiles, custom_range, paginator = paginateProfiles(
        request, profiles, results)
    props = {'profiles': profiles, 'search_query': search_query,
             'paginator': paginator, 'custom_range': custom_range}
    return render(request, 'users/profiles.html', props)


# Needs citation ----- Convert skill to interests
def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.interests_set.exclude(description__exact="")
    otherSkills = profile.interests_set.filter(description="")
    props = {'p': profile, 'topSkills': topSkills, 'otherSkills': otherSkills}
    return render(request, 'users/user-profile.html', props)

# +++++++++++++ PROFILE EDITING +++++++++++++


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    interests = profile.interests_set.all()
    blogs = profile.blog_set.all()
    results = 6
    blogs, custom_range, paginator = paginateBlogs(request, blogs, results)
    context = {'profile': profile, 'interests': interests,
               'blogs': blogs, 'custom_range': custom_range}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)

# +++++++++++ INTEREST EDITING ++++++++++++


@login_required(login_url="login")
def createInterest(request):
    form = InterestForm()
    if request.method == "POST":
        form = InterestForm(request.POST)
        if form.is_valid():
            interest = form.save(commit=False)
            interest.user = request.user.profile
            interest.save()
            messages.success(request, "Interest was Created")
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/interest_form.html', context)


@login_required(login_url="login")
def updateInterest(request, pk):
    profile = request.user.profile
    interest = profile.interests_set.get(id=pk)
    form = InterestForm(instance=interest)
    if request.method == "POST":
        form = InterestForm(request.POST, instance=interest)
        if form.is_valid():
            form.save()
            messages.success(request, "Interest was Updated")
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/interest_form.html', context)


@login_required(login_url="login")
def deleteInterest(request, pk):
    profile = request.user.profile
    interest = profile.interests_set.get(id=pk)
    if request.method == "POST":
        if interest:
            interest.delete()
            messages.success(request, "Interest was Deleted")
        return redirect('account')

    return render(request, 'blogs/delete_obj.html', {'name': interest.name})

# ++++++++++ LOGIN / LOGOUT ++++++++++


def loginPage(request):
    page = "login"
    props = {'page': page}
    flag = False
    if request.user.is_authenticated:
        return redirect('blogs')
    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            flag = True
            messages.error(
                request, 'There is a Mistake in your credentials.')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        elif not flag:
            messages.error(
                request, 'There is a Mistake in your credentials.')
    return render(request, 'users/login_register.html', props)


def logoutPage(request):
    try:
        logout(request)
        messages.info(
            request, "User logged out successfully!")
        return redirect('login')
    except:
        messages.error(request, "Something seems Wrong, Try again")


def registerPage(request):
    page = "register"
    form = CustomUserCreationForm
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "Account Created! Let's Mistake")
            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(request, "An error occured during registration.")

    props = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', props)

# ++++++++++++++++++ MESSAGE SECTION ++++++++++++++++++


@login_required(login_url='login')
def inbox(request):
    context = {}
    try:
        profile = request.user.profile
        # Not doing messages_set as we have mejik in models.py
        messageList = profile.messages.all()
        unreadCount = messageList.filter(is_read=False).count()
        context = {'messageList': messageList, 'unreadCount': unreadCount}
    except:
        messages.error(
            request, "Some error occured TRY AGAIN or TROUBLESHOOT!!")
    return render(request, 'users/inbox.html', context)


@login_required(login_url="login")
def viewMessage(request, pk):
    context = {}
    try:
        profile = request.user.profile
        myMessage = profile.messages.get(id=pk)
        if request.method == "POST":
            myMessage.delete()
            return redirect('inbox')
        if myMessage and not myMessage.is_read:
            myMessage.is_read = True
            myMessage.save()
        context = {'myMessage': myMessage}
    except:
        messages.error(request, "Some error occured, TRY AGAIN !!")
    return render(request, 'users/message.html', context)


@login_required(login_url='login')
def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            try:
                message = form.save(commit=False)
                message.recipient = recipient
                message.sender = request.user.profile
                message.name = request.user.profile.name
                message.email = recipient.email
                message.save()
                messages.success(request, "Message sent successfully")
                return redirect('profile', pk=recipient.id)
            except:
                messages.error(
                    request, "There was some problem in sending message")
    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message_form.html', context)
