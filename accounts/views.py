from django.forms import ValidationError
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from .forms import CustomUserCreationForm
def signupaccount(request):
    if request.method == 'GET':
       return render(request, 'signupaccount.html', {'form':CustomUserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['mail'],password=request.POST['password1'],firstName=request.POST['firstName'],lastName=request.POST['lastName'],birth=request.POST['birth'])
                user.save()
                login(request,user)
                return redirect('home')
            except ValidationError:
                return render(request, 'signupaccount.html', {'form':CustomUserCreationForm, 'error':'Fecha con formato incorrecto debe ser YY-MM-DD'})
        else:
            return render(request, 'signupaccount.html', {'form':CustomUserCreationForm, 'error':'Las contraseñas no coinciden'})
        
def logoutaccount(request):
    logout(request)
    return redirect('home')
# Create your views here.

def loginaccount(request):
    if request.method == 'GET':
        return render(request,'loginaccount.html',{'form':AuthenticationForm})
    else:
        user= authenticate(request, mail=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'loginaccount.html',{'form': AuthenticationForm(),'error':'Usuario no encontrado'})
        else:
            login(request,user)
            return redirect('home')