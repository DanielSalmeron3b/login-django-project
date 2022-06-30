from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    return render(request, 'authentication/index.html')


def signup(request):

    if request.method == 'POST':

        # Saving all the user information from the form in variables
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        # If the user already exists in the database then him/her
        # will not be able to create an acoount with the same username

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists, please try other username')
            return redirect('home')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists, please try other email')
            return redirect('home')

        # If the username is too long...
        if len(username) > 14:
            messages.error(request, 'Username too long, it must be under 14 characters')

        # If the username didn't match the password...
        if password != confirm:
            messages.error(request, 'Password mismatch, please try again')

        # If the username is not alphanumeric...
        if not username.isalnum():
            messages.error(request, 'Username must be alphanumeric, please try again')
            return redirect('home')

        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname

        # Saving the user in the database
        myuser.save()

        # Showing a message to the user
        messages.success(request, "Your account was created successfully.")

        # Redirecting the user to the login page
        return redirect('/signin')

    return render(request, 'authentication/signup.html')


def signin(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authentication of the user to see if is the same as in the database
        user = authenticate(username=username, password=password)

        # If the user gave their correct credentials...
        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, 'authentication/index.html', {
                # This dict is to show a message with the first name of the user in the index.html
                'fname': fname
            } )
        # If the user DID NOT give their correct credentials...
        else:
            messages.error(request, "Bad Creadentials!")
            return redirect('home')

    return render(request, 'authentication/signin.html')


def signout(request):
    logout(request)
    messages.success(request, 'Logged Out Successfully!')
    return redirect('home')
