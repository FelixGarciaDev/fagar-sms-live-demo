from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, reverse_lazy

from .views import (    	
    AdminDashboardView,
    AdminSmsManagerListView,
    AdminDetailSmsManagerView,
    AdminCreateSmsManagerView,    
    AdminUpdateSmsManagerView,
    AdminUpdateSmsManagerProfileView,
    AdminUpdateSmsManagerProfilePictureView,
    AdminCompanyListView,
    AdminDetailCompanyView,
    AdminCreateCompanyView,
    AdminUpdateCompanyView,
    AdminEmployeeListView,
    AdminDetailEmployeeView,
    AdminCreateEmployeeView,
    AdminUpdateEmployeeProfileView,
    AdminUpdateEmployeeProfilePictureView,
    VerificationView,
    ActivationFormView,
)

app_name = 'superuser'

urlpatterns = [
    # start    
    path('dashboard/', AdminDashboardView.as_view(), name='dashboard'),
    # manager urls
    path('dashboard/sms-managers-list/', AdminSmsManagerListView.as_view(), name='sms-manager-list'),
    path('dashboard/sms-manager-detail/<int:id>/', AdminDetailSmsManagerView.as_view(), name='sms-manager-detail'),    
    path('dashboard/sms-manager-create/', AdminCreateSmsManagerView.as_view(), name='sms-manager-create'),    
    path('dashboard/sms-manager-update/<int:id>/', AdminUpdateSmsManagerView.as_view(), name='sms-manager-update'),
    path('dashboard/sms-manager-update-profile/<int:id>/', AdminUpdateSmsManagerProfileView.as_view(), name='sms-manager-update-profile'),
    path('dashboard/sms-manager-update-profile-picture/<int:id>/', AdminUpdateSmsManagerProfilePictureView.as_view(), name='sms-manager-update-profile-pic'),    
    # company urls
    path('dashboard/companys-list/', AdminCompanyListView.as_view(), name='company-list'),
    path('dashboard/comapny-detail/<int:id>/', AdminDetailCompanyView.as_view(), name='company-detail'),
    path('dashboard/company-create/', AdminCreateCompanyView.as_view(), name='company-create'),
    path('dashboard/company-update/<int:id>/', AdminUpdateCompanyView.as_view(), name='company-update'),
    # employee urls
    path('dashboard/employees-list/', AdminEmployeeListView.as_view(), name='employee-list'),
    path('dashboard/employee-detail/<int:id>/', AdminDetailEmployeeView.as_view(), name='employee-detail'),
    path('dashboard/employee-create/', AdminCreateEmployeeView.as_view(), name='employee-create'),
    path('dashboard/employee-update-profile/<int:id>/', AdminUpdateEmployeeProfileView.as_view(), name='employee-update-profile'),
    path('dashboard/employee-update-profile-picture/<int:id>/', AdminUpdateEmployeeProfilePictureView.as_view(), name='employee-update-profile-pic'),
    # user activation urls works for manager and employee
    path('activation/<uidb64>/<token>/', VerificationView.as_view(), name='activation'),
    path('activation/changepassword/', VerificationView.as_view(), name='activation-change-password'),
    path('activationform/form/<int:id>/', ActivationFormView.as_view(), name='activation-form')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)