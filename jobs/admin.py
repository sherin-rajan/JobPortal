from django.contrib import admin
from jobs.models import Sectors,Company,Jobs,Applications,Profile

# Register your models here.
admin.site.register(Sectors)
admin.site.register(Company)
admin.site.register(Jobs)
admin.site.register(Applications)
admin.site.register(Profile)