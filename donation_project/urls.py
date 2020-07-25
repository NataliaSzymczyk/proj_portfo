"""donation_project URL Configuration

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
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from charity_donation.views import *
from django.contrib.auth import views as auth_views
from charity_donation.forms import MyCustomResetForm

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', LandingPage.as_view(), name='index'),
    path('add-donation/', AddDonation.as_view(), name='add-donation'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('user-profile/', UserProfile.as_view(), name='user-profile'),
    path('user-edit/', EditUser.as_view(), name='user-edit'),
    path('user-password/', UserPassword.as_view(), name='user-password'),
    path('user-donations/', UserDonations.as_view(), name='user-donations'),
    path('confirmation/', FormConfirmation.as_view(), name='confirmation'),



    # path('password_change/done/',
    #      auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
    #      name='password_change_done'),
    #
    # path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
    #      name='password_change'),

    path('password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html', form_class=MyCustomResetForm), name='password_reset'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
]
