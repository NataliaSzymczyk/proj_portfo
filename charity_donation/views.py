from datetime import date
from django.core.paginator import Paginator
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

        all_donations = Donation.objects.aggregate(Sum('quantity'))
        supperted_foundations = Donation.objects.annotate(total=Count('institution', distinct=True))
        list_of = []
        for element in supperted_foundations:
            list_of.append(element.institution.name)
        set_of = set(list_of)
        # supported_institution=supperted_foundations[0].total # działa, ale nie to
        # supperted_foundations_set = set(supperted_foundations) #nie ma sensu, bo..
        supported_institution = len(set_of)

        foundations = Institution.objects.filter(type='Fundacja')
        organizations = Institution.objects.filter(type='Organizacja_pozarządowa')
        collections= Institution.objects.filter(type='Zbiórka_lokalna')

        p = Paginator(foundations, 2)
        # page = request.GET.get('page')
        # contacts = paginator.get_page(page)
        return render(request, 'index.html', {"foundations":foundations,
                                              "organizations":organizations,
                                              "collections":collections,
                                              "all_donations":all_donations,
                                              "supported_institution":supported_institution,})


class AddDonation(View):
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        return render(request, 'form.html', {"categories":categories, "institutions":institutions})
    # def post(self, request):
        # quantity = request.POST.get("bags")
        # chosen_organization = request.POST.get("organization")
        # got_organization = Institution.objects.get(id=chosen_organization)
        # # zbierze id -dokonczyc
        # adress = request.POST.get("adress")
        # city = request.POST.get("city")
        # zip_code = request.POST.get("postcode")
        # phone_number = request.POST.get("phone")
        # pick_up_date = request.POST.get("data")
        # pick_up_time = request.POST.get("time")
        # pick_up_comment = request.POST.get("more_info")
        # user = self.request.user
        # #
        # categories = request.POST.getlist("categories") #getlist
        #
        # new_d = Donation.objects.create(quantity=quantity, institution=got_organization,
        #                                 adress=adress, city=city, zip_code=zip_code,
        #                                 phone_number=phone_number, pick_up_time=pick_up_time,
        #                                 pick_up_date=pick_up_date, pick_up_comment=pick_up_comment,
        #                                 user=user)
        # for element in categories:
        #     new_d.categories.add(int(element)) #int?
        # new_d.save() #
        #
        # #is_taken ma default, click_date może być null
        #



class UserProfile(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user-profile.html')


class UserDonations(LoginRequiredMixin, View):
    def get(self, request):
        donated_by_me = Donation.objects.filter(user=self.request.user).order_by('-pick_up_date')
        dzis = date.today()
        donated_by_me_with_time = Donation.objects.filter(user=self.request.user).filter(pick_up_date__gt=dzis).order_by('pick_up_date')
        return render(request, 'user-donations.html', {"donated_by_me":donated_by_me, 'dzis':dzis,
                                                       "donated_by_me_with_time":donated_by_me_with_time})

    def post(self, request):
        today_is = date.today()
        donated_by_me = Donation.objects.filter(user=self.request.user).order_by('-click_date')
        dzis = date.today()
        donated_by_me_with_time = Donation.objects.filter(user=self.request.user).filter(
            pick_up_date__gt=dzis).order_by('pick_up_date')
        try:
            odebrane = int(request.POST['odebrane'])
            if odebrane != None:
                x = Donation.objects.get(id=odebrane)
                x.is_taken = False
                x.click_date = None
                x.save()
            return render(request, 'user-donations.html', {"donated_by_me": donated_by_me, 'dzis': dzis,
                                                       "donated_by_me_with_time": donated_by_me_with_time})

        except:
            nieodebrane = int(request.POST['nieodebrane'])
            if nieodebrane != None:
                x = Donation.objects.get(id=nieodebrane)
                x.is_taken=True
                x.click_date = today_is
                x.save()
                return render(request, 'user-donations.html', {"donated_by_me": donated_by_me, 'dzis': dzis,
                                                       "donated_by_me_with_time": donated_by_me_with_time})

        # if is_taken=='Zaznacz jako nieodebrane':
        #
        # if is_taken=='Zaznacz jako odebrane'


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
    # !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
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
        password1 = request.POST['password']
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
            return redirect(reverse('login'))#
