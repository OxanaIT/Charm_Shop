from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'main_app/home.html')


def women(request):
    return render(request, 'main_app/women.html')


def men(request):
    return render(request, 'main_app/men.html')


def kids(request):
    return render(request, 'main_app/kids.html')


def cart(request):
    return render(request, 'main_app/cart.html')


def profile(request):
    return render(request, 'main_app/profile.html')

"""
def new_search(request):
    search = request.POST.get("search")
    print(search)
    return render(request, 'main_app/home.html')
"""