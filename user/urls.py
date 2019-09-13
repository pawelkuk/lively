from django.conf.urls import url, include
from django.shortcuts import redirect
from django.urls import path

from .views import home, SignUpView, measurement_progress, exercise_progress,\
    progress_exercise_chart, progress_measurement_chart
from django.contrib.auth.views import LoginView, LogoutView
from user.admin import user_admin_site
from django.contrib import admin



admin.autodiscover()

urlpatterns = [
    url('^$', home, name='user_home'),
    url('^login/', LoginView.as_view(template_name='user/login_form.html'),
        name='user_login'),
    url('^logout/', LogoutView.as_view(),
        name='user_logout'),
    url('signup', SignUpView.as_view(), name='user_signup'),
    path('admin/', user_admin_site.urls),
    url('progress/measurement$', measurement_progress, name='measurement_progress'),
    url('progress/exercise$', exercise_progress, name='exercise_progress'),
    path('progress/measurement/<int:progress_type>/', progress_measurement_chart, name='progress_measurement_chart'),
    path('progress/exercise/<int:progress_type>/', progress_exercise_chart, name='progress_exercise_chart'),
]
