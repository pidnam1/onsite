from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, render
from requests import session

from service.forms import CompanySignUpForm1, CompanySignUpForm2, ManufacturerSignUpForm2, ManufacturerSignUpForm1, \
    ProductCreationForm, EditedProductForm, AddressForm, ProductsForCheckoutQuantityForm, ProjectForm, CompanyProfileForm, \
    ManufacturerProfileForm


from service.models import Profile, PRODUCT_CHOICES, Product, Cart, ProductsForCheckout, Project
from django.contrib.auth.models import User
from django import template
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import User
from .decorators import user_is_company, user_is_manufacturer
'''Views page, most view names are self explanatory, others are commented in. Also if the functions within the views are
complicated(query page) that is also commented in.'''

###Home page
def index(request):


    if request.user.is_superuser:
        return redirect('/admin')
    if request.user.is_authenticated:
        loggedProfile = Profile.objects.get(user=request.user)
        if loggedProfile.bio != "":
            return redirect('/service/detail/')
        else:
            return redirect('/signup/companycont/')
    else:
        return render(request, 'service/home.html')


## Signup Choice Page
def signup(request):

    if request.user.is_authenticated and request.user.profile.is_manufacturer:
        return redirect('/service/manufacturerhome/')
    else:
        return render(request, 'service/signupchoice.html')

## Services info page
def services_info(request):

    return render(request, 'service/services_info.html')

## Services info page
def services_vendor_matching(request):

    return render(request, 'service/services_vendor_matching.html')

def services_project_management(request):

    return render(request, 'service/services_project_management.html')

def services_record_keeping(request):

    return render(request, 'service/services_record_keeping.html')

def services_consulting(request):

    return render(request, 'service/services_consulting.html')

## First Company Signup Page
def company_signup1(request):
    if request.user.is_authenticated and request.user.profile.is_company:
        return redirect('/service/companyhome/')

    if request.method == 'POST':
        form = CompanySignUpForm1(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()

            ## Create Profile instance
            user.refresh_from_db()

            user.profile.is_company = True
            user.profile.business_name = form.cleaned_data.get('business_name')

            ##Creates cart
            cart = Cart(profile = user.profile)
            cart.save()


            user.profile.save()
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            return redirect('/signup/companycont')
    else:
        form = CompanySignUpForm1()
    return render(request, 'service/new_sign_up.html', {'form': form})

## Second Company Sign Up Page
def company_signup2(request):
    loggedProfile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = CompanySignUpForm2(request.POST)
        if form.is_valid():
            loggedProfile.bio = form.cleaned_data.get('bio')
            loggedProfile.address = form.cleaned_data.get('address')
            loggedProfile.is_complete_signup = True
            loggedProfile.save()
            return redirect('/service/detail/')
    else:
        form = CompanySignUpForm2
    return render(request, 'service/CompanySignUp2.html',{'form': form, 'profile': loggedProfile} )

## First Manufacturer Sign Up Page
def manufacturer_signup1(request):
    if request.method == 'POST':
        form = ManufacturerSignUpForm1(request.POST)

        if form.is_valid():
            user = form.save()

            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.is_manufacturer = True
            user.profile.business_name = form.cleaned_data.get('business_name')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/signup/manufacturercont/')
    else:
        form = ManufacturerSignUpForm1()
    return render(request, 'service/ManufacturerSignUp.html', {'form': form})

### Second manufacturer Signup Page
@login_required
def manufacturer_signup2(request):
    loggedProfile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ManufacturerSignUpForm2(request.POST)
        if form.is_valid():

            loggedProfile.bio = form.cleaned_data.get('bio')
            loggedProfile.region = form.cleaned_data.get('region')
            loggedProfile.address = form.cleaned_data.get('address')
            loggedProfile.is_complete_signup = True

            loggedProfile.save()
            return redirect('/service/detail/')
    else:
        form = ManufacturerSignUpForm2
    return render(request, 'service/ManufacturerSignUp2.html', {'form': form})

### Home page for company, manufacturer, or not signed in. Checks for each case and redirects
@login_required
@user_passes_test(lambda u: u.profile.bio != "", login_url = '/signup/companycont/')
def detail(request):
    loggedProfile = Profile.objects.get(user = request.user)
    if loggedProfile.is_company and loggedProfile.bio is None:
        return redirect('signup/companycont/')
    if loggedProfile.is_company:
        return render(request, 'service/LoggedInHomeCompany.html', {"profile" : loggedProfile})

    if loggedProfile.is_manufacturer:
        return render(request, 'service/LoggedInHomeManufacturer.html', {"profile": loggedProfile})
    else:
        return render(request, 'service/home.html')

##Profile page, check if user is manufacturer or is company and bases it on that
@login_required
@user_passes_test(lambda u: u.profile.bio != "", login_url = '/signup/companycont/')
def myProfile(request):

    #### CHECK IF USER IS COMPANY OR IS MANUFACTURER AND RENDER FORM BASED ON THAT
    loggedProfile = Profile.objects.get(user=request.user)
    test = False
    if request.method == 'POST':

        form = ManufacturerProfileForm(request.POST)

        if form.is_valid():
            loggedProfile.business_name = form.cleaned_data.get('business_name')
            loggedProfile.address = form.cleaned_data.get('address')
            request.user.email = form.cleaned_data.get('email')
            loggedProfile.region = form.cleaned_data.get('region')
            loggedProfile.save()
            return redirect('/service/detail/')


    else:
        form = ManufacturerProfileForm(initial={'email' : request.user.email, 'business_name': loggedProfile.business_name,
                                           'address' : loggedProfile.address, 'region': loggedProfile.region, 'bio':loggedProfile.bio
                                            })

    return render(request, 'service/MyProfile.html', {"profile": loggedProfile, 'form': form})

###Projects Page, with list of all projects
@login_required
@user_passes_test(lambda u: u.profile.bio != "", login_url = '/signup/companycont/')
def projects(request):
    loggedProfile = Profile.objects.get(user=request.user)

    ### Retrieves all active projects for Profile
    activeProjects = loggedProfile.project_set.filter(profile = loggedProfile)



    return render(request, 'service/Projects.html', {"profile": loggedProfile, 'projects': activeProjects})


### Add new project page
@login_required
@user_passes_test(lambda u: u.profile.bio != "", login_url = '/signup/companycont/')
def addNewProject(request):
    loggedProfile = Profile.objects.get(user=request.user)
    projects = loggedProfile.project_set.filter(profile=loggedProfile)
    error_message = ''
    projectnames = []
    product_list = ["Bitumen", "Cement", "Steel", "Admixture", "Plywood", "Tin", "Paint", "Machinery"]

    for proj in projects:
        projectnames.append(proj.name)

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid() and form.cleaned_data.get('name') not in projectnames:
            newProject = Project(profile=loggedProfile)
            newProject.address = form.cleaned_data.get('address')
            newProject.name = form.cleaned_data.get('name')
            newProject.budget = form.cleaned_data.get('budget')
            newProject.client = form.cleaned_data.get('client')
            newProject.length = form.cleaned_data.get('length')
            newProject.deadline = form.cleaned_data.get('deadline')
            newProject.comments = form.cleaned_data.get('comments')
            #newProject.deadline = form.cleaned_data.get('deadline')

            #newProject.nearest_landmark = form.cleaned_data.get('nearest_landmark')
            newProject.save()
            loggedProfile.save()
            return redirect('/service/projects/')
        if form.is_valid() and form.cleaned_data.get('name') in projectnames:
            error_message = "You already have a project with this name"
    else:
        form = ProjectForm

    return render(request, 'service/AddNewProject.html', {'form': form, 'error_message': error_message, 'products': product_list})
@login_required
@user_passes_test(lambda u: u.profile.bio != "", login_url = '/signup/companycont/')
def orders(request):
    loggedProfile = Profile.objects.get(user=request.user)

    return render(request, 'service/Orders.html', {"profile": loggedProfile})
@login_required
@user_passes_test(lambda u: u.profile.bio != "", login_url = '/signup/companycont/')
def payments(request):
    loggedProfile = Profile.objects.get(user=request.user)

    return render(request, 'service/Payments.html', {"profile": loggedProfile})

@login_required
@user_passes_test(lambda u: u.profile.bio != "", login_url = '/signup/companycont/')
def records(request):
    loggedProfile = Profile.objects.get(user = request.user)

    return render(request, 'service/Records.html', {"profile": loggedProfile})
@login_required
@user_passes_test(lambda u: u.profile.bio != "", login_url = '/signup/companycont/')
def products(request):
    loggedProfile = Profile.objects.get(user=request.user)
    products = loggedProfile.product_set.all()
    form = EditedProductForm()
    product_list = ["Bitumen", "Cement", "Steel", "Admixture", "Plywood", "Tin", "Paint", "Machinery"]
    if request.method == 'POST':
        form = EditedProductForm(request.POST)
        if form.is_valid():
            editedproduct = form.save(commit=False)
            for product in product_list:
                if product in request.POST:
                 editedproduct.name = product
                 editedproduct.profile = loggedProfile
                 editedproduct.save()
                 return redirect('/service/products/edit')
    else:
        form = EditedProductForm
    return render(request, 'service/Products.html', {"profile": loggedProfile, 'products': products, 'form': form})
@login_required
@user_passes_test(lambda u: u.profile.bio != "", login_url = '/signup/companycont/')
def product_creation(request):
    loggedProfile = Profile.objects.get(user=request.user)
    error_message = ''
    if request.method == 'POST':
        form = ProductCreationForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            try:
                checkProd = loggedProfile.product_set.get(name = form.cleaned_data.get('name'))
                error_message = "You cannot create a new instance of a product you already are listing."
                return render(request, 'service/ProductCreation.html', {"profile": loggedProfile, 'form': form, 'error': error_message})
            except Product.DoesNotExist:

                product.name = form.cleaned_data.get('name')
                product.price = form.cleaned_data.get('price')
                product.quantityAvailable = form.cleaned_data.get('quantity_available')
                product.availability = form.cleaned_data.get('availability')
                product.description = form.cleaned_data.get('description')
                product.profile = loggedProfile
                product.save()
                return redirect('/service/products/')
    else:
        form = ProductCreationForm
    return render(request, 'service/ProductCreation.html', {"profile": loggedProfile, 'form': form})
@login_required
@user_passes_test(lambda u: u.profile.bio != "", login_url = '/signup/companycont/')
def order(request):
    loggedProfile = Profile.objects.get(user=request.user)
    projects = loggedProfile.project_set.filter(profile = loggedProfile)
    projnames = []
    for proj in projects:
        projnames.append(proj.name)


    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            for name in projnames:
                if name in request.POST:
                    projname = name
                    request.session['address_id'] = projname
                    return redirect('/service/order/withaddress')
            else:
                address = form.cleaned_data.get('enter_site_address')
                request.session['address_id'] = address
                return redirect('/service/order/withaddress')

    else:
        form = AddressForm
    return render(request, 'service/Order.html', {"profile": loggedProfile,'projects': projects, 'form': form})

### order_queried query function can be edited to be more efficient
@login_required
@user_passes_test(lambda u: u.profile.bio != "", login_url = '/signup/companycont/')
def order_queried(request):
    loggedProfile = Profile.objects.get(user=request.user)
    profiles = Profile.objects.filter(is_manufacturer = True)
    searched_products = []
    test_sub2 = ["OPC 43", "PPC", "PSC"]
    test_sub1 = ["Test1", "Test2", "Test3"]
    product_list = ["Bitumen", "Cement", "Steel", "Admixture", "Plywood", "Tin", "Paint", "Machinery"]

    projects = loggedProfile.project_set.filter(profile = loggedProfile)

    address = request.session.get('address_id')
    for proj in projects:
        if address == proj.name:
            address = proj.address


    if request.method == 'POST':
        form = EditedProductForm(request.POST)
        if form.is_valid():
            for product in product_list:
                if product in request.POST:
                 search_product = product
                 request.session['search_product'] = search_product
                 return redirect('/service/order/withaddress/results')
    else:
        form = EditedProductForm
    ### Loops through the products that are checked on previous form to see which need to be searched
    ### Then goes through each product and all the manufacturers, and finds the one with cheapest price.
    ### Going to have to edit once we get in delivery fees and location

    return render(request, 'service/OrderWithAddress.html', {"profile": loggedProfile, 'products': product_list, 'address':
                                                              address, 'form': form})
@login_required
def product_edit(request):
    loggedProfile = Profile.objects.get(user=request.user)
    editedproduct = loggedProfile.editedproduct_set.last()
    product = loggedProfile.product_set.get(name = editedproduct.name)
    error_message = ''
    if request.method == 'POST':
        form = ProductCreationForm(request.POST)
        if "delete" in request.POST:
            product.delete()
            return redirect('/service/products/')
        if form.is_valid() and form.cleaned_data.get('name') == product.name:
            product.price = form.cleaned_data.get('price')
            product.quantityAvailable = form.cleaned_data.get('quantity_available')
            product.availability = form.cleaned_data.get('availability')
            product.description = form.cleaned_data.get('description')
            product.profile = loggedProfile
            product.save()
            return redirect('/service/products/')
        if form.is_valid() and form.cleaned_data.get('name') != product.name:
            error_message = "You cannot change the name of a product"
    else:

        form = ProductCreationForm(initial={'name': product.name, 'price' : product.price, 'quantity_available': product.quantityAvailable
                                            ,'availability': product.availability, 'description': product.description
                                            })

    return render(request, 'service/ProductEdit.html', {"profile": loggedProfile, 'form': form, 'product': product, 'error': error_message})
@login_required
@user_passes_test(lambda u: u.profile.bio != "", login_url = '/signup/companycont/')
def cart(request):
    loggedProfile = Profile.objects.get(user=request.user)
    cart = loggedProfile.cart_set.get(profile = loggedProfile)
    products_for_checkout = cart.productsforcheckout_set.all()
    totals = []
    for product in products_for_checkout:
        totals.append(product.quantity * product.price)
    full_list = zip(products_for_checkout, totals)
    return render(request, 'service/Cart.html', {"profile": loggedProfile, 'full_list': full_list})
@login_required
@user_passes_test(lambda u: u.profile.bio != "", login_url = '/signup/companycont/')
def search_results(request):

    #Loading results onto page
    loggedProfile = Profile.objects.get(user=request.user)
    search_product = request.session.get('search_product')




    cart = loggedProfile.cart_set.get(profile = loggedProfile)
    cheapest_products = []
    profiles = Profile.objects.filter(is_manufacturer = True)
    add_to_cart_business = ""
    cheapest_product = Product(price = 10000000)


    for profile in profiles:
        try:
            current_product = profile.product_set.get(name=search_product)
            cheapest_products.append(current_product)
            ###if current_product.price < cheapest_product.price:
               ### cheapest_product = current_product

        except Product.DoesNotExist:
            continue

    cheapest_products.sort(key=lambda x: x.price, reverse = False)

    #Handling request forms
    if request.method == 'POST':
        form = ProductsForCheckoutQuantityForm(request.POST)
        if form.is_valid():
            quantity = 0
            quantity = form.cleaned_data.get('quantity')
            add_to_cart_business = request.POST.get('name')
            selected_manufacturer_profile = Profile.objects.get(business_name = add_to_cart_business)
            selected_product = Product.objects.get(name = current_product.name, profile = selected_manufacturer_profile)
            checkout_product = ProductsForCheckout(profile = loggedProfile, cart = cart, name = selected_product.name, price = selected_product.price,
                                               description = selected_product.description, business_name = add_to_cart_business, quantity = quantity)
            loggedProfile.cart_amount += 1
            checkout_product.save()
            loggedProfile.save()
            form.clean()
            return redirect('/service/order/withaddress/results')
    else:
        form = ProductsForCheckoutQuantityForm

    return render(request, 'service/SearchResults.html', {'profile': loggedProfile, 'cheapest_products': cheapest_products, 'search_product':
                                                          search_product, 'form': form,
                                                          })



def testVideo(request):
    return render(request, 'service/testvideo.html')

def testHome(request):
    return render(request, 'service/Bootslander/index.html')


