from django.shortcuts import render

# Create your views here.
def uploadResume(request):
    return render(request,'resume.html')
def showHomepage(request):
    return render(request,'home.html' )