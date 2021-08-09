"""desmatterpage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the includes() function: from django.urls import includes, path
    2. Add a URL to urlpatterns:  path('service/', includes('service.urls'))
"""
from django.urls import include, path
from django.contrib import admin
from service import views as blog_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('service.urls')),

    ### Signup, Log In, and Password Reset
    path('testvideo/', blog_views.testVideo, name='testvideo'),
    path('testhome/', blog_views.testHome, name='testHome'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='service/login.html'),  name = 'login'),
    path('service/detail/',blog_views.detail, name = 'detail'),
    path('signup/', blog_views.signup, name='signup'),
    path('signup/company',blog_views.company_signup1, name = 'company_signup'),
    path('signup/companycont/', blog_views.company_signup2, name = 'company_signup2'),
    path('signup/manufacturer', blog_views.manufacturer_signup1, name = 'manufacturer_signup'),
    path('signup/manufacturercont/', blog_views.manufacturer_signup2, name='manufacturer_signup2'),
    path('reset/',
        auth_views.PasswordResetView.as_view(
        template_name='service/password_reset.html',
        email_template_name='service/password_reset_email.html',
        subject_template_name='service/password_reset_subject.txt'
    ), name = 'password_reset'),
    path('reset/done/',
    auth_views.PasswordResetDoneView.as_view(template_name='service/password_reset_done.html'),
    name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name='service/password_reset_confirm.html'),
    name='password_reset_confirm'),
    path('reset/complete/',
    auth_views.PasswordResetCompleteView.as_view(template_name='service/password_reset_complete.html'),
    name='password_reset_complete'),
    path('settings/password/', auth_views.PasswordChangeView.as_view(template_name='service/password_change.html'),
    name='password_change'),
    path('settings/password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='service/password_change_done.html'),
    name='password_change_done'),

    ### General Logged In Views
    path('service/', blog_views.index, name = 'index'),
    path('service/profile/', blog_views.myProfile, name = 'profile'),
    path('service/orders/', blog_views.orders, name = 'orders'),
    path('service/payments/', blog_views.payments, name = 'payments'),
    ### Companies Home and Views
    path('service/projects/', blog_views.projects, name = 'projects'),
    path('service/order/', blog_views.order, name = 'order'),
    path('service/order/withaddress', blog_views.order_queried, name = 'order_address'),
    path('service/order/withaddress/results',blog_views.search_results, name = 'search_results'),
    path('service/cart/',blog_views.cart, name = 'cart'),
    path('service/addproject/', blog_views.addNewProject, name="add_new_project"),
    ###Manufacturer Home and Views
    path('service/products/', blog_views.products, name = 'products'),
    path('service/products/create/', blog_views.product_creation, name = 'product_creation'),
    path('service/products/edit/', blog_views.product_edit, name = 'product_edit'),
    path('service/records', blog_views.records, name = 'records'),

    #services
    path('service/services_info', blog_views.services_info, name='services_info'),
    path('service/services_vendor_matching', blog_views.services_vendor_matching, name='services_vendor_matching'),
    path('service/services_project_management', blog_views.services_project_management, name='services_project_management'),
    path('service/services_record_keeping', blog_views.services_record_keeping, name='services_record_keeping'),
    path('service/services_consulting', blog_views.services_consulting, name='services_consulting')

]
