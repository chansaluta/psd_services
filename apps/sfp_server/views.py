from django.shortcuts import render

# Create your views here.

def index(request):
    template = "sfp/index.html"

    return render(request, template)

def dashboard(request):
    template = "sfp/pages/dashboard.html"

    return render(request, template)

def nut_status_add_data(request):
    template = "sfp/pages/status_tool.html"

    return render(request, template)

# ? Children Status List


def moderately_wasted_children(request):
    template = "sfp/pages/status_list/moderately_wasted.html"

    return render(request, template)


def severely_stunted_children(request):
    template = "sfp/pages/status_list/severely_stunted.html"

    return render(request, template)


def severely_underweight_children(request):
    template = "sfp/pages/status_list/severely_underweight.html"

    return render(request, template)


def severely_wasted_children(request):
    template = "sfp/pages/status_list/severely_wasted.html"

    return render(request, template)


def stunted_children(request):
    template = "sfp/pages/status_list/stunted.html"

    return render(request, template)


def underweight_children(request):
    template = "sfp/pages/status_list/underweight.html"

    return render(request, template)


def summary(request):
    template = "sfp/pages/summary.html"

    return render(request, template)