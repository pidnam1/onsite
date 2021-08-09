from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from datetime import date



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.TextField(max_length=500, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    region = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length = 40, blank = True)
    is_complete_signup = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)
    is_manufacturer = models.BooleanField(default=False)
    cart_amount = models.IntegerField(default=0)




    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)


    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        if instance.is_superuser:
            pass
        else:
            instance.profile.save()


    def __str__(self):
        return self.user.username




PRODUCT_CHOICES = (('Bitumen', 'Bitumen'), ('Cement','Cement'), ('Steel','Steel'), ('Admixture','Admixture'), ('Plywood','Plywood'),
                   ('Tin','Tin'), ('Paint','Paint'), ('Machinery','Machinery'))



class Product(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=10, choices=PRODUCT_CHOICES, default=None)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    quantityAvailable = models.IntegerField(default=0)
    availability = models.BooleanField(default=True)
    description = models.CharField(max_length=100, blank=True)

class EditedProduct(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length =20, default = None)

class Cart(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None)

class ProductsForCheckout(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=10, choices=PRODUCT_CHOICES, default=None)
    business_name = models.CharField(max_length = 50, default=None)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.CharField(max_length=100, blank=True)
    quantity = models.PositiveIntegerField(default=0)
class Project(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length = 40, blank = True)
    address = models.CharField(max_length = 40, blank = True)
    nearest_landmark = models.CharField(max_length = 40, blank = True)
    length = models.PositiveIntegerField(default=0)
    client = models.CharField(max_length = 40, blank = True)
    budget =  models.IntegerField(default=0)
    deadline = models.DateField(default=date.today, blank = True)
    comments = models.CharField(max_length = 200, blank = True)
    #materials = models.MultipleChoiceField(blank = True)

class Order(models.Model):
    order_id = models.PositiveIntegerField(default=0)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=None)
    business_bought_from = models.CharField(max_length = 50, blank = True)
    date_bought = models.DateField(auto_now=True)
    product = models.CharField(max_length = 50, blank = True)
    total_cost = models.PositiveIntegerField(default=0)
    address_of_site = models.CharField(max_length = 50, blank = True)
    address_of_business_bought_from = models.CharField(max_length = 50, blank = True)
    quantity_ordered = models.PositiveIntegerField(default=0)
    price_per_quantity = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length = 50, blank = True)





