from django import forms
from users.models import SmsManager, RiskReport, Employee, IncidentAccident

class EmployeeProfileFormModal(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ['name', 'last_name', 'phone']

class EmployeePicFormModal(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ['photo',]


class EmployeeRiskReportForm(forms.ModelForm):

    class Meta:
        model = RiskReport
        fields = ['date', 'place', 'type_of_risk', 'photo1', 'photo2', 'photo3', 'photo4', 'photo5', 'description', 'recmendations',]  
        """widgets = {
          'description': forms.Textarea(attrs={'rows':20, 'cols':15}),
        }"""

    #esto sirve para añadir class a un field del form
    def __init__(self, *args, **kwargs):
        super(EmployeeRiskReportForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs\
            .update({                
                'class': 'materialize-textarea'
            })
        self.fields['recmendations'].widget.attrs\
            .update({                
                'class': 'materialize-textarea'
            })

class EmployeeIncidentAccidentForm(forms.ModelForm):

    class Meta:
        model = IncidentAccident
        fields = ['date', 'only_incident','place', 'photo1', 'photo2', 'photo3', 'photo4', 'photo5', 'description',]        

    #esto sirve para añadir class a un field del form
    def __init__(self, *args, **kwargs):
        super(EmployeeIncidentAccidentForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs\
            .update({                
                'class': 'materialize-textarea'
            })