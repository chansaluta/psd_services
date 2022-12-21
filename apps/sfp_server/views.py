from django.shortcuts import render

# Create your views here.

def index(request):
    template = "sfp/index.html"

    return render(request, template)

def dashboard(request):
    template = "sfp/pages/dashboard.html"

    return render(request, template)