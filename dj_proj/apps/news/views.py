from django.shortcuts import render, redirect, HttpResponse
from django.shortcuts import reverse


def index(request):
    return render(request, 'news/index.html')
