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



class AddToCartView(TemplateView):
    template_name = "main_app/addtocart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get product id from requested url
        product_id = self.kwargs['pro_id']
        # get product
        product_obj = Product.objects.get(id=product_id)
        # check if cart exists
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(product=product_obj)

            # items already exists in cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.price
                cartproduct.save()
                cart_obj.total += product_obj.price
                cart_obj.save()
            # new item is added in cart
            else:
                cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj,
                                                         rate=product_obj.price, quantity=1,
                                                         subtotal=product_obj.price)
                cart_obj.total += product_obj.price
                cart_obj.save()
        # if cart does not exist
        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj,
                                                     rate=product_obj.price, quantity=1,
                                                     subtotal=product_obj.price)
            cart_obj.total += product_obj.price
            cart_obj.save()

        return context



class ManageCartView(View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart

        # when user inc the item - inc quantity, subtotal, cart value
        if action == "inc":
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()

        # when user dcr the item - dcr quantity, subtotal, cart value
        elif action == "dcr":
                cp_obj.quantity -= 1
                cp_obj.subtotal -= cp_obj.rate
                cp_obj.save()
                cart_obj.total -= cp_obj.rate
                cart_obj.save()
                if cp_obj.quantity == 0:
                    cp_obj.delete()

        # remove the item subtotal value from total. Delete cart product obj
        elif action == "rmv":
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect("mycart")


class MyCartView(TemplateView):
    template_name = "main_app/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        # if exists
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context


def checkout(request):
    return render(request, "main_app/checkout.html")


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
