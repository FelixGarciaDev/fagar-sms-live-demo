from django.db.models import Count

from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse

# email verification and password reset stuff
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

from django.db.models import Q

from datetime import datetime, date

from users.tokens import token_generator
# VIEWS
from django.views import View
from django.views.generic.base import RedirectView
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    ListView,
    DeleteView,
    FormView
)

from users.models import User, SmsManager, RiskReport, Company, Employee, Task

class SmsManagerTaskListView(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'managers/task/taskList.html'    

    def get_context_data(self, **kwargs):        
        id_ = self.request.user.id
        manager = get_object_or_404(SmsManager, user=id_)
        company = get_object_or_404(Company, company_sms_manager=manager)
        employees = Employee.objects.filter(company=company)        
        kwargs['notdone'] = Task.objects.filter(Q(employee__in=employees, completedTask=False) | Q(manager=manager, completedTask=False)).order_by('-id')
        kwargs['done'] = Task.objects.filter(Q(employee__in=employees, completedTask=True) | Q(manager=manager, completedTask=True)).order_by('-id')
        return super().get_context_data(**kwargs)

class SmsManagerUpdateTaskStatusView(View):        
    template_name = 'managers/modals/taskUpdateStatus.html'       

    def post(self, request, *args, **kwargs):
        id_ = self.kwargs.get("id")
        task = get_object_or_404(Task, id = id_)
        user_id_ = self.request.user.id
        manager = get_object_or_404(SmsManager, user=user_id_)
        if task.completedTask == False:
            task.completed_date = datetime.now()
        task.completedTask = not task.completedTask        
        task.save()
        # Mail logic
        # if  task.completedTask == True:
        #     company         = manager.managed_by.first()
        #     report          = task.report 
        #     domain          = get_current_site(self.request).domain
        #     link            = reverse('employees:task-list')
        #     report_url      = 'http://'+domain+link        
        #     email_subject   = '[Fagar-SMS] El Gerente SMS ha marcado como completada tu defensa o tarea para '+company.name
        #     emai_body       = 'El Gerente SMS ha marcado como completada tu defensa o tarea asignada: "'+task.taskDescription+'" asociada al reporte "'+report.description+'" para '+company.name+'.\n'+'Puedes revisarlo en el siguiente link: '+report_url        
        #     send_mail(
        #         email_subject, 
        #         emai_body,
        #         #'noreply@fagar.com'
        #         'noreply@fagar.com',
        #         #['manager.user'], #recipients list
        #         ['fg.sos.store@gmail.com'],
        #         fail_silently=False,
        #     )
        # if  task.completedTask == False:
        #     company         = manager.managed_by.first()
        #     report          = task.report 
        #     domain          = get_current_site(self.request).domain
        #     link            = reverse('employees:task-list')
        #     report_url      = 'http://'+domain+link        
        #     email_subject   = '[Fagar-SMS] El Gerente SMS ha marcado como pendiente tu defensa o tarea para '+company.name
        #     emai_body       = 'El Gerente SMS ha marcado como pendiente tu defensa o tarea asignada: "'+task.taskDescription+'" asociada al reporte "'+report.description+'" para '+company.name+'.\n'+'Puedes revisarlo en el siguiente link: '+report_url        
        #     send_mail(
        #         email_subject, 
        #         emai_body,
        #         #'noreply@fagar.com'
        #         'noreply@fagar.com',
        #         #['manager.user'], #recipients list
        #         ['fg.sos.store@gmail.com'],
        #         fail_silently=False,
        #     )
        # redirect
        return HttpResponseRedirect(reverse('managers:task-list'))