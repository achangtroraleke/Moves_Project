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
            total_votes += len(x.user_votes.all())
        
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
                        new_option = Option.objects.create(
                            venue = suggested_option,
                            poll=selected_poll,
                            
                        )
                        new_option.user_votes.add(request.user)
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
                    new_option = Option.objects.create(
                        venue=new_venue,
                        poll=selected_poll
                        
                    )
                    new_option.user_votes.add(request.user)

                    selected_poll.venues.add(new_venue)
                    selected_poll.participants.add(request.user)
                    return redirect('home')
                
            else:
                messages.error(request, "Please make sure you fill out all the fields properly.")

    context ={'form':form, 'poll':selected_poll}
    return render(request, 'base/create-move.html', context)

@login_required(login_url='login')
def searchMove(request, pk):
    venues = Venue.objects.all()
    selected_poll = Poll.objects.get(id=pk)
    if request.method =="POST":
        selected_venue = request.POST.get('venue').lower()

        try:
            found_venue = Venue.objects.get(name = selected_venue)
            if found_venue in selected_poll.venues.all():
                messages.error(request, "This Venue was already suggested for this poll.")
                return redirect('home')
            else:
                Option.objects.create(
                    venue=found_venue,
                    poll=selected_poll
                )
                return redirect('home')
        except Venue.DoesNotExist:
            return redirect('create-move', pk=pk)
    

    context = {'poll':selected_poll, "venues":venues}
    return render(request, 'base/search-move.html', context)

@login_required(login_url='login')
def addVote(request,pk):
    
    option = Option.objects.get(id=pk)
    print(option.poll.participants.all())
    if request.user in option.poll.participants.all():
        for all_options in option.poll.option_set.all():
            if request.user in all_options.user_votes.all():
                all_options.user_votes.remove(request.user)
                all_options.votes -= 1
                all_options.save()
        option.user_votes.add(request.user)
        option.votes +=1
        option.save()
       
      
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
            user = User.objects.get(email=username)
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
            messages.error(request, 'An error occurred during registering.\nPlease make sure your password contains:\nUppercase,\nLowercase,\nSpecial characters,\nA number.')
    return render(request, 'base/login.html', {"form":form})
