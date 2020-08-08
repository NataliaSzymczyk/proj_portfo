from django.contrib import admin
from charity_donation.models import Category, Institution, Donation
from django.contrib.auth.models import User
from django.db.models import ProtectedError
from django.db.models.signals import pre_delete
from django.dispatch import receiver


admin.site.site_header = "Panel administracyjny"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "type", "additional_list")
    ordering = ['type']
    def additional_list(self, obj):
        return ", ".join([str(o.name) for o in obj.categories.all()])


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ("quantity", "institution", "address", "phone_number", "city", "zip_code",
                    "pick_up_date", "pick_up_time", "pick_up_comment", "user", "additional_list2")
    raw_id_fields = ('institution',)
    def additional_list2(self, obj):
        return ", ".join([str(o.name) for o in obj.categories.all()])


@receiver(pre_delete, sender=User)
def function(sender, instance, **kwargs):
    if User.objects.all().count() == 1:
        raise ProtectedError('zabraniam kasowania użytkownika.', instance)


