from django.shortcuts import render, redirect
from .models import Poll, Venue, User, Option
from .forms import VenueForm, MyUserCreationForm
import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    today = datetime.datetime.now()
    current_week = today - datetime.timedelta(days=today.weekday())
    try:
        poll = Poll.objects.get(active=True)
        venues = poll.option_set.all().order_by('-votes')  
        total_votes = 0
        for x in venues:
            total_votes +=x.votes
        
        context = {'poll':poll, 'venues': venues, 'current_week': current_week.date, 'total_votes': total_votes}
     
    except Poll.DoesNotExist:
        poll = None
        context ={'poll':poll, 'current_week': current_week}

   
   
    
    return render(request, 'base/home.html', context)

@login_required(login_url='login')
def createMove(request,pk):
    form = VenueForm()
    selected_poll = Poll.objects.get(id=pk)
    if request.user in selected_poll.participants.all():
        messages.error(request, "You have already participated in this poll.")
        return redirect('home')
    else:
        if request.method=="POST":
            form = VenueForm(request.POST)
            if form.is_valid():
                print('success')
                try:
                    suggested_option = Venue.objects.get(name=form.cleaned_data['name'].lower())
                    if suggested_option in selected_poll.venues.all():
                        messages.error(request, "This move was already suggested. Please vote on the existing choice.")
                    else:
                        Option.objects.create(
                            venue = suggested_option,
                            poll=selected_poll,
                            user_votes=request.user,
                        )
                        selected_poll.participants.add(request.user)
                        selected_poll.venues.add(suggested_option)
                    return redirect('home')
                        
                except Venue.DoesNotExist:
                    new_venue=Venue.objects.create(
                            host = request.user,
                            website = form.cleaned_data['website'],
                            # address = form.cleaned_data['address'],
                            name = form.cleaned_data['name'].lower()
                            )
                    Option.objects.create(
                        venue=new_venue,
                        poll=selected_poll,
                        user_votes=request.user,
                        
                    )
                    selected_poll.venues.add(new_venue)
                    selected_poll.participants.add(request.user)
                    return redirect('home')
                
            else:
                messages.error(request, "Please make sure you fill out all the fields properly.")

    context ={'form':form, 'poll':selected_poll}
    return render(request, 'base/create-move.html', context)

@login_required(login_url='login')
def addVote(request,pk):
    
    option = Option.objects.get(id=pk)
    print(option.poll.participants.all())
    if request.user in option.poll.participants.all():
        
        messages.error(request, "You have already voted.")
        return redirect('home')
    else:
        option.poll.participants.add(request.user) 
        option.votes += 1
        option.user_votes.add(request.user)
        option.save()
        return redirect('home')


@login_required(login_url='login')
def createPoll(request):
    try:
        current_poll = Poll.objects.get(active=True)
        current_poll.active = False
        current_poll.save()
    except Poll.DoesNotExist:
        pass    
    
    Poll.objects.create(
        area="new york"
    )
    return redirect('home')


def loginUser(request):
    page = 'login'
    if request.method  == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist.")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is incorrect.')

    context = {'page':page}
    return render(request, 'base/login.html', context)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('home')


def registerUser(request):
    form = MyUserCreationForm()
    
    if request.method=="POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occurred during registering.")
    return render(request, 'base/login.html', {"form":form})