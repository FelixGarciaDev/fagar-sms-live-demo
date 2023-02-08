from django.db.models import Count

from datetime import datetime, date

from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse

# email verification and password reset stuff
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

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

from users.models import User, SmsManager, RiskReport, Employee, Company, IncidentAccident, Task
from .forms import EmployeeProfileFormModal, EmployeePicFormModal, EmployeeRiskReportForm, EmployeeIncidentAccidentForm

class EmployeeDashboardView(View):
    template_name = "employee/employeeStart.html"     

    def get(self, request, *args, **kwargs):
        # GET method
        context={}
        id_ = self.request.user.id
        employee = get_object_or_404(Employee, user=id_)
        context["employee"] = employee
        company = get_object_or_404(Company, employee_of_company=employee)
        context["company"] = company
        context["totalRiskReports"] = RiskReport.objects.filter(owner=employee.user).count()
        context["totalIncidentes"] = IncidentAccident.objects.filter(owner=employee.user).count()
        context["uncompleted"]  = Task.objects.filter(reponsable=employee.user, completedTask=False).count()
        return render(request, self.template_name, context)    
        
class EmployeeProfileView(DetailView):
    model           = Employee
    template_name   = 'employee/employeeProfile.html'    

    def get_object(self):        
        id_ = self.request.user.id
        return get_object_or_404(Employee, user=id_)

class EmployeeProfileUpdate(UpdateView):
    model = Employee
    template_name = 'employee/modals/employeeUpdateProfile.html'
    form_class = EmployeeProfileFormModal

    def get_object(self):        
        id_ = self.request.user.id
        return get_object_or_404(Employee, user=id_)    

    def get_success_url(self):
            return reverse('employees:profile')

class EmployeeProfilePicUpdateView(UpdateView):
    model           = Employee
    template_name   = 'employee/modals/employeeUpdateProfilePic.html'
    form_class      = EmployeePicFormModal

    def get_object(self):        
        id_ = self.request.user.id
        return get_object_or_404(Employee, user=id_)    

    def get_success_url(self):
        return reverse('employees:profile')

#RISK REPORTS VIEWS
class EmployeeRiskReportListView(ListView):
    model = RiskReport    
    paginate_by = 10
    context_object_name = 'risk_reports'
    template_name = 'employee/riskReports/employeeRiskReportList.html'

    def get_context_data(self, **kwargs):
        #obtengo id del empleado
        id_ = self.request.user.id
        employee = get_object_or_404(Employee, user=id_)        
        kwargs['employee'] = employee
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        #obtengo id del empleado
        id_ = self.request.user.id
        employee = get_object_or_404(Employee, user=id_)
        #obtengo solo los reportes hechos por este empleado
        queryset = RiskReport.objects.filter(owner=employee.user).order_by('-id')
        return queryset

class EmployeeRiskReportListWithSearchView(ListView):
    model = RiskReport    
    paginate_by = 10
    context_object_name = 'risk_reports'
    template_name = 'employee/riskReports/employeeRiskReportList.html'

    def get_queryset(self):
        id_             = self.request.user.id
        employee        = get_object_or_404(Employee, user=id_)        
        company         = employee.company        
        my_search       = self.request.GET.get('my_search')        
        new_queryset    = RiskReport.objects.filter(owner=employee.user, of_company=company, description__unaccent__icontains=my_search).order_by('-id')
        return new_queryset

    def get_context_data(self, **kwargs):
        context                 = super(EmployeeRiskReportListWithSearchView, self).get_context_data(**kwargs)
        context['my_search']    = self.request.GET.get('my_search')
        return context

class EmployeeRiskReportDetailView(DetailView):
    template_name = 'employee/riskReports/employeeRiskReportDetail.html'
    model         = RiskReport   

    def get_object(self):        
        id_ = self.kwargs.get("id")        
        return get_object_or_404(RiskReport, id=id_)

class EmployeeCreateRiskReportView(CreateView):
    model = RiskReport    
    template_name = 'employee/riskReports/employeeRiskReportCreate.html'
    form_class      = EmployeeRiskReportForm    

    def form_valid(self, form):        
        new_report = form.save(commit=False)
        new_report.owner = self.request.user
        #obtengo id del empleado
        id_ = self.request.user.id
        employee = get_object_or_404(Employee, user=id_)            
        new_report.of_company = employee.company        
        # save report
        new_report.save()
        # email notification to manager
        # company         = employee.company
        # manager         = company.company_sms_manager        
        # domain          = get_current_site(self.request).domain
        # link            = reverse('managers:risk-report-detail', kwargs={'id':new_report.id})
        # report_url      = 'http://'+domain+link        
        # email_subject   = '[Fagar-SMS] '+employee.name+' '+employee.last_name+' ha creado un reporte de riesgo para '+company.name
        # emai_body       = employee.name+' '+employee.last_name+' ha creado un reporte de riesgo\n'+'Puedes revisarlo en el siguiente link: '+report_url        
        # send_mail(
        #     email_subject, 
        #     emai_body,
        #     #'noreply@fagar.com'
        #     'fg.sos.store@gmail.com',
        #     #['manager.user'], #recipients list
        #     ['fg.sos.store@gmail.com'],
        #     fail_silently=False,
        # )    
        return redirect('employees:risk-report-list')

###################################INCIDENTS-ACCIDENTS REPORTS VIEWS
class EmployeeIncidentAccidentListView(ListView):
    model = IncidentAccident    
    paginate_by = 10
    context_object_name = 'incidents_accidents'
    template_name = 'employee/incidents_and_accidents/employeeIncidentAccidentList.html'

    def get_context_data(self, **kwargs):
        #obtengo id del empleado y el empleado asociado
        id_ = self.request.user.id
        employee = get_object_or_404(Employee, user=id_)        
        kwargs['employee']          = employee
        company                     = employee.company
        kwargs['incidents']         = IncidentAccident.objects.filter(of_company=company, only_incident='1').order_by('-id')
        kwargs['accidents']         = IncidentAccident.objects.filter(of_company=company, only_incident='2').order_by('-id')
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        #obtengo id del empleado
        id_ = self.request.user.id
        employee = get_object_or_404(Employee, user=id_)
        #obtengo solo los reportes hechos por este empleado
        queryset = IncidentAccident.objects.filter(owner=employee.user).order_by('-id')
        return queryset

class EmployeeIncidentAccidentListWithSearchView(ListView):
    model               = IncidentAccident    
    paginate_by         = 10
    context_object_name = 'incidents_accidents'
    template_name = 'employee/incidents_and_accidents/employeeIncidentAccidentList.html'

    def get_context_data(self, **kwargs):
        context                 = super(EmployeeIncidentAccidentListWithSearchView, self).get_context_data(**kwargs)
        context['my_search']    = self.request.GET.get('my_search')        
        my_search               = self.request.GET.get('my_search')
        id_ = self.request.user.id
        employee = get_object_or_404(Employee, user=id_)        
        kwargs['employee']      = employee
        company                 = employee.company        
        incidents               = IncidentAccident.objects.filter(of_company=company, only_incident='1', description__unaccent__icontains=my_search).order_by('-id')
        accidents               = IncidentAccident.objects.filter(of_company=company, only_incident='2', description__unaccent__icontains=my_search).order_by('-id')        
        kwargs['incidents']     = incidents
        kwargs['accidents']     = accidents
        return super().get_context_data(**kwargs)

class EmployeeIncidentAccidentDetailView(DetailView):
    template_name = 'employee/incidents_and_accidents/employeeIncidentAccidentDetail.html'
    model         = IncidentAccident   

    def get_object(self):        
        id_ = self.kwargs.get("id")                
        return get_object_or_404(IncidentAccident, id=id_)

class EmployeeCreateIncidentAccidentView(CreateView):
    model = IncidentAccident    
    template_name = 'employee/incidents_and_accidents/employeeIncidentAccidentCreate.html'
    form_class      = EmployeeIncidentAccidentForm    

    def form_valid(self, form):        
        new_report = form.save(commit=False)
        new_report.owner = self.request.user
        #obtengo id del empleado
        id_ = self.request.user.id
        employee = get_object_or_404(Employee, user=id_)            
        new_report.of_company = employee.company        
        #guardo el reporte
        new_report.save()
        # email notification to manager
        # company         = employee.company
        # manager         = company.company_sms_manager
        # if new_report.only_incident == '1':
        #     type_report = 'incidente'
        # if new_report.only_incident == '2':
        #     type_report = 'accidente'
        # domain          = get_current_site(self.request).domain
        # link            = reverse('managers:incident-accident-detail', kwargs={'id':new_report.id})
        # report_url      = 'http://'+domain+link        
        # email_subject   = '[Fagar-SMS] '+employee.name+' '+employee.last_name+' ha creado un reporte de '+type_report+' para '+company.name
        # emai_body       = employee.name+' '+employee.last_name+' ha creado un reporte de '+type_report+'.\n'+'Puedes revisarlo en el siguiente link: '+report_url        
        # send_mail(
        #     email_subject, 
        #     emai_body,
        #     #'noreply@fagar.com'
        #     'fg.sos.store@gmail.com',
        #     #['manager.user'], #recipients list
        #     ['fg.sos.store@gmail.com'],
        #     fail_silently=False,
        # )                
        return redirect('employees:incident-accident-list')

###################################INCIDENTS-ACCIDENTS REPORTS VIEWS

class EmployeeTaskListView(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'employee/task/taskList.html'

    def get_context_data(self, **kwargs):
        #obtengo id del empleado y el empleado asociado
        id_ = self.request.user.id
        employee = get_object_or_404(Employee, user=id_)        
        kwargs['notdone'] = Task.objects.filter(employee=employee, completedTask=False).order_by('-id')
        kwargs['done'] = Task.objects.filter(employee=employee, completedTask=True).order_by('-id')
        return super().get_context_data(**kwargs)

class EmployeeUpdateTaskStatusView(View):        
    template_name = 'employee/modals/taskUpdateStatus.html'       

    def post(self, request, *args, **kwargs):
        id_ = self.kwargs.get("id")
        task = get_object_or_404(Task, id = id_)        
        user_id_ = self.request.user.id
        employee = get_object_or_404(Employee, user=user_id_)
        if task.completedTask == False:
            task.completed_date = datetime.now()
        task.completedTask = not task.completedTask
        task.save()
        # Mail logic
        # if  task.completedTask == True:
        #     company         = employee.company
        #     report          = task.report 
        #     domain          = get_current_site(self.request).domain
        #     link            = reverse('managers:task-list')
        #     report_url      = 'http://'+domain+link        
        #     email_subject   = '[Fagar-SMS] '+employee.name+' '+employee.last_name+' ha marcado como completada una defensa o tarea para '+company.name
        #     emai_body       = employee.name+' '+employee.last_name+' ha marcado como completada la siguiente defensa o tarea: "'+task.taskDescription+'" asociada al reporte "'+report.description+'" para '+company.name+'.\n'+'Puedes revisarlo en el siguiente link: '+report_url        
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
        #     company         = employee.company
        #     report          = task.report 
        #     domain          = get_current_site(self.request).domain
        #     link            = reverse('managers:task-list')
        #     report_url      = 'http://'+domain+link        
        #     email_subject   = '[Fagar-SMS] '+employee.name+' '+employee.last_name+' ha marcado como pendiente una defensa o tarea para '+company.name
        #     emai_body       = employee.name+' '+employee.last_name+' ha marcado como pendiente la siguiente defensa o tarea: "'+task.taskDescription+'" asociada al reporte "'+report.description+'" para '+company.name+'.\n'+'Puedes revisarlo en el siguiente link: '+report_url        
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
        return HttpResponseRedirect(reverse('employees:task-list'))

    