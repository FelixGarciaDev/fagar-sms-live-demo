from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, reverse_lazy

from .views import (    	
    SmsManagerDashboardView,
    SmsManagerProfileView,
    SmsManagerProfileUpdate,
    SmsManagerProfilePicUpdateView,
    SmsManagerRiskReportListView,
    SmsManagerRiskReportListWithSearchView,
    SmsManagerRiskReportDetailView,
    SmsManagerCloseReportView,
    SmsManagerUpdateLevelView,
    SmsManagerUpdateTaskView,
    SmsManagerCreateRiskReportView,
    SmsManagerIncidentAccidentListView,
    SmsManagerIncidentAccidentListWithSearchView,
    SmsManagerIncidentAccidentDetailView,
    SmsManagerCreateIncidentAccidentView,
    SmsManagerEmployeeListView,
    SmsManagerEmployeeListWithSearchView,
    SmsManagerDetailEmployeeView,
    SmsManagerCreateEmployeeView, 
    SmsManagerDeleteEmployeeView, 
    SmsManagerEmployeeProfileUpdate,
    SmsManagerEmployeeProfilePicUpdateView,  
)

from .taskViews import (
    SmsManagerTaskListView,   
    SmsManagerUpdateTaskStatusView,
)

app_name = 'managers'

urlpatterns = [    
    path('sms-manager/dashboard/', SmsManagerDashboardView.as_view(), name='dashboard'),
    path('sms-manager/dashboard/profile/', SmsManagerProfileView.as_view(), name='profile'),
    path('sms-manager/dashboard/profile-update/', SmsManagerProfileUpdate.as_view(), name='update-profile'),
    path('sms-manager/dashboard/profile-pic_update/', SmsManagerProfilePicUpdateView.as_view(), name='update-profile-pic'),    
    # RISK REPORTS
    path('sms-manager/dashboard/risk-report-list/', SmsManagerRiskReportListView.as_view(), name='risk-report-list'),
    path('sms-manager/dashboard/risk-report-search/', SmsManagerRiskReportListWithSearchView.as_view(), name='risk-report-search'),
    path('sms-manager/dashboard/risk-report-detail/<int:id>/', SmsManagerRiskReportDetailView.as_view(), name='risk-report-detail'),
    path('sms-manager/dashboard/risk-report-close/<int:id>/', SmsManagerCloseReportView.as_view(), name='risk-report-close'),
    # LEVEL AND TASK FOR RISK REPORTE
    path('sms-manager/dashboard/risk-report-level-update/<int:id>/', SmsManagerUpdateLevelView.as_view(), name='risk-report-level'),
    path('sms-manager/dashboard/risk-report-task-update/<int:id>/', SmsManagerUpdateTaskView.as_view(), name='risk-report-task'),    
    path('sms-manager/dashboard/risk-report-create/', SmsManagerCreateRiskReportView.as_view(), name='risk-report-create'),
    # INCIDENTS ACCIDENTS
    path('sms-manager/dashboard/incident-accident-list/', SmsManagerIncidentAccidentListView.as_view(), name='incident-accident-list'),
    path('sms-manager/dashboard/incident-accident-search/', SmsManagerIncidentAccidentListWithSearchView.as_view(), name='incident-accident-search'),
    path('sms-manager/dashboard/incident-accident-detial/<int:id>/', SmsManagerIncidentAccidentDetailView.as_view(), name='incident-accident-detail'),
    path('sms-manager/dashboard/incident-accident-create/', SmsManagerCreateIncidentAccidentView.as_view(), name='incident-accident-create'),
    # EMPLOYEES
    path('sms-manager/dashboard/employees-list/', SmsManagerEmployeeListView.as_view(), name='employee-list'),
    path('sms-manager/dashboard/employees-search/', SmsManagerEmployeeListWithSearchView.as_view(), name='employee-search'),    
    path('sms-manager/dashboard/employee-detail/<int:id>/', SmsManagerDetailEmployeeView.as_view(), name='employee-detail'),
    path('sms-manager/dashboard/employee-create/', SmsManagerCreateEmployeeView.as_view(), name='employee-create'),
    path('sms-manager/dashboard/employee-delete/<int:id>/', SmsManagerDeleteEmployeeView.as_view(), name='employee-delete'),    
    path('sms-manager/dashboard/employee-profile-update/<int:id>/', SmsManagerEmployeeProfileUpdate.as_view(), name='employee-update-profile'),
    path('sms-manager/dashboard/employee-profile-pic_update/<int:id>/', SmsManagerEmployeeProfilePicUpdateView.as_view(), name='employee-update-profile-pic'),
    #task, defenses views
    path('sms-manager/dashboard/task-list/', SmsManagerTaskListView.as_view(), name='task-list'),
    path('sms-manager/dashboard/task-status-update/<int:id>/', SmsManagerUpdateTaskStatusView.as_view(), name='task-update'),    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)