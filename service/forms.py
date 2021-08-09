from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Product, EditedProduct, ProductsForCheckout, Profile, Project
from django.forms import ModelForm, Field
from django.forms.widgets import NumberInput


class CompanySignUpForm1(UserCreationForm):
    business_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=254)



    class Meta:
        model = User
        fields = ('username', 'business_name', 'email',  'password1', 'password2')

class CompanySignUpForm2(ModelForm):
    address = forms.CharField(max_length=100, required=True, help_text='State in which business operates')
    region = forms.CharField(max_length=100, required=True, help_text='State in which business operates')
    bio = forms.CharField(max_length=2000, required=True, help_text='Description of company')


    class Meta:
        model = Profile
        fields = ('address','region', 'bio' )

class CompanyProfileForm(ModelForm):
    business_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=254)
    address = forms.CharField(max_length=100, required=True, help_text='State in which business operates')
    bio = forms.CharField(max_length=2000, required=True, help_text='Description of company')
    class Meta:
        model = User
        fields = ('business_name', 'email', 'address', 'bio')

class ManufacturerProfileForm(ModelForm):
    business_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    region = forms.CharField(max_length=100, required=True, help_text='State in which business operates')
    address = forms.CharField(max_length=100, required=True, help_text='State in which business operates')
    bio = forms.CharField(max_length=2000, required=True, help_text='Description of company')

    class Meta:
        model = User
        fields = ('business_name', 'email', 'region', 'address', 'bio')


class ManufacturerSignUpForm1(UserCreationForm):
    business_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')



    class Meta:
        model = User
        fields = ('username', 'business_name', 'email','password1', 'password2')

class ManufacturerSignUpForm2(ModelForm):
    region = forms.CharField(max_length=100, required=True, help_text='State in which business operates')
    address = forms.CharField(max_length=100, required=True, help_text='State in which business operates')
    bio = forms.CharField(max_length=2000, required=True, help_text='Description of company')


    class Meta:
        model = Profile
        fields = ( 'region', 'address', 'bio')

PRODUCT_CHOICES = (('Bitumen', 'Bitumen'), ('Cement','Cement'), ('Steel','Steel'), ('Admixture','Admixture'), ('Plywood','Plywood'),
                   ('Tin','Tin'), ('Paint','Paint'), ('Machinery','Machinery'))
PRODUCTS = []
for product in PRODUCT_CHOICES:
    PRODUCTS.append(product[0])
AVAILABILITY_CHOICES = (
    (True, 'Available'),
    (False, 'Not Available')
)

class ProjectForm(ModelForm):
    name = forms.CharField(max_length=40, required=True, label="Name")
    address = forms.CharField(max_length=40, required=True, label="Address")
    nearest_landmark = forms.CharField(max_length=40, required=True, label="Nearest Landmark")
    length = forms.IntegerField(max_value=None,min_value=0, label="Length(km)")
    client = forms.CharField(max_length=40, required=True, label="Client")
    budget = forms.IntegerField(max_value=None,min_value=0, label="Budget")
    materials = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=PRODUCT_CHOICES, )
    deadline = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    comments = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))

    class Meta:
        model = Project
        fields = ('name', 'address', 'nearest_landmark', 'length', 'client', 'budget', 'materials', 'deadline', 'comments')





class ProductCreationForm(ModelForm):
    name = forms.ChoiceField(choices=PRODUCT_CHOICES, required=True)
    price = forms.DecimalField(decimal_places=2, max_digits=10, min_value=0)
    quantity_available = forms.IntegerField(max_value=None,min_value=1)
    availability = forms.ChoiceField(choices=AVAILABILITY_CHOICES)
    description = forms.CharField(max_length=50, required=False, help_text='Short Description')
    class Meta:
        model = Product
        fields = ('name', 'price', 'quantity_available', 'availability', 'description')
class EditedProductForm(ModelForm):
    name = forms.CharField(max_length=20, required=False)
    class Meta:
        model = EditedProduct
        fields = ('name',)

class AddressForm(forms.Form):
    enter_site_address = forms.CharField(max_length= 50, required= False)
class ProductsForCheckoutQuantityForm(ModelForm):
    quantity = forms.IntegerField(min_value=1)
    class Meta:
        model = ProductsForCheckout
        fields = ('quantity', )

class EditedCheckoutForm(ModelForm):
    ###reference: https://jacobian.org/2010/feb/28/dynamic-form-generation/
    pass






