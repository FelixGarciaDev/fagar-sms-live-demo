from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, reverse_lazy

from .views import (    	
    EmployeeDashboardView,
    
    EmployeeProfileView,
    EmployeeProfileUpdate, #for basic data
    EmployeeProfilePicUpdateView, #for only the profile picture
    EmployeeRiskReportListView, #El empleado solo debe ver los reportes hechos por el mismo
    EmployeeRiskReportListWithSearchView,
    EmployeeRiskReportDetailView,
    EmployeeCreateRiskReportView,
    EmployeeIncidentAccidentListView,
    EmployeeIncidentAccidentListWithSearchView,
    EmployeeIncidentAccidentDetailView,
    EmployeeCreateIncidentAccidentView,
    EmployeeTaskListView,
    EmployeeUpdateTaskStatusView,
)

app_name = 'employees'

urlpatterns = [    
    path('employee/dashboard/', EmployeeDashboardView.as_view(), name='dashboard'),
    path('employee/dashboard/profile/', EmployeeProfileView.as_view(), name='profile'),
    path('employee/dashboard/profile_update/', EmployeeProfileUpdate.as_view(), name='update-profile'),
    path('employee/dashboard/profile_pic_update/', EmployeeProfilePicUpdateView.as_view(), name='update-profile-pic'),
    path('employee/dashboard/risk-report-list/', EmployeeRiskReportListView.as_view(), name='risk-report-list'),
    path('employee/dashboard/risk-report-search/', EmployeeRiskReportListWithSearchView.as_view(), name='risk-report-search'),    
    path('employee/dashboard/risk-report-detial/<int:id>/', EmployeeRiskReportDetailView.as_view(), name='risk-report-detail'),
    path('employee/dashboard/risk-report-create/', EmployeeCreateRiskReportView.as_view(), name='risk-report-create'),    
    path('employee/dashboard/incident-accident-list/', EmployeeIncidentAccidentListView.as_view(), name='incident-accident-list'),
    path('employee/dashboard/incident-accident-search/', EmployeeIncidentAccidentListWithSearchView.as_view(), name='incident-accident-search'),    
    path('employee/dashboard/incident-accident-detial/<int:id>/', EmployeeIncidentAccidentDetailView.as_view(), name='incident-accident-detail'),
    path('employee/dashboard/incident-accident-create/', EmployeeCreateIncidentAccidentView.as_view(), name='incident-accident-create'),
    #task, defenses views
    path('employee/dashboard/task-list/', EmployeeTaskListView.as_view(), name='task-list'),
    path('employee/dashboard/task-status-update/<int:id>/', EmployeeUpdateTaskStatusView.as_view(), name='task-update'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)