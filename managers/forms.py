from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from users.models import User, SmsManager, Employee, RiskReport, Company, IncidentAccident, Task

class SmsManagerProfileFormModal(forms.ModelForm):

    class Meta:
        model = SmsManager
        fields = ['name', 'last_name', 'phone']

class SmsManagerProfilePicFormModal(forms.ModelForm):

    class Meta:
        model = SmsManager
        fields = ['photo',]

class EmployeeProfileFormModal(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ['name', 'last_name', 'phone']

class EmployeeProfilePicFormModal(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ['photo',]

#CREAR REPORTE DE RIESGO
class SmsManagerRiskReportForm(forms.ModelForm):

    class Meta:
        model = RiskReport
        fields = ['date', 'place', 'type_of_risk', 'photo1', 'photo2', 'photo3', 'photo4', 'photo5', 'description', 'recmendations',]          

    #esto sirve para añadir class a un field del form
    def __init__(self, *args, **kwargs):
        super(SmsManagerRiskReportForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs\
            .update({                
                'class': 'materialize-textarea'
            })
        self.fields['recmendations'].widget.attrs\
            .update({                
                'class': 'materialize-textarea'
            })

#CREAR INCIDENTE / ACCIDENTE
class SmsManagerIncidentAccidentForm(forms.ModelForm):

    class Meta:
        model = IncidentAccident
        fields = ['date', 'only_incident','place', 'photo1', 'photo2', 'photo3', 'photo4', 'photo5', 'description',]  
    
    def __init__(self, *args, **kwargs):
        super(SmsManagerIncidentAccidentForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs\
            .update({                
                'class': 'materialize-textarea'
            })

# ADD LEVEL

class SmsManagerAddLevelForm(forms.ModelForm):

    class Meta:
        model = RiskReport
        fields = ['probability', 'consequence']  

class SmsManagerAddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['reponsable','taskDescription',]

    def __init__(self, *args, **kwargs):
        super(SmsManagerAddTaskForm, self).__init__(*args, **kwargs)
        self.fields['taskDescription'].widget.attrs\
            .update({                
                'class': 'materialize-textarea'
            })         

    
#CREAR EMPLEADO
class SignupEmployeeForm(ModelForm):	
	email 		= forms.EmailField(max_length=300, help_text='Required')	

	class Meta(UserCreationForm.Meta):
		model = User
		fields = ('email',)

    #Chequeamos que el mail no exista (ya registrado)
	def clean_email(self):
		# Get the email
		email = self.cleaned_data.get('email')

		# Check to see if any users already exist with this email as a username.
		try:
			match = User.objects.get(email=email)
		except User.DoesNotExist:
			# Unable to find a user, this is fine
			return email

		# A user was found with this as a username, raise an error.
		raise forms.ValidationError('Esta dirección de correo ya esta en uso')