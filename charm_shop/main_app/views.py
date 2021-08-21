from django.shortcuts import render
from .models import *
from django.views.generic import TemplateView

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

"""
def new_search(request):
    search = request.POST.get("search")
    print(search)
    return render(request, 'main_app/home.html')
"""