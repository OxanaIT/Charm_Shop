from django.db import models
from django.contrib.auth.models import User


# creating Customer model with user that is one to one one user one cart one page. + import from
# django auth.model - User. name, address + when created the account
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    # address = models.CharField(max_length=200, null=True, blank=True)
    joined_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


# creating category model with title and slug as unique
class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"


class SubCategory(models.Model):
    title = models.CharField(max_length=200, null=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "SubCategories"


# creating Product model with info about each product. slug like url unique.
class Product(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField()
    return_policy = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField()
    image = models.CharField(max_length=1000, null=False, default='Picture not available')

    def __str__(self):
        return self.title


class VariationManager(models.Manager):
    def all(self):
        return super(VariationManager, self).filter(active=True)

    def sizes(self):
        return self.all().filter(category='size')

    def colors(self):
        return self.all().filter(category='color')


VAR_CATEGORIES = (
    ('size', 'size'),
    ('color', 'color'),
    )


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.CharField(max_length=120, choices=VAR_CATEGORIES, default='size')
    title = models.CharField(max_length=120)
    active = models.BooleanField(default=True)

    objects = VariationManager()

    def __str__(self):
        return self.title


# creating cart model with connection with Customer model, + total items in cart + when added
class Cart(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.FloatField(default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    # returning id of cart
    def __str__(self):
        return "Cart: " + str(self.id)


# create cart product - this is shown inside cart
class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.FloatField(default=0.00)
    quantity = models.PositiveIntegerField()
    subtotal = models.FloatField(default=0.00)

    def __str__(self):
        return "Cart: " + str(self.cart.id) + "CartProduct: " + str(self.id)


ORDER_STATUS = {
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("On the way", "On the way"),
    ("Order Completed", "Order Completed"),
    ("Order Canceled", "Order Canceled"),
}


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    ordered_by = models.CharField(max_length=200)
    shipping_address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(null=True, blank=True)
    subtotal = models.FloatField(default=0.00)
    total = models.FloatField(default=0.00)
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Order: " + str(self.id)
