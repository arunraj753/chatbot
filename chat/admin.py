from django.contrib import admin
from .models import Inquiry,Career,Leave,LeaveApplication,Project,News,ResetCode

admin.site.register(Inquiry)
admin.site.register(Career)
admin.site.register(Leave)
admin.site.register(LeaveApplication)
admin.site.register(Project)
admin.site.register(News)
admin.site.register(ResetCode)
