from django.contrib import admin

from exercise.models import BodyPart, Exercise, Set, Load
admin.site.register(BodyPart)
admin.site.register(Exercise)
admin.site.register(Set)
admin.site.register(Load)
