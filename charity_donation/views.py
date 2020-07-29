from datetime import date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.forms import forms
from django.http import HttpResponse #
from .forms import *
from django.shortcuts import render, redirect
from django.urls import reverse #
from django.views import View
from .models import Category, Donation, Institution
from django.db.models import Sum, Count
import os
import smtplib
from email.message import EmailMessage
from .validators import PasswordLenValidator, NumberValidator, LowLetterValidator, UpperLetterValidator, SpecialCharacterValidator


class LandingPage(View):
    def get(self, request):
        all_donations = Donation.objects.aggregate(Sum('quantity'))
        supperted_foundations = Donation.objects.annotate(total=Count('institution', distinct=True))
        list_of = []
        for element in supperted_foundations:
            list_of.append(element.institution.name)
        set_of = set(list_of)
        supported_institution = len(set_of)
        foundations = Institution.objects.filter(type='Fundacja')
        organizations = Institution.objects.filter(type='Organizacja_pozarządowa')
        collections= Institution.objects.filter(type='Zbiórka_lokalna')
        return render(request, 'index.html', {"foundations":foundations,
                                              "organizations":organizations,
                                              "collections":collections,
                                              "all_donations":all_donations,
                                              "supported_institution":supported_institution,})
    def post(self, request):
        superusers = User.objects.filter(is_superuser=True)
        mail_list = []
        for user in superusers:
            mail_list.append(user.email)
        name = request.POST['name']
        surname = request.POST['surname']
        message = request.POST['message']
        try:
            msg = EmailMessage()
            msg['Subject'] = 'Wiadomość kontaktowa'
            msg['From'] = f'{name} {surname} <email.potrzebny@interiowy.pl>'
            msg['To'] = mail_list
            msg.set_content(f'{message}')
            server = smtplib.SMTP_SSL('poczta.interia.pl', 465)
            server.ehlo()
            server.login('email.potrzebny@interiowy.pl', 'haslo1')
            # w przypadku wyboru tej metody wysyłki - trzeba uzupełnić odpowiednie dane
            server.send_message(msg)
            server.quit()
            return redirect('index')
        except Exception:
            return render(request, 'try-again-later.html')


class AddDonation(View):
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        try:
            chosen_categories = request.GET.getlist("categories")
            institutions_to_choose = Donation.categories.filter(donation__institution_id__in=chosen_categories)
            return render(request, 'form.html', {"categories":categories, "institutions":institutions, "institutions_to_choose":institutions_to_choose})
        except Exception:
            return render(request, 'form.html', {"categories":categories, "institutions":institutions})
    def post(self, request):
        quantity = request.POST.get("bags")
        chosen_organization = request.POST.get("organization")
        got_organization = Institution.objects.get(id=chosen_organization)

        address = request.POST.get("address")
        city = request.POST.get("city")
        zip_code = request.POST.get("postcode")
        phone_number = request.POST.get("phone")
        pick_up_date = request.POST.get("date")
        pick_up_time = request.POST.get("time")
        pick_up_comment = request.POST.get("more_info")
        user = self.request.user
        categories = request.POST.getlist("categories")

        new_donation = Donation()
        new_donation.quantity = quantity
        new_donation.institution = got_organization
        new_donation.address = address
        new_donation.city = city
        new_donation.zip_code = zip_code
        new_donation.phone_number = phone_number
        new_donation.pick_up_time = pick_up_time
        new_donation.pick_up_date = pick_up_date
        new_donation.pick_up_comment = pick_up_comment
        new_donation.user = user
        new_donation.save()

        for element in categories:
            new_donation.categories.add(int(element))
        new_donation.save() #
        return redirect('confirmation')


class FormConfirmation(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'form-confirmation.html')


class UserProfile(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user-profile.html')


class UserDonations(LoginRequiredMixin, View):
    def get(self, request):
        donated_by_me = Donation.objects.filter(user=self.request.user).order_by('is_taken', 'pick_up_date')
        return render(request, 'user-donations.html', {"donated_by_me":donated_by_me})

    def post(self, request):
        today_is = date.today()
        donated_by_me = Donation.objects.filter(user=self.request.user).order_by('is_taken', 'pick_up_date')
        try:
            odebrane = int(request.POST['odebrane'])
            if odebrane != None:
                x = Donation.objects.get(id=odebrane)
                x.is_taken = False
                x.click_date = None
                x.save()
            return render(request, 'user-donations.html', {"donated_by_me": donated_by_me})
        except:
            nieodebrane = int(request.POST['nieodebrane'])
            if nieodebrane != None:
                x = Donation.objects.get(id=nieodebrane)
                x.is_taken=True
                x.click_date = today_is
                x.save()
                return render(request, 'user-donations.html', {"donated_by_me": donated_by_me})


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
    # sp = "[!#$%&'()*+,-./:;<=>?@'[\]^_`{|}\"~]"
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
            return redirect('user-profile')
        else:
            return redirect(reverse('register'))


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('index')


class Register(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        name = request.POST['first_name']
        surname = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        sp_characters = "[!#$%&'()*+,-./:;<=>?@'[\]^_`{|}\"~]"
        if password1 != password2:
            msg = "Hasła się nie zgadzają."
            return render(request, 'register.html', {"msg":msg})
        elif len(password1) < 8:
            msg = 'Hasło musi mieć minimum 8 znaków.'
            return render(request, 'register.html', {"msg":msg})
        elif not any(char.isdigit() for char in password1):
            msg = 'Hasło musi zawierać minimum jedną cyfrę.'
            return render(request, 'register.html', {"msg":msg})
        elif not any(char.islower() for char in password1):
            msg = 'Hasło musi zawierać przynajmniej 1 małą literę.'
            return render(request, 'register.html', {"msg":msg})
        elif not any(char.isupper() for char in password1):
            msg = 'Hasło musi zawierać przynajmniej 1 dużą literę.'
            return render(request, 'register.html', {"msg":msg})
        elif not any(char in sp_characters for char in password1):
            msg = 'Hasło musi zawierać przynajmniej 1 znak specjalny, czyli jeden z tych: ' + sp_characters
            return render(request, 'register.html', {"msg":msg})
        else:
            User.objects.create_user(username=email, email=email, password=password1,
                                                first_name=name, last_name=surname)
            return redirect('login')
