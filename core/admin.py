from django.contrib import admin
from core.models import *

admin.site.register(User)
admin.site.register(Deploy)
admin.site.register(Params)
admin.site.register(Image)
admin.site.register(Container)