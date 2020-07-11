from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .models import Category, Donation, Institution
from .forms import EditPassword

from django.db.models import Sum, Count



class LandingPage(View):
    def get(self, request):
        foundations = Institution.objects.filter(type='Fundacja')
        organizations = Institution.objects.filter(type='Organizacja_pozarządowa')
        collections= Institution.objects.filter(type='Zbiórka_lokalna')
        return render(request, 'index.html', {"foundations":foundations,
                                              "organizations":organizations,
                                              "collections":collections})


class AddDonation(View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'form.html', {"categories":categories})


class UserProfile(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user-profile.html')


class EditUser(LoginRequiredMixin, View):
    def get(self, request):
        form2 = EditPassword()
        return render(request, 'user-edit.html', {"form2":form2})
    def post(self, request):
        current_user = self.request.user
        current_user_id = User.objects.get(id=current_user.id)
        form2 = EditPassword(request.POST)
        username = request.POST['username']
        first_name = request.POST['first_name']
        surname = request.POST['surname']
        email = request.POST['email']
        old_password = request.POST['old_password']
        if current_user_id.check_password(old_password) == True:
            current_user_id.username = username
            current_user_id.first_name = first_name
            current_user_id.last_name = surname
            current_user_id.email = email
            current_user_id.save()
            msg = "Zapisano."
            return render(request, 'user-edit.html', {"msg": msg, "form2": form2})
        else:
            msg = "Hasło się nie zgadza. Popraw, aby zapisać."
            return render(request, 'user-edit.html', {"msg": msg, "form2": form2})


class UserPassword(LoginRequiredMixin, View):
    def get(self, request):
        form = EditPassword()
        return render(request, 'user-edit-pass.html', {"form":form})
    def post(self, request):
        current_user = self.request.user
        current_user_id = User.objects.get(id=current_user.id)
        form = EditPassword(request.POST)
        if form.is_valid():
            old_password1 = form.cleaned_data['old_password1']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if current_user_id.check_password(old_password1) == True:
                if password1 == password2:
                    current_user_id.set_password(password1)
                    current_user_id.save()
                    msg = "Zapisano hasło."
                    return render(request, 'user-edit.html', {"msg":msg, "form":form})
                else:
                    msg = "Hasła nie są identyczne. Popraw, aby zapisać."
                    return render(request, 'user-edit-pass.html', {"msg":msg, "form":form})


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
