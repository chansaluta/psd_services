from django.shortcuts import render

# Create your views here.

def index(request):
    template = "rrptp/index.html"

    return render(request, template)


def dashboard(request):
    template = "rrptp/pages/dashboard.html"

    return render(request, template)