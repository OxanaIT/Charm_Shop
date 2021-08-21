from django.views.generic import View, TemplateView, CreateView, FormView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import UserRegistrationForm, UserLoginForm
from django.urls import reverse_lazy

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



def all_products(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'main_app/all_products.html', context)


class ProductDetailView(TemplateView):
    template_name = "main_app/productdetail.html"

    # dynamic content is not present, we have to send it from our backend

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        product = Product.objects.get(slug=url_slug)
        context['product'] = product
        return context


class UserRegistrationView(CreateView):
    template_name = "registration.html"
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
    template_name = "userlogin.html"
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
def new_search(request):
    search = request.POST.get("search")
    print(search)
    return render(request, 'main_app/home.html')
"""