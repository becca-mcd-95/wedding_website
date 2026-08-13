from django.shortcuts import render

def index(request):
    return HttpResponse("Welcome to our wedding website")