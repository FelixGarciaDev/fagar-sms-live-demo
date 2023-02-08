from django.contrib import admin
from .models import User, SmsManager, Company, RiskReport, Employee, IncidentAccident, Task
# Register your models here.

admin.site.register(User)
admin.site.register(SmsManager)
admin.site.register(Company)
admin.site.register(RiskReport)
admin.site.register(Employee)
admin.site.register(IncidentAccident)
admin.site.register(Task)