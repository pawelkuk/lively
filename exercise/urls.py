from django.conf.urls import url
from .views import body_part_form, set_form, exercise_form, load_form

urlpatterns = [
    url('^bodypartform/', body_part_form, name='body_part_form'),
    url('^setform/', set_form, name='set_form'),
    url('^exerciseform/', exercise_form, name='exercise_form'),
    url('^loadform/', load_form, name='load_form'),
]
