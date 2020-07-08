from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .models import Category, Donation, Institution


from django.db.models import Sum, Count



class LandingPage(View):
    def get(self, request):
        return render(request, 'index.html')


class AddDonation(View):
    def get(self, request):
        return render(request, 'form.html')


class UserProfile(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user-profile.html')


class EditUser(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user-edit.html')
    def post(self, request):
        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        current_user = self.request.user
        current_user.name = name
        current_user.surname = surname
        current_user.email = email
        if password == password2:
            current_user.password = password
        current_user.save()
        return redirect('user-profile')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')
    def post(self, request):
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # return redirect('add-donation')
            return redirect('user-profile') #reverse?
        else:
            return redirect(reverse('register'))


class LogoutView(LoginRequiredMixin, View): #wylog.
    def get(self, request):
        logout(request)
        return redirect('index')


class Register(View):
    def get(self, request):
        return render(request, 'register.html')
    def post(self, request):
        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            User.objects.create_user(username=email, email=email, password=password,
                                                first_name=name, last_name=surname)
        return redirect(reverse('login'))
