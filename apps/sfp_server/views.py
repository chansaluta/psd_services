from django.shortcuts import render

# Create your views here.

def index(request):
    template = "sfp/index.html"

    return render(request, template)