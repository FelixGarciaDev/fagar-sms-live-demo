from django.db import models
from django.db.models.signals import post_save

from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

from django.utils.translation import ugettext_lazy as _

from django.dispatch import receiver

#USERMANAGER esto para usar el correo electronico como identificador de usuario
class MyUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)        
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

#Clase basica para tener varios tipos de usuarios
class User(AbstractBaseUser, PermissionsMixin):
    email           = models.EmailField(unique=True, blank=False)
    #flags que determinan el rol del usuario
    is_sms_manager	= models.BooleanField(default=False)
    is_employee	= models.BooleanField(default=False)
    #flag staff
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_('Do you think you can be a Superuser?'),
    )
    #flag staff
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )
    #falg activo
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )    
    
    USERNAME_FIELD = 'email'

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

#Clase para los gerentes SMS
class SmsManager(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name        = models.CharField(max_length=50)
    last_name   = models.CharField(max_length=50)    
    #ci          = models.IntegerField(unique=True)
    career      = models.CharField(max_length=50, default='')     
    phone       = models.PositiveBigIntegerField(null=False, default=0)
    photo       = models.ImageField(upload_to='sms_managers/profile_pics/', default='sms_managers/profile_pics/default_user_profile_pic.png')    

TYPE_OF_COMPANY = (
    ('1', 'Airport'),#Aeropuerto
    ('2', 'Aeroline'),#Personas Juridicas
    ('3', 'ciac'),#centro de instrucción
    ('4', 'omac'),#Taller OMAC    
)

class Company(models.Model):
    #todo compañia debe tener un gerente sms
    #tambien muchas compañias pueden tener un mismo gerete sms
    company_sms_manager = models.ForeignKey(SmsManager, on_delete=models.CASCADE, related_name='managed_by')
    name                = models.CharField(max_length=100)
    type_of_company     = models.CharField(max_length=1, choices=TYPE_OF_COMPANY, blank=True)
    #rav_type           = models.CharField(max_length=1, choices=TYPE_OF_RAP, blank=True)
    #una compañia puede tener mas de rav
    #hay regulaciones por otros paises rap (peru), far(estados unidos), etc
    #rav_number         = models.IntegerField(null=False, default=0)
    phone               = models.PositiveBigIntegerField(null=False, default=0)
    company_logo        = models.ImageField(upload_to='companys/company_logos/', default='companys/company_logos/default_company_logo.png')
    rif                 = models.PositiveBigIntegerField(null=False, default=0)
    company_mail        = models.EmailField(blank=False, default='mail@mail.com')

class Employee(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    #muchos empleados pertenecen a una compañia
    company     = models.ForeignKey(Company, on_delete=models.CASCADE, related_name = 'employee_of_company', default = False)
    name        = models.CharField(max_length=50)
    last_name   = models.CharField(max_length=50)    
    phone       = models.PositiveBigIntegerField(null=False, default=0)
    photo       = models.ImageField(upload_to='employees/profile_pics/', default='employees/profile_pics/default_user_profile_pic.png')    

TYPE_OF_RISK = (
    ('1', 'Relacionado con vuelo'),
    ('2', 'E.P.P. (Equipos de protección personal)'),
    ('3', 'Procedimientos'),
    ('4', 'Mantenimiento Aeronáutico'),
    ('5', 'FOD (Objetos extraños)'),
    ('6', 'Orden y limpieza'),
    ('7', 'Acto inseguro'),
    ('8', 'Otros'),
)

LEVEL_OF_RISK = (
    ('1', 'Aceptable'),
    ('2', 'Moderado'),
    ('3', 'Alto'),
    ('4', 'Extremo')    
)

PROBABILITY = (
    ('1', 'Improbable'),
    ('2', 'Remoto'),
    ('3', 'Ocasional'),    
    ('4', 'Frecuente'),
    ('5', 'Probable'),
)

CONSEQUENCE = (
    ('1', 'Insignificante'),
    ('2', 'Menor'),
    ('3', 'Moderado'),    
    ('4', 'Grave'),
    ('5', 'Catastrofico'), 
)


class RiskReport(models.Model):
    owner           = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_of_owner')
    of_company      = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='reports_of_company')
    create_at_date  = models.DateTimeField(auto_now_add=True)    
    date            = models.DateField()
    place           = models.CharField(max_length=100)
    type_of_risk    = models.CharField(max_length=1, choices=TYPE_OF_RISK, blank=True)
    photo1          = models.ImageField(upload_to='risk_reports/', default='risk_reports/risk.png')
    photo2          = models.ImageField(upload_to='risk_reports/', default='risk_reports/risk.png')
    photo3          = models.ImageField(upload_to='risk_reports/', default='risk_reports/risk.png')
    photo4          = models.ImageField(upload_to='risk_reports/', default='risk_reports/risk.png')
    photo5          = models.ImageField(upload_to='risk_reports/', default='risk_reports/risk.png')
    description     = models.TextField(blank=True)
    recmendations   = models.TextField(blank=True, default='')
    is_open         = models.BooleanField(default=True)
    level_of_risk   = models.CharField(max_length=1, choices=LEVEL_OF_RISK, blank=True)
    probability     = models.CharField(max_length=1, choices=PROBABILITY, blank=True)
    consequence     = models.CharField(max_length=1, choices=PROBABILITY, blank=True)            
    level           = models.IntegerField(null=False, default=0)
     
INCIDENT_OR_ACCIDENT = (
    ('1', 'Incidente'),
    ('2', 'Accidente'),
)

class IncidentAccident(models.Model):
    owner           = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incident_accident_of_owner')
    of_company      = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='incident_accident_of_company')
    create_at_date  = models.DateTimeField(auto_now_add=True)
    only_incident   = models.CharField(max_length=1, choices=INCIDENT_OR_ACCIDENT, default='1')
    date            = models.DateField()
    place           = models.CharField(max_length=100)    
    photo1          = models.ImageField(upload_to='incidents_accidents/', default='incidents_accidents/incident_accident.jpg')
    photo2          = models.ImageField(upload_to='incidents_accidents/', default='incidents_accidents/incident_accident.jpg')
    photo3          = models.ImageField(upload_to='incidents_accidents/', default='incidents_accidents/incident_accident.jpg')
    photo4          = models.ImageField(upload_to='incidents_accidents/', default='incidents_accidents/incident_accident.jpg')
    photo5          = models.ImageField(upload_to='incidents_accidents/', default='incidents_accidents/incident_accident.jpg')
    description     = models.TextField(blank=True)

class Task(models.Model):    
    assigned_date   = models.DateTimeField(auto_now_add=True)    
    report          = models.ForeignKey(RiskReport, on_delete=models.CASCADE, related_name='task_of_report')
    reponsable      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_of_user')
    manager         = models.ForeignKey(SmsManager, on_delete=models.CASCADE, related_name='task_of_manager', null=True)
    employee        = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='task_of_employee', null=True)
    taskDescription = models.TextField(blank=False)
    completedTask   = models.BooleanField(default=False)
    completed_date  = models.DateTimeField(blank=True, null=True)    