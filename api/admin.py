from django.contrib import admin
from .models import User, Question, Meta, Card, Update
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(User, UserAdmin)
admin.site.register(Question)
admin.site.register(Meta)
admin.site.register(Card)
admin.site.register(Update)