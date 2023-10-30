from django.contrib import admin
from .models import Questions, Entries, Incorrectban
# Register your models here.

admin.site.register(Questions)
admin.site.register(Entries)
admin.site.register(Incorrectban)