from django.urls import reverse

from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse

from django.contrib import messages

from django.contrib.auth import get_user_model, login, logout

from django.contrib.auth.models import User

from django.db.models import Count
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
    ListView,
    DeleteView,
    FormView
)

from users.models import User, SmsManager, Company, Employee

from .forms import (
    SignupSmsManagerForm,
    SignupEmployeeForm,
    CreateCompanyForm, 
    SmsManagerProfileFormModal, 
    SmsManagerProfilePicFormModal,
    EmployeeProfileFormModal,
    EmployeeProfilePicFormModal,
    UserUpdatePassWordForm,
)

class AdminDashboardView(View):
    template_name = "superuser/AdminDashboard.html"    

    def get(self, request, *args, **kwargs):
        # GET method
        context={}                
        return render(request, self.template_name, context)

#SMS MANAGERS VIEWS

class AdminSmsManagerListView(ListView):
    model = SmsManager
    ordering = ('name', )
    paginate_by = 10
    context_object_name = 'sms_managers'
    template_name = 'superuser/smsManager/smsManagerList.html'

    def get_queryset(self):
        queryset = SmsManager.objects.all()        
        return queryset

class AdminDetailSmsManagerView(DetailView):
    template_name = 'superuser/smsManager/smsManagerDetail.html'
    model           = SmsManager   

    def get_object(self):        
        id_ = self.kwargs.get("id")        
        return get_object_or_404(SmsManager, user=id_)

class AdminCreateSmsManagerView(CreateView):
    model = SmsManager
    form_class = SignupSmsManagerForm
    template_name = "superuser/smsManager/smsManagerCreate.html"

    def form_valid(self, form):                            
        user = form.save(commit=False)
        user.is_active = False #por ahora
        user.is_sms_manager = True
        user.password1 = ''
        user.password2 = ''
        user.save()        
        # begin activation by email
        uidb64          = urlsafe_base64_encode(force_bytes(user.pk))
        token           = token_generator.make_token(user)        
        domain          = get_current_site(self.request).domain
        link            = reverse('superuser:activation', kwargs={'uidb64':uidb64, 'token': token})
        activate_url    = 'http://'+domain+link
        email_subject   = '[Fagar-SMS] Activa y establece un contraseña para tu cuenta de Gerente SMS'
        emai_body       = 'Bienvenido activa tu cuenta de Gerente SMS haciendo click en el siguiente link\n'+activate_url
        send_mail(
            email_subject, 
            emai_body,
            'noreply@fagarsms.com',
            #[user], #recipients list
            ['fg.sos.store@gmail.com'],
            fail_silently=False,
        )                
        #CreoAlGerenteSMS
        sms_manager = SmsManager.objects.create(user=user)
        messages.success(self.request, 'Gerente SMS Creado')
        return redirect('superuser:sms-manager-list')

class AdminUpdateSmsManagerView(UpdateView):
    model = SmsManager
    form_class = SignupSmsManagerForm
    template_name = "superuser/smsManager/smsManagerCreate.html"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(SmsManager, user_id=id_)

    def form_valid(self, form):            
        user = form.save(commit=True)            
        user.is_sms_manager = True
        #GuardoElUsuario
        user.save()    
        #CreoAlGerenteSMS
        sms_manager = SmsManager.objects.create(user=user)         
        return redirect('superuser:sms-manager-list')

class AdminUpdateSmsManagerProfileView(UpdateView):
    model = SmsManager
    template_name = 'superuser/smsManager/modals/smsMangerUpdateProfile.html'
    form_class = SmsManagerProfileFormModal

    def get_object(self, **kwargs):        

        id_     = self.kwargs.get("id")
        print(id_)                
        return get_object_or_404(SmsManager, user_id=id_)            

    def get_success_url(self):
            messages.success(self.request, 'Cambio de perfil exitoso')
            return reverse('superuser:sms-manager-list')

class AdminUpdateSmsManagerProfilePictureView(UpdateView):
    model           = SmsManager
    template_name   = 'superuser/smsManager/modals/smsMangerUpdateProfilePicture.html'
    form_class      = SmsManagerProfilePicFormModal    

    def get_object(self):                
        id_     = self.kwargs.get("id")
        return get_object_or_404(SmsManager, user_id=id_)    

    def get_success_url(self):
        messages.success(self.request, 'Cambio de imagen de perfil exitoso')
        return reverse('superuser:sms-manager-list')

#COMPANYS VIEWS

class AdminCompanyListView(ListView):
    model = Company
    ordering = ('name')
    paginate_by = 10
    context_object_name = 'companys'
    template_name = 'superuser/organization/organizationList.html'

    def get_queryset(self):
        queryset = Company.objects.all()        
        return queryset

class AdminDetailCompanyView(DetailView):
    template_name = 'superuser/organization/organizationDetail.html'
    model         = Company   

    def get_object(self):        
        id_ = self.kwargs.get("id")        
        return get_object_or_404(Company, id=id_)

class AdminCreateCompanyView(CreateView):
    model = Company
    form_class= CreateCompanyForm    
    template_name = "superuser/organization/organizationCreate.html"
  
    def get_context_data(self, **kwargs):
        # managers = SmsManager.objects.all()
        # a limitation for only return managers that have 0 companies
        managers = SmsManager.objects.annotate(Count('managed_by')).filter(managed_by__count__lt=1)        
        # 
        kwargs['sms_managers'] = managers
        return super().get_context_data(**kwargs)       

    def form_valid(self, form):        
        new_company = form.save()        
        new_company.save()
        return redirect('superuser:company-list')

class AdminUpdateCompanyView(UpdateView):
    model = Company
    form_class= CreateCompanyForm    
    template_name = "superuser/organization/organizationCreate.html"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Company, id=id_)

    def get_context_data(self, **kwargs):
        # managers = SmsManager.objects.all()
        # a limitation for only return managers that have 0 companies
        managers = SmsManager.objects.annotate(Count('managed_by')).filter(managed_by__count__lt=1)        
        # 
        kwargs['sms_managers'] = managers
        return super().get_context_data(**kwargs)       

    def form_valid(self, form):        
        new_company = form.save()        
        new_company.save()
        return redirect('superuser:company-list')

#EMPLOYEE VIEWS

class AdminEmployeeListView(ListView):
    model = Employee
    ordering = ('name')
    paginate_by = 10
    context_object_name = 'employees'
    template_name = 'superuser/employee/employeeList.html'

    def get_queryset(self):
        queryset = Employee.objects.all()        
        return queryset

class AdminDetailEmployeeView(DetailView):
    template_name = 'superuser/employee/employeeDetail.html'
    model           = Employee   

    def get_object(self):        
        id_ = self.kwargs.get("id")        
        return get_object_or_404(Employee, user=id_)

class AdminCreateEmployeeView(CreateView):
    model = Employee
    form_class= SignupEmployeeForm    
    template_name = "superuser/employee/employeeCreate.html"
  
    def form_valid(self, form):         
        user = form.save(commit=False)
        user.is_active = False #por ahora
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
        #obtengo la compañia seleccionada
        selected_company = form.cleaned_data.get('companys') #aqui obtengo el objeto company y puedo comprabarlo con print(selected_company.id) o print(selected_company)        
        employee = Employee.objects.create(user=user, company=selected_company)
        employee.save()
        messages.success(self.request, 'Empleado Creado')
        return redirect('superuser:employee-list')

class AdminUpdateEmployeeProfileView(UpdateView):
    model = Employee
    template_name = 'superuser/employee/modals/employeeUpdateProfile.html'
    form_class = EmployeeProfileFormModal

    def get_object(self, **kwargs):
        id_     = self.kwargs.get("id")
        print(id_)                
        return get_object_or_404(Employee, user_id=id_)            

    def get_success_url(self):
            messages.success(self.request, 'Cambio de perfil exitoso')
            return reverse('superuser:employee-list')

class AdminUpdateEmployeeProfilePictureView(UpdateView):
    model           = Employee
    template_name   = 'superuser/employee/modals/employeeUpdateProfilePicture.html'
    form_class      = EmployeeProfilePicFormModal    

    def get_object(self):                
        id_     = self.kwargs.get("id")
        return get_object_or_404(Employee, user_id=id_)    

    def get_success_url(self):
        messages.success(self.request, 'Cambio de imagen de perfil exitoso')
        return reverse('superuser:employee-list')

class VerificationView(View):

    def get(self, request, uidb64, token):
        try:            
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)            
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None        
        if user is not None and token_generator.check_token(user, token):
            # activate user and login:
            user.is_active = True
            user.save()
            login(request, user)            
            return render(request, 'superuser/activation/activationValid.html')
        else:
            return HttpResponse('¡Link invalido o expirado!')

    def post(self, request):
        form = UserUpdatePassWordForm(request.POST)
        if form.is_valid():
            print("form valid")
            #user = form.save()
            user = self.request.user
            print("got user")
            print(user)
            print(form.cleaned_data['password1'])
            user.set_password(form.cleaned_data['password1'])
            print("password was set")
            user.save()
            #update_session_auth_hash(request, user) # Important, to update the session with the new password
            return HttpResponse('Password changed successfully')

class ActivationFormView(UpdateView):
    model           = User
    template_name   = 'superuser/activation/activationValid.html'
    form_class      = UserUpdatePassWordForm 

    def get_object(self):                
        id_     = self.kwargs.get("id")
        return get_object_or_404(Employee, user_id=id_)   
