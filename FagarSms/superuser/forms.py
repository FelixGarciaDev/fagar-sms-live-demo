from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from users.models import User, SmsManager, Employee, Company

class SignupSmsManagerForm(ModelForm):
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
	"""
	#Override clean method to check 
	def clean(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		if password1 and password1 != password2:			
			raise forms.ValidationError("The two password fields must match.")

		return self.cleaned_data"""

class SignupEmployeeForm(ModelForm):
	companys 	= forms.ModelChoiceField(queryset=Company.objects.all(), empty_label="Debe seleccionar una empresa")
	email 		= forms.EmailField(max_length=300, help_text='Required')	

	class Meta(UserCreationForm.Meta):
		model = User
		fields = ('companys', 'email',)

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
	"""
	#Override clean method to check 
	def clean(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		if password1 and password1 != password2:			
			#raise forms.ValidationError("Las dos contraseñas deben coincidir")
			#raise forms.ValidationError({'password1': ["Passwords must be the same."]})

		return self.cleaned_data"""

class UserUpdatePassWordForm(ModelForm):
	password1 	= forms.CharField(label="",max_length=50,min_length=8, widget=forms.PasswordInput())
	password2 	= forms.CharField(label="",max_length=50,min_length=8, widget=forms.PasswordInput())

	class Meta:
		model 	= User
		fields 	= ('password1','password2',)

	#Override clean method to check 
	def clean(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		if password1 and password1 != password2:			
			raise forms.ValidationError("Las dos contraseñas deben coincidir")

		return self.cleaned_data


class CreateCompanyForm(ModelForm):
	class Meta:
		model 	= Company
		fields 	= ('company_sms_manager','name', 'company_logo', 'type_of_company', 'phone', 'company_mail', 'rif')



# MODAL FORMS
# 
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