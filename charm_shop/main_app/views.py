from django.views.generic import View, TemplateView, CreateView, FormView, DetailView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import UserRegistrationForm, UserLoginForm, CheckoutForm
from django.urls import reverse_lazy
from django.db.models import Q


class AssignCustomer(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            if request.user.is_authenticated and request.user.customer:
                cart_obj.customer = request.user.customer
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)


def home_page(request):
    return render(request, 'main_app/home.html')


def women_category(request):
    context = {
        "items": Product.objects.filter(category=1)
    }
    return render(request, 'main_app/women.html', context)


def men_category(request):
    context = {
        "items": Product.objects.filter(category=2)
    }
    return render(request, 'main_app/men.html', context)


def kids_category(request):
    context = {
        'kiditem': Product.objects.filter(category=3)
    }
    return render(request, 'main_app/kids.html', context)


def sub_items(request):
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


class ProductDetailView(AssignCustomer, TemplateView):
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


class SearchView(AssignCustomer, TemplateView):
    template_name = 'main_app/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET['keyword']
        results = Product.objects.filter(Q(title__icontains=kw) | Q(description__icontains=kw))
        context['results'] = results
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

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("home")


class UserLoginView(FormView):
    template_name = "main_app/user_login.html"
    form_class = UserLoginForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user_name = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=user_name, password=password)
        if user is not None and user.customer:
            login(self.request, user)
        else:
            return render(self.request, self.template_name, {"form": self.form_class,
                                                             "error": "This user doesn't exist"})
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url


class AddToCartView(AssignCustomer, TemplateView):
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


class ManageCartView(AssignCustomer, View):
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


class MyCartView(AssignCustomer, TemplateView):
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


class CheckoutView(AssignCustomer, CreateView):
    template_name = "main_app/checkout.html"
    form_class = CheckoutForm
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.customer:
            pass
        else:
            return redirect("/login/?next=/checkout/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.total = cart_obj.total
            form.instance.order_status = "Order Received"
            del self.request.session['cart_id']
        else:
            return redirect("home")
        return super().form_valid(form)


def womencateg(request, data=None):
    winter = []
    #category_name = ["Women", "Men", "Kids"]
    if data is None:
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


class UserProfileView(AssignCustomer, TemplateView):
    template_name = 'main_app/user_profile.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.customer:
            pass
        else:
            return redirect("/login/?next=/checkout/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        context['customer'] = customer
        orders = Order.objects.filter(cart__customer=customer)
        context['orders'] = orders
        return context


class CustomerOrderDetailView(DetailView):
    template_name = 'main_app/customer_order_detail.html'
    model = Order
    context_object_name = 'ord_obj'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.customer:
            pass
        else:
            return redirect("/login/?next=/checkout/")
        return super().dispatch(request, *args, **kwargs)

