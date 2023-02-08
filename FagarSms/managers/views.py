from django.contrib import messages

from datetime import datetime, date

from django.db.models import Count, Q

from django.db.models.functions import Trunc

from django.shortcuts import render, redirect, get_object_or_404

from django.urls import reverse

from django.http import HttpResponseRedirect

# email verification and password reset stuff
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

from users.tokens import token_generator
# VIEWS
from django.views import View
from django.views.generic.base import RedirectView
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,    
    DeleteView,
    FormView
)

from users.models import SmsManager, RiskReport, Company, Employee, IncidentAccident, User, Task

from .forms import (
    SmsManagerProfileFormModal,
    SmsManagerProfilePicFormModal,
    SmsManagerRiskReportForm,
    SmsManagerIncidentAccidentForm,
    SignupEmployeeForm,
    EmployeeProfileFormModal,
    EmployeeProfilePicFormModal,
    SmsManagerAddLevelForm,
    SmsManagerAddTaskForm,
) 

class SmsManagerDashboardView(View):    
    template_name = "managers/managerStart.html"        

    def get(self, request, *args, **kwargs):
        # GET method
        context={}
        #Obtengo El manager                
        id_ = self.request.user.id
        manager = get_object_or_404(SmsManager, user=id_)
        #obtengo cuantas compañias maneja el manager
        number = manager.managed_by.count() #"managed_by" es el related name definido en el modelo de compañia
        #si el manager no maneja ningun prestador de servicios
        if number == 0:        
            context["Manage_cero"] = True
        #si el manager gestiona un solo prestador de servicios
        if number == 1:        
            context["Manage_many"] = False            
            company = get_object_or_404(Company, company_sms_manager=manager)
            context["company"] = company
            # here is the magic of counting objects by time            
            current_year        = datetime.now().year
            current_month       = datetime.now().month
            current_week        = date.today().isocalendar()[1] 
            current_day         = datetime.now().day            
            #number of risk reports
            context["reports_this_year"]                = RiskReport.objects.filter(date__year=current_year, of_company=company).count()
            context["reports_this_month"]               = RiskReport.objects.filter(date__month=current_month, of_company=company).count()
            context["reports_this_week"]                = RiskReport.objects.filter(date__week=current_week, of_company=company).count()
            context["reports_this_day"]                 = RiskReport.objects.filter(date__day=current_day, of_company=company).count()            
            # conditios for colors
            # in start everything is green
            context["risk_report_card_color"]           = 'green'

            # conditions for orange
            if context["reports_this_week"] >= 6 and context["reports_this_week"] <= 10:
                context["risk_report_card_color"] = 'orange'
            if context["reports_this_month"] >= 11 and context["reports_this_month"] <= 20:
                context["risk_report_card_color"] = 'orange'
            if context["reports_this_year"] >= 21 and context["reports_this_year"] <= 50:
                context["risk_report_card_color"] = 'orange'

            # conditions for red
            if context["reports_this_week"] >= 11:
                context["risk_report_card_color"] = 'red'
            if context["reports_this_month"] >= 11:
                context["risk_report_card_color"] = 'red'
            if context["reports_this_year"] >= 21:
                context["risk_report_card_color"] = 'red'
                       
            #number of risk reports by type
            context["Vuelo_this_year"]                  = RiskReport.objects.filter(date__year=current_year, type_of_risk='1', of_company=company).count()
            context["EPP_this_year"]                    = RiskReport.objects.filter(date__year=current_year, type_of_risk='2', of_company=company).count()
            context["Procedimientos_this_year"]         = RiskReport.objects.filter(date__year=current_year, type_of_risk='3', of_company=company).count()
            context["Mantenimiento_this_year"]          = RiskReport.objects.filter(date__year=current_year, type_of_risk='4', of_company=company).count()
            context["FOD_this_year"]                    = RiskReport.objects.filter(date__year=current_year, type_of_risk='5', of_company=company).count()
            context["OrdenLimpieza_this_year"]          = RiskReport.objects.filter(date__year=current_year, type_of_risk='6', of_company=company).count()
            context["ActoInseguro_year"]                = RiskReport.objects.filter(date__year=current_year, type_of_risk='7', of_company=company).count()
            context["Otros_this_year"]                  = RiskReport.objects.filter(date__year=current_year, type_of_risk='8', of_company=company).count()
            # number of incidints / accidents
            context["incidents_this_year"]              = IncidentAccident.objects.filter(date__year=current_year, of_company=company, only_incident='1').count()
            context["incidents_this_month"]             = IncidentAccident.objects.filter(date__month=current_month, of_company=company, only_incident='1').count()
            context["incidents_this_week"]              = IncidentAccident.objects.filter(date__week=current_week, of_company=company, only_incident='1').count()
            context["incidents_this_day"]               = IncidentAccident.objects.filter(date__day=current_day, of_company=company, only_incident='1').count()
            # number of accidents
            context["accidents_this_year"]              = IncidentAccident.objects.filter(date__year=current_year, of_company=company, only_incident='2').count()
            context["accidents_this_month"]             = IncidentAccident.objects.filter(date__month=current_month, of_company=company, only_incident='2').count()
            context["accidents_this_week"]              = IncidentAccident.objects.filter(date__week=current_week, of_company=company, only_incident='2').count()
            context["accidents_this_day"]               = IncidentAccident.objects.filter(date__day=current_day, of_company=company, only_incident='2').count()
            # number of reports by month
            context["reports_on_janaury"]               = RiskReport.objects.filter(date__iso_year=current_year, date__month=1, of_company=company).count()
            context["reports_on_february"]              = RiskReport.objects.filter(date__iso_year=current_year, date__month=2, of_company=company).count()
            context["reports_on_march"]                 = RiskReport.objects.filter(date__iso_year=current_year, date__month=3, of_company=company).count()
            context["reports_on_april"]                 = RiskReport.objects.filter(date__iso_year=current_year, date__month=4, of_company=company).count()
            context["reports_on_may"]                   = RiskReport.objects.filter(date__iso_year=current_year, date__month=5, of_company=company).count()
            context["reports_on_june"]                  = RiskReport.objects.filter(date__iso_year=current_year, date__month=6, of_company=company).count()
            context["reports_on_july"]                  = RiskReport.objects.filter(date__iso_year=current_year, date__month=7, of_company=company).count()
            context["reports_on_august"]                = RiskReport.objects.filter(date__iso_year=current_year, date__month=8, of_company=company).count()
            context["reports_on_september"]             = RiskReport.objects.filter(date__iso_year=current_year, date__month=9, of_company=company).count()
            context["reports_on_october"]               = RiskReport.objects.filter(date__iso_year=current_year, date__month=10, of_company=company).count()
            context["reports_on_november"]              = RiskReport.objects.filter(date__iso_year=current_year, date__month=11, of_company=company).count()
            context["reports_on_december"]              = RiskReport.objects.filter(date__iso_year=current_year, date__month=12, of_company=company).count()
            # number of reports by danger level on january
            context["low_on_janaury"]                   = RiskReport.objects.filter(date__iso_year=current_year, date__month=1, of_company=company, level_of_risk='1').count()
            context["moderate_on_janaury"]              = RiskReport.objects.filter(date__iso_year=current_year, date__month=1, of_company=company, level_of_risk='2').count()
            context["high_on_janaury"]                  = RiskReport.objects.filter(date__iso_year=current_year, date__month=1, of_company=company, level_of_risk='3').count()
            context["extreme_on_janaury"]               = RiskReport.objects.filter(date__iso_year=current_year, date__month=1, of_company=company, level_of_risk='4').count()
            context["no_level_on_janaury"]               = RiskReport.objects.filter(date__iso_year=current_year, date__month=1, of_company=company, level_of_risk='').count()
            # number of reports by danger level on february
            context["low_on_february"]                  = RiskReport.objects.filter(date__iso_year=current_year, date__month=2, of_company=company, level_of_risk='1').count()
            context["moderate_on_february"]             = RiskReport.objects.filter(date__iso_year=current_year, date__month=2, of_company=company, level_of_risk='2').count()
            context["high_on_february"]                 = RiskReport.objects.filter(date__iso_year=current_year, date__month=2, of_company=company, level_of_risk='3').count()
            context["extreme_on_february"]              = RiskReport.objects.filter(date__iso_year=current_year, date__month=2, of_company=company, level_of_risk='4').count()
            context["no_level_on_february"]              = RiskReport.objects.filter(date__iso_year=current_year, date__month=2, of_company=company, level_of_risk='').count()
            # number of reports by danger level on march
            context["low_on_march"]                     = RiskReport.objects.filter(date__iso_year=current_year, date__month=3, of_company=company, level_of_risk='1').count()
            context["moderate_on_march"]                = RiskReport.objects.filter(date__iso_year=current_year, date__month=3, of_company=company, level_of_risk='2').count()
            context["high_on_march"]                    = RiskReport.objects.filter(date__iso_year=current_year, date__month=3, of_company=company, level_of_risk='3').count()
            context["extreme_on_march"]                 = RiskReport.objects.filter(date__iso_year=current_year, date__month=3, of_company=company, level_of_risk='4').count()
            context["no_level_on_march"]                = RiskReport.objects.filter(date__iso_year=current_year, date__month=3, of_company=company, level_of_risk='').count()
            # number of reports by danger level on april
            context["low_on_april"]                     = RiskReport.objects.filter(date__iso_year=current_year, date__month=4, of_company=company, level_of_risk='1').count()
            context["moderate_on_april"]                = RiskReport.objects.filter(date__iso_year=current_year, date__month=4, of_company=company, level_of_risk='2').count()
            context["high_on_april"]                    = RiskReport.objects.filter(date__iso_year=current_year, date__month=4, of_company=company, level_of_risk='3').count()
            context["extreme_on_april"]                 = RiskReport.objects.filter(date__iso_year=current_year, date__month=4, of_company=company, level_of_risk='4').count()
            context["no_level_on_april"]                 = RiskReport.objects.filter(date__iso_year=current_year, date__month=4, of_company=company, level_of_risk='').count()
            # number of reports by danger level on may
            context["low_on_may"]                       = RiskReport.objects.filter(date__iso_year=current_year, date__month=5, of_company=company, level_of_risk='1').count()
            context["moderate_on_may"]                  = RiskReport.objects.filter(date__iso_year=current_year, date__month=5, of_company=company, level_of_risk='2').count()
            context["high_on_may"]                      = RiskReport.objects.filter(date__iso_year=current_year, date__month=5, of_company=company, level_of_risk='3').count()
            context["extreme_on_may"]                   = RiskReport.objects.filter(date__iso_year=current_year, date__month=5, of_company=company, level_of_risk='4').count()
            context["no_level_on_may"]                  = RiskReport.objects.filter(date__iso_year=current_year, date__month=5, of_company=company, level_of_risk='').count()
            # number of reports by danger level on june
            context["low_on_june"]                      = RiskReport.objects.filter(date__iso_year=current_year, date__month=6, of_company=company, level_of_risk='1').count()
            context["moderate_on_june"]                 = RiskReport.objects.filter(date__iso_year=current_year, date__month=6, of_company=company, level_of_risk='2').count()
            context["high_on_june"]                     = RiskReport.objects.filter(date__iso_year=current_year, date__month=6, of_company=company, level_of_risk='3').count()
            context["extreme_on_june"]                  = RiskReport.objects.filter(date__iso_year=current_year, date__month=6, of_company=company, level_of_risk='4').count()
            context["no_level_on_june"]                 = RiskReport.objects.filter(date__iso_year=current_year, date__month=6, of_company=company, level_of_risk='').count()
            # number of reports by danger level on july
            context["low_on_july"]                      = RiskReport.objects.filter(date__iso_year=current_year, date__month=7, of_company=company, level_of_risk='1').count()
            context["moderate_on_july"]                 = RiskReport.objects.filter(date__iso_year=current_year, date__month=7, of_company=company, level_of_risk='2').count()
            context["high_on_july"]                     = RiskReport.objects.filter(date__iso_year=current_year, date__month=7, of_company=company, level_of_risk='3').count()
            context["extreme_on_july"]                  = RiskReport.objects.filter(date__iso_year=current_year, date__month=7, of_company=company, level_of_risk='4').count()
            context["no_level_on_july"]                 = RiskReport.objects.filter(date__iso_year=current_year, date__month=7, of_company=company, level_of_risk='').count()
            # number of reports by danger level on august
            context["low_on_august"]                    = RiskReport.objects.filter(date__iso_year=current_year, date__month=8, of_company=company, level_of_risk='1').count()
            context["moderate_on_august"]               = RiskReport.objects.filter(date__iso_year=current_year, date__month=8, of_company=company, level_of_risk='2').count()
            context["high_on_august"]                   = RiskReport.objects.filter(date__iso_year=current_year, date__month=8, of_company=company, level_of_risk='3').count()
            context["extreme_on_august"]                = RiskReport.objects.filter(date__iso_year=current_year, date__month=8, of_company=company, level_of_risk='4').count()
            context["no_level_on_august"]                = RiskReport.objects.filter(date__iso_year=current_year, date__month=8, of_company=company, level_of_risk='').count()
            # number of reports by danger level on september
            context["low_on_september"]                 = RiskReport.objects.filter(date__iso_year=current_year, date__month=9, of_company=company, level_of_risk='1').count()
            context["moderate_on_september"]            = RiskReport.objects.filter(date__iso_year=current_year, date__month=9, of_company=company, level_of_risk='2').count()
            context["high_on_september"]                = RiskReport.objects.filter(date__iso_year=current_year, date__month=9, of_company=company, level_of_risk='3').count()
            context["extreme_on_september"]             = RiskReport.objects.filter(date__iso_year=current_year, date__month=9, of_company=company, level_of_risk='4').count()
            context["no_level_on_september"]            = RiskReport.objects.filter(date__iso_year=current_year, date__month=9, of_company=company, level_of_risk='').count()
            # number of reports by danger level on october
            context["low_on_october"]                   = RiskReport.objects.filter(date__iso_year=current_year, date__month=10, of_company=company, level_of_risk='1').count()
            context["moderate_on_october"]              = RiskReport.objects.filter(date__iso_year=current_year, date__month=10, of_company=company, level_of_risk='2').count()
            context["high_on_october"]                  = RiskReport.objects.filter(date__iso_year=current_year, date__month=10, of_company=company, level_of_risk='3').count()
            context["extreme_on_october"]               = RiskReport.objects.filter(date__iso_year=current_year, date__month=10, of_company=company, level_of_risk='4').count()
            context["no_level_on_october"]              = RiskReport.objects.filter(date__iso_year=current_year, date__month=10, of_company=company, level_of_risk='').count()
            # number of reports by danger level on november
            context["low_on_november"]                  = RiskReport.objects.filter(date__iso_year=current_year, date__month=11, of_company=company, level_of_risk='1').count()
            context["moderate_on_november"]             = RiskReport.objects.filter(date__iso_year=current_year, date__month=11, of_company=company, level_of_risk='2').count()
            context["high_on_november"]                 = RiskReport.objects.filter(date__iso_year=current_year, date__month=11, of_company=company, level_of_risk='3').count()            
            context["extreme_on_november"]              = RiskReport.objects.filter(date__iso_year=current_year, date__month=11, of_company=company, level_of_risk='4').count()
            context["no_level_on_november"]             = RiskReport.objects.filter(date__iso_year=current_year, date__month=11, of_company=company, level_of_risk='').count()            
            # number of reports by danger level on december
            context["low_on_december"]                  = RiskReport.objects.filter(date__iso_year=current_year, date__month=12, of_company=company, level_of_risk='1').count()
            context["moderate_on_december"]             = RiskReport.objects.filter(date__iso_year=current_year, date__month=12, of_company=company, level_of_risk='2').count()
            context["high_on_december"]                 = RiskReport.objects.filter(date__iso_year=current_year, date__month=12, of_company=company, level_of_risk='3').count()
            context["extreme_on_december"]              = RiskReport.objects.filter(date__iso_year=current_year, date__month=12, of_company=company, level_of_risk='4').count()
            context["no_level_on_december"]             = RiskReport.objects.filter(date__iso_year=current_year, date__month=12, of_company=company, level_of_risk='').count()
            
        if number > 1:        
            context["Manage_many"] = True
            context["select_a_company"] = False
            companys = Company.objects.filter(company_sms_manager=manager)
            context["companys"] = companys
        return render(request, self.template_name, context)

class SmsManagerDashboardCompanySelectedView(View):    
    template_name = "sms_manager/SmsManagerDashboardStart.html"        

    def get(self, request, *args, **kwargs):        
        context={}        
        id_ = self.request.user.id
        manager = get_object_or_404(SmsManager, user=id_)                
        context["Manage_many"] = True        
        context["select_a_company"] = True
        company = get_object_or_404(Company, id=self.kwargs.get("id_company"))
        context["company"] = company
        companys = Company.objects.filter(company_sms_manager=manager)
        context["companys"] = companys
        return render(request, self.template_name, context)

class SmsManagerProfileView(DetailView):
    model           = SmsManager
    template_name   = 'managers/managerProfile.html'

    def get_context_data(self, **kwargs):        
        id_ = self.request.user.id
        manager = get_object_or_404(SmsManager, user=id_)        
        number = manager.managed_by.count() #"managed_by" es el related name definido en el modelo de compañia        
        if number == 1:
            kwargs["Manage_many"]       = False
            company                     = manager.managed_by.first() #Como las compañias solo pueden tener un gerente sms, nos basta con el primero de la relación
            kwargs['sms_managers']      = manager            
        if number > 1:
            kwargs["Manage_many"]       = True
            kwargs["select_a_company"]  = True
            #compañia que seleccione
            company                     = get_object_or_404(Company, id=self.kwargs.get("id_company"))
            kwargs["company"]           = company
            #todas las compañias
            companys                    = Company.objects.filter(company_sms_manager=manager)
            kwargs["companys"]          = companys
            kwargs['sms_managers']      = manager
            kwargs['employees']         = Employee.objects.filter(company=company)

        return super().get_context_data(**kwargs)

    def get_object(self):        
        id_ = self.request.user.id
        return get_object_or_404(SmsManager, user=id_)

class SmsManagerProfileUpdate(UpdateView):
    model = SmsManager
    template_name = 'managers/modals/managerUpdateProfile.html'
    form_class = SmsManagerProfileFormModal

    def get_object(self):        
        id_ = self.request.user.id
        return get_object_or_404(SmsManager, user=id_)    

    def get_success_url(self):
            return reverse('managers:profile')

class SmsManagerProfilePicUpdateView(UpdateView):
    model           = SmsManager
    template_name   = 'managers/modals/managerProfilePicture.html'
    form_class      = SmsManagerProfilePicFormModal    

    def get_object(self):        
        id_ = self.request.user.id
        return get_object_or_404(SmsManager, user=id_)    

    def get_success_url(self):
        return reverse('managers:profile')


#RISK REPORTS VIEWS
class SmsManagerRiskReportListView(ListView):
    model = RiskReport    
    paginate_by = 10
    context_object_name = 'risk_reports'
    template_name = 'managers/riskReports/SmsManager-RiskReportList.html'

    def get_context_data(self, **kwargs):
        #obtengo id del manager
        id_ = self.request.user.id
        manager = get_object_or_404(SmsManager, user=id_)
        #obtengo cuantas compañias maneja el manager
        number = manager.managed_by.count() #"managed_by" es el related name definido en el modelo de compañia        
        if number == 1:
            kwargs["Manage_many"] = False
            company                 = manager.managed_by.first() #Como las compañias solo pueden tener un gerente sms, nos basta con el primero de la relación
            kwargs['sms_managers']  = manager            
        if number > 1:
            kwargs["Manage_many"]       = True
            kwargs["select_a_company"]  = True
            #compañia que seleccione
            company                     = get_object_or_404(Company, id=self.kwargs.get("id_company"))
            kwargs["company"]           = company
            #todas las compañias
            companys                    = Company.objects.filter(company_sms_manager=manager)
            kwargs["companys"]          = companys
            kwargs['sms_managers']      = manager
            kwargs['employees']         = Employee.objects.filter(company=company)

        return super().get_context_data(**kwargs)

    def get_queryset(self):
        #obtengo id del manager
        id_ = self.request.user.id
        manager = get_object_or_404(SmsManager, user=id_)
        #obtengo cuantas compañias maneja el manager
        number = manager.managed_by.count() #"managed_by" es el related name definido en el modelo de compañia        
        if number == 1:
            company = manager.managed_by.first() #Como las compañias solo pueden tener un gerente sms, nos basta con el primero de la relación
            queryset = RiskReport.objects.filter(of_company=company).order_by('-id')
        if number > 1:
            context={}
            context["Manage_one"] = True
            context["select_a_company"] = True
            company = get_object_or_404(Company, id=self.kwargs.get("id_company"))            
            queryset = RiskReport.objects.filter(of_company=company)
        return queryset

class SmsManagerRiskReportListWithSearchView(ListView):
    model = RiskReport    
    paginate_by = 10
    context_object_name = 'risk_reports'
    template_name = 'managers/riskReports/SmsManager-RiskReportList.html'

    def get_queryset(self):
        id_ = self.request.user.id
        manager = get_object_or_404(SmsManager, user=id_)        
        company = manager.managed_by.first()
        my_search       = self.request.GET.get('my_search')        
        new_queryset    = RiskReport.objects.filter(of_company=company, description__unaccent__icontains=my_search).order_by('-id')
        return new_queryset

    def get_context_data(self, **kwargs):
        context                 = super(SmsManagerRiskReportListWithSearchView, self).get_context_data(**kwargs)
        context['my_search']    = self.request.GET.get('my_search')
        return context

class SmsManagerRiskReportDetailView(DetailView):
    template_name = 'managers/riskReports/SmsManager-RiskReportDetail.html'
    model         = RiskReport

    def get_context_data(self, **kwargs):
                # obtengo el reporte
        id_ = self.kwargs.get("id")        
        report = get_object_or_404(RiskReport, id=id_)
        #obtengo a quien creo el reporte
        owner = User.objects.get(email = report.owner)
        # logic
        if owner.is_employee:
            kwargs['reporter']      = get_object_or_404(Employee, user_id= owner.id)
            kwargs['employee']      = True
            kwargs['sms_manager']   = False
        if owner.is_sms_manager:
            kwargs['reporter']      = get_object_or_404(SmsManager, user_id= owner.id)
            kwargs['employee']      = False
            kwargs['sms_manager']   = True
        # obtengo al manager
        manager_id                 = self.request.user.id
        manager             = get_object_or_404(SmsManager, user=manager_id)        
        kwargs['manager']   = manager
        #obtengo el prestador de servicios
        company             = manager.managed_by.first()
        # obtengo los empleados de ese prestador de servicios
        kwargs['employees'] = Employee.objects.filter(company=company)
        # obtenemos las tareas asociadas a este reporte
        tasks = Task.objects.filter(report=report)                
        kwargs['tasks'] = tasks
        kwargs['allTasksCompleted'] = True
        for task in tasks:
            if task.completedTask == False:
                kwargs['allTasksCompleted'] = False
        return super().get_context_data(**kwargs)   

    def get_object(self):        
        id_ = self.kwargs.get("id")        
        return get_object_or_404(RiskReport, id=id_)

class SmsManagerCreateRiskReportView(CreateView):
    model = RiskReport    
    template_name = 'managers/riskReports/SmsManager-RiskReportCreate.html'
    form_class      = SmsManagerRiskReportForm
    context_object_name = 'risk_reports'

    def form_valid(self, form):                
        new_report = form.save(commit=False)
        new_report.owner = self.request.user
        #obtengo id del manager
        id_ = self.request.user.id
        manager = get_object_or_404(SmsManager, user=id_)
        #obtengo cuantas compañias maneja el manager
        number = manager.managed_by.count() #"managed_by" es el related name definido en el modelo de compañia
        if number == 0:        
            print('aun no gestiono nada')
        if number == 1:
            company = manager.managed_by.first() #Como las compañias solo pueden tener un gerente sms, nos basta con el primero de la relación            
            new_report.of_company = company
        if number > 1:        
            print('este manager gestiona varias empresas deberia seleccionar primero una empresa antes de crear un reporte')
        #despues de la logica anterior se guarda el reporte
        new_report.save() 
        # # email notification to manager
        # company         = new_report.of_company        
        # domain          = get_current_site(self.request).domain
        # link            = reverse('managers:risk-report-detail', kwargs={'id':new_report.id})
        # report_url      = 'http://'+domain+link        
        # email_subject   = '[Fagar-SMS] Has creado un reporte de riesgo para '+company.name
        # emai_body       = 'Has creado un reporte de riesgo.\n'+'Puedes revisarlo en el siguiente link: '+report_url        
        # send_mail(
        #     email_subject, 
        #     emai_body,
        #     #'noreply@fagar.com'
        #     'fg.sos.store@gmail.com',
        #     #['manager.user'], #recipients list
        #     ['fg.sos.store@gmail.com'],
        #     fail_silently=False,
        # )               
        return redirect('managers:risk-report-list')

class SmsManagerCloseReportView(UpdateView):        
    template_name = 'managers/modals/riskReportclose.html'       

    def post(self, request, *args, **kwargs):
         id_ = self.kwargs.get("id")
         report = get_object_or_404(RiskReport, id = id_)
         report.is_open = not report.is_open
         report.save()         
         return HttpResponseRedirect(reverse('managers:risk-report-detail', kwargs={'id' : id_}))

class SmsManagerUpdateLevelView(UpdateView):
    model = RiskReport    
    template_name = 'managers/modals/riskReportAddLevel.html'
    form_class      = SmsManagerAddLevelForm    

    def get_object(self):        
        id_ = self.kwargs.get("id")
        return get_object_or_404(RiskReport, id=id_)

    def get_success_url(self):
            id_ = self.kwargs.get("id")
            report = get_object_or_404(RiskReport, id=id_)
            probability = int(report.probability)
            consequence = int(report.consequence)
            report.level = probability*consequence
            if report.level >= 0 and report.level <= 3:
                report.level_of_risk = '1'
            if report.level >= 4 and report.level <= 7:
                report.level_of_risk = '2'
            if report.level >= 8 and report.level <= 14:
                report.level_of_risk = '3'
            if report.level >= 15 and report.level <= 25:
                report.level_of_risk = '4'
            report.save()
            messages.success(self.request, 'Establecido nivel de riesgo')
            return reverse('managers:risk-report-detail', kwargs={'id' : id_})

# ADD A NEW TASK TO SOME RISK REPORT
class SmsManagerUpdateTaskView(CreateView):
    model = Task    
    template_name = 'managers/modals/riskReportAddTask.html'
    form_class      = SmsManagerAddTaskForm

    def get_context_data(self, **kwargs):
        # obtengo el reporte
        rerport_id          = self.kwargs.get("id")
        report              = get_object_or_404(RiskReport, id=rerport_id) 
        kwargs['report']    = report
        # obtengo al manager
        id_                 = self.request.user.id
        manager             = get_object_or_404(SmsManager, user=id_)        
        kwargs['manager']   = manager
        #obtengo el prestador de servicios
        company             = manager.managed_by.first()
        # obtengo los empleados de ese prestador de servicios
        kwargs['employees'] = Employee.objects.filter(company=company)
        #super
        return super().get_context_data(**kwargs)       
    
    def form_valid(self, form):               
        new_task        = form.save(commit=False)
        id_             = self.kwargs.get("id")
        report          = get_object_or_404(RiskReport, id = id_)
        #
        new_task.report = report        
        userid          = self.request.POST['reponsable']
        user            = get_object_or_404(User, id = userid)
        #
        new_task.reponsable = user        
        if user.is_sms_manager == True:
            manager  = get_object_or_404(SmsManager, user_id = user.id)
            new_task.manager = manager            
        if user.is_employee == True:
            employee = get_object_or_404(Employee, user_id = user.id)
            new_task.employee = employee
        new_task.save()        
        messages.success(self.request, 'Tarea Agregada')                                
        # email notification
        # domain          = get_current_site(self.request).domain
        # link            = reverse('employees:task-list')        
        # report_url      = 'http://'+domain+link
        # if new_task.manager is not None:
        #     recipient       = new_task.manager.user
        #     email_subject   = '[Fagar-SMS] Te has asignado una tarea'
        #     emai_body       = 'Te ha asignado una tarea\n'+'Mirala en el listado de tareas pendientes: '+report_url        
        # if new_task.employee is not None:
        #     recipient = new_task.employee.user
        #     email_subject   = '[Fagar-SMS] El gerente SMS te ha asignado una tarea'
        #     emai_body       = 'El gerente SMS te ha asignado una tarea\n'+'Mirala en el listado de tareas pendientes: '+report_url                
        
        # send_mail(
        #     email_subject, 
        #     emai_body,
        #     'noreply@fagar.com'
        #     # 'fg.sos.store@gmail.com',
        #     ['recipient'], #recipients list
        #     # ['fg.sos.store@gmail.com'],
        #     fail_silently=False,
        # ) 
        return HttpResponseRedirect(reverse('managers:risk-report-detail', kwargs={'id' : self.kwargs.get("id")}))


###################################INCIDENTS-ACCIDENTS-VIEWS
class SmsManagerIncidentAccidentListView(ListView):
    model = IncidentAccident
    #ordering = ('name', ) #para ordenar por fecha quiza tengamos que cambiar a Generic date views
    paginate_by = 10
    context_object_name = 'incidents_accidents'
    template_name = 'managers/incidentsAndAccidents/SmsManager-IncidentAccidentList.html'

    def get_context_data(self, **kwargs):
        #obtengo id del manager
        id_ = self.request.user.id
        manager = get_object_or_404(SmsManager, user=id_)
        #obtengo cuantas compañias maneja el manager
        number = manager.managed_by.count() #"managed_by" es el related name definido en el modelo de compañia        
        if number == 1:
            kwargs["Manage_many"] = False
            company                 = manager.managed_by.first() #Como las compañias solo pueden tener un gerente sms, nos basta con el primero de la relación
            kwargs['sms_managers']  = manager
            kwargs['employees']     = Employee.objects.filter(company=company)
            kwargs['incidents']     = IncidentAccident.objects.filter(of_company=company, only_incident='1').order_by('-id')
            kwargs['accidents']     = IncidentAccident.objects.filter(of_company=company, only_incident='2').order_by('-id')
        if number > 1:
            kwargs["Manage_many"]       = True        
            kwargs["select_a_company"]  = True
            #compañia que seleccione
            company                     = get_object_or_404(Company, id=self.kwargs.get("id_company"))
            kwargs["company"]           = company
            #todas las compañias
            companys                    = Company.objects.filter(company_sms_manager=manager)
            kwargs["companys"]          = companys
            kwargs['sms_managers']      = manager
            kwargs['employees']         = Employee.objects.filter(company=company)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        #obtengo id del manager
        id_ = self.request.user.id
        manager = get_object_or_404(SmsManager, user=id_)
        #obtengo cuantas compañias maneja el manager
        number = manager.managed_by.count() #"managed_by" es el related name definido en el modelo de compañia        
        if number == 1:
            company = manager.managed_by.first() #Como las compañias solo pueden tener un gerente sms, nos basta con el primero de la relación
            queryset = IncidentAccident.objects.filter(of_company=company)
        if number > 1:
            context={}
            context["Manage_one"] = True
            context["select_a_company"] = True
            company = get_object_or_404(Company, id=self.kwargs.get("id_company"))            
            queryset = IncidentAccident.objects.filter(of_company=company)
        return queryset

class SmsManagerIncidentAccidentListWithSearchView(ListView):
    model               = IncidentAccident    
    paginate_by         = 10
    context_object_name = 'incidents_accidents'
    template_name       = 'managers/incidentsAndAccidents/SmsManager-IncidentAccidentList.html'

    def get_context_data(self, **kwargs):
        context                 = super(SmsManagerIncidentAccidentListWithSearchView, self).get_context_data(**kwargs)
        context['my_search']    = self.request.GET.get('my_search')        
        my_search               = self.request.GET.get('my_search')
        id_                     = self.request.user.id
        manager                 = get_object_or_404(SmsManager, user=id_)
        company                 = manager.managed_by.first() #Como las compañias solo pueden tener un gerente sms, nos basta con el primero de la relación
        kwargs['sms_managers']  = manager
        kwargs['employees']     = Employee.objects.filter(company=company)
        incidents               = IncidentAccident.objects.filter(of_company=company, only_incident='1', description__unaccent__icontains=my_search).order_by('-id')
        accidents               = IncidentAccident.objects.filter(of_company=company, only_incident='2', description__unaccent__icontains=my_search).order_by('-id')
        kwargs['incidents']     = incidents
        kwargs['accidents']     = accidents
        return super().get_context_data(**kwargs)


class SmsManagerIncidentAccidentDetailView(DetailView):
    template_name = 'managers/incidentsAndAccidents/SmsManager-IncidentAccidentDetail.html'
    model         = IncidentAccident

    def get_context_data(self, **kwargs):
        #obtengo el reporte
        id_ = self.kwargs.get("id")        
        report = get_object_or_404(IncidentAccident, id=id_)
        owner = User.objects.get(email = report.owner)        
        if owner.is_employee:
            kwargs['reporter']      = get_object_or_404(Employee, user_id= owner.id)
            kwargs['employee']      = True
            kwargs['sms_manager']   = False
        if owner.is_sms_manager:
            kwargs['reporter']      = get_object_or_404(SmsManager, user_id= owner.id)
            kwargs['employee']      = False
            kwargs['sms_manager']   = True
        
        return super().get_context_data(**kwargs)   

    def get_object(self):        
        id_ = self.kwargs.get("id")        
        return get_object_or_404(IncidentAccident, id=id_)

class SmsManagerCreateIncidentAccidentView(CreateView):
    model = IncidentAccident    
    template_name = 'managers/incidentsAndAccidents/SmsManager-IncidentAccidentCreate.html'
    form_class      = SmsManagerIncidentAccidentForm
    
    def form_valid(self, form):        
        new_report = form.save(commit=False)
        new_report.owner = self.request.user
        #obtengo id del manager
        id_ = self.request.user.id
        manager = get_object_or_404(SmsManager, user=id_)
        #obtengo cuantas compañias maneja el manager
        number = manager.managed_by.count() #"managed_by" es el related name definido en el modelo de compañia
        if number == 0:        
            print('aun no gestiono nada')
        if number == 1:
            company = manager.managed_by.first() #Como las compañias solo pueden tener un gerente sms, nos basta con el primero de la relación            
            new_report.of_company = company
        if number > 1:        
            print('este manager gestiona varias empresas deberia seleccionar primero una empresa antes de crear un reporte')
        #despues de la logica anterior se guarda el reporte
        new_report.save()   
        # email notification to manager
        # company         = new_report.of_company        
        # if new_report.only_incident == '1':
        #     type_report = 'incidente'
        # if new_report.only_incident == '2':
        #     type_report = 'accidente'
        # domain          = get_current_site(self.request).domain
        # link            = reverse('managers:incident-accident-detail', kwargs={'id':new_report.id})
        # report_url      = 'http://'+domain+link        
        # email_subject   = '[Fagar-SMS] Has creado un reporte de '+type_report+' para '+company.name
        # emai_body       = 'Has creado un reporte de '+type_report+'.\n'+'Puedes revisarlo en el siguiente link: '+report_url        
        # send_mail(
        #     email_subject, 
        #     emai_body,
        #     #'noreply@fagar.com'
        #     'noreply@fagar.com',
        #     #['manager.user'], #recipients list
        #     ['fg.sos.store@gmail.com'],
        #     fail_silently=False,
        # )
        return redirect('managers:incident-accident-list')

###################################################EMPLOYEE VIEWS
class SmsManagerEmployeeListView(ListView):
    model = Employee
    ordering = ('name')
    paginate_by = 10
    context_object_name = 'employees'
    template_name = 'managers/employees/SmsManager-EmployeeList.html'

    def get_context_data(self, **kwargs):
        #obtengo id del manager
        id_ = self.request.user.id
        manager = get_object_or_404(SmsManager, user=id_)
        #obtengo cuantas compañias maneja el manager
        number = manager.managed_by.count() #"managed_by" es el related name definido en el modelo de compañia        
        if number == 1:
            kwargs["Manage_many"] = False
            company                 = manager.managed_by.first() #Como las compañias solo pueden tener un gerente sms, nos basta con el primero de la relación
            kwargs['sms_managers']  = manager            
        if number > 1:
            kwargs["Manage_many"]       = True
            kwargs["select_a_company"]  = True
            #compañia que seleccione
            company                     = get_object_or_404(Company, id=self.kwargs.get("id_company"))
            kwargs["company"]           = company
            #todas las compañias
            companys                    = Company.objects.filter(company_sms_manager=manager)
            kwargs["companys"]          = companys
            kwargs['sms_managers']      = manager
            kwargs['employees']         = Employee.objects.filter(company=company)

        return super().get_context_data(**kwargs)

    def get_queryset(self):
        #obtengo id del manager
        id_ = self.request.user.id
        manager = get_object_or_404(SmsManager, user=id_)
        #obtengo cuantas compañias maneja el manager
        number = manager.managed_by.count()
        if number == 0:        
            print('aun no gestiono nada')
        if number == 1:
            #obtengo la unica compañia que se esta gestionado
            company = manager.managed_by.first()
            #selecciono solo a los empleados que pertenecen a esa compañia
            queryset = Employee.objects.filter(company=company)  
        if number > 1:        
            context={}            
            company = get_object_or_404(Company, id=self.kwargs.get("id_company"))            
            queryset = RiskReport.objects.filter(of_company=company)
        return queryset

class SmsManagerEmployeeListWithSearchView(ListView):
    model = Employee
    ordering = ('name')
    paginate_by = 10
    context_object_name = 'employees'
    template_name = 'managers/employees/SmsManager-EmployeeList.html'

    def get_queryset(self):
        id_ = self.request.user.id
        manager = get_object_or_404(SmsManager, user=id_)
        company = manager.managed_by.first()
        my_search       = self.request.GET.get('my_search')
        new_queryset    = Employee.objects.filter(company=company, name__unaccent__icontains=my_search)
        return new_queryset


class SmsManagerDetailEmployeeView(DetailView):
    template_name = 'managers/employees/SmsManager-EmployeeDetail.html'
    model           = Employee   

    def get_object(self):        
        id_ = self.kwargs.get("id")        
        return get_object_or_404(Employee, user=id_)

class SmsManagerDeleteEmployeeView(DeleteView):
    model = User
    template_name = 'managers/modals/employeeDelete.html'
        
    def get_success_url(self):        
        messages.success(self.request, 'Empleado Eliminado')        
        return reverse('managers:employee-list')

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(User, id=id_)

class SmsManagerCreateEmployeeView(CreateView):
    model = Employee
    form_class= SignupEmployeeForm    
    template_name = "managers/employees/SmsManager-EmployeeCreate.html"
  
    def form_valid(self, form):                
        user = form.save(commit=False)
        user.is_active = False
        user.is_employee = True
        user.password1 = ''
        user.password2 = ''
        user.save()              
        # begin activation by email
        uidb64          = urlsafe_base64_encode(force_bytes(user.pk))
        token           = token_generator.make_token(user)        
        domain          = get_current_site(self.request).domain
        link            = reverse('superuser:activation', kwargs={'uidb64':uidb64, 'token': token})
        activate_url    = 'http://'+domain+link
        email_subject   = '[Fagar-SMS] Activa y establece un contraseña para tu cuenta'
        emai_body       = 'Bienvenido activa tu cuenta haciendo click en el siguiente link\n'+activate_url
        send_mail(
            email_subject, 
            emai_body,
            'noreply@fagarsms.com',
            #[user], #recipients list
            ['fg.sos.store@gmail.com'],
            fail_silently=False,
        )
        #obtengo el manager
        id_ = self.request.user.id
        manager = get_object_or_404(SmsManager, user=id_)
        company = manager.managed_by.first()
        employee = Employee.objects.create(user=user, company=company)    
        employee.save()
        messages.success(self.request, 'Empleado Creado')
        return redirect('managers:employee-list')

class SmsManagerEmployeeProfileUpdate(UpdateView):
    model = Employee
    template_name = 'managers/modals/managerUpdateProfile.html'
    form_class = EmployeeProfileFormModal

    def get_object(self, **kwargs):
        id_     = self.kwargs.get("id")
        print(id_)                
        return get_object_or_404(Employee, user_id=id_)            

    def get_success_url(self):
            messages.success(self.request, 'Cambio de perfil exitoso')
            return reverse('superuser:employee-list')


class SmsManagerEmployeeProfilePicUpdateView(UpdateView):
    model           = Employee
    template_name   = 'managers/modals/managerProfilePicture.html'
    form_class      = EmployeeProfilePicFormModal    

    def get_object(self):                
        id_     = self.kwargs.get("id")
        return get_object_or_404(Employee, user_id=id_)    

    def get_success_url(self):
        messages.success(self.request, 'Cambio de imagen de perfil exitoso')
        return reverse('superuser:employee-list')
