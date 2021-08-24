from django.views.generic import View, TemplateView, CreateView, FormView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import UserRegistrationForm, UserLoginForm
from django.urls import reverse_lazy

# Create your views here.
def home(request):
    return render(request, 'main_app/home.html')


def women(request):
    context = {
        "items": Product.objects.filter(category=1)
    }
    return render(request, 'main_app/women.html', context)


def men(request):
    context = {
        "items": Product.objects.filter(category=2)
    }
    return render(request, 'main_app/men.html', context)


def kids(request):
    context = {
        'kiditem': Product.objects.filter(category=3)
    }
    return render(request, 'main_app/kids.html', context)


def cart(request):
    return render(request, 'main_app/cart.html')


def subitem(request):
    context = {
        'products': Product.objects.all(),
        'categories': SubCategory.objects.all(),
        'item': Product.objects.filter(category=1, sub_category_id=1)
    }
    return render(request, 'main_app/subitem.html', context)



def all_products(request):
    context = {
        'products': Product.objects.all(),
    }
    return render(request, 'main_app/all_products.html', context)


class ProductDetailView(TemplateView):
    template_name = "main_app/productdetail.html"

    # dynamic content is not present, we have to send it from our backend

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        product = Product.objects.get(slug=url_slug)
        context = {
            'product': product,
        }
        return context


class UserRegistrationView(CreateView):
    template_name = "main_app/registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username, email, password)
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("home")


class UserLoginView(FormView):
    template_name = "main_app/userlogin.html"
    form_class = UserLoginForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data.get("password")
        usr = authenticate(username=uname, password=pword)
        if usr is not None and usr.customer:
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class,
                                                             "error": "This user doesn't exist"})
        return super().form_valid(form)

"""

Adding search 

def new_search(request):
    search = request.POST.get("search")
    print(search)
    return render(request, 'main_app/home.html')
"""



def womencateg(request, data=None):
    if data == None:
        winter = Product.objects.all(category="Women")
    elif data == 'winters-clothing' or 'summer-wear' or 'footwear' or 'accessories' or 'pyjamas':
        winter = Product.objects.filter(category__title="Women", sub_category__slug=data)
    return render(request, 'main_app/winteritems.html', {'winter': winter})

def mencateg(request, data=None):
    if data == None:
        mencat = Product.objects.all(category="Men")
    elif data == 'winters-clothing' or 'summer-wear' or 'footwear' or 'accessories' or 'pyjamas':
        mencat = Product.objects.filter(category__title="Men", sub_category__slug=data)
    return render(request, 'main_app/winteritems.html', {'mencat': mencat})

def kidcateg(request, data=None):
    if data == None:
        kidcat = Product.objects.all(category="Kids")
    elif data == 'winters-clothing' or 'summer-wear' or 'footwear' or 'accessories' or 'pyjamas':
        kidcat = Product.objects.filter(category__title="Kids", sub_category__slug=data)
    return render(request, 'main_app/winteritems.html', {'kidcat': kidcat})

"""
def subcat(request, data=None):
    if data == None:
        winter = Product.objects.all(category="Women")
        men = Product.objects.all(category="Men")
    elif data == 'winters-clothing' or 'summer-wear' or 'footwear' or 'accessories' or 'pyjamas':
        winter = Product.objects.filter(category__title="Women", sub_category__slug=data)
        men = Product.objects.filter(category__title="Men", sub_category__slug=data)
    return render(request, 'main_app/winteritems.html', {'winter': winter, 'men': men})
"""
