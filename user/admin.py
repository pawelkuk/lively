from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import Permission

from exercise.models import BodyPart, Exercise, Set, Load
from measurement.models import MeasurementType, Measurement
from django.contrib.auth.forms import AuthenticationForm


class UserAdmin(AdminSite):

    login_form = AuthenticationForm

    def has_permission(self, request):
        """
        Removed check for is_staff.
        """
        request.user.user_permissions.add(Permission.objects.get(codename="change_set"))
        request.user.user_permissions.add(Permission.objects.get(codename="change_measurement"))
        request.user.user_permissions.add(Permission.objects.get(codename="delete_set"))
        request.user.user_permissions.add(Permission.objects.get(codename="delete_measurement"))
        return request.user.is_active


user_admin_site = UserAdmin(name='usersadmin')
user_admin_site.register(Measurement)
user_admin_site.register(MeasurementType)
user_admin_site.register(BodyPart)
user_admin_site.register(Exercise)
user_admin_site.register(Set)
user_admin_site.register(Load)

