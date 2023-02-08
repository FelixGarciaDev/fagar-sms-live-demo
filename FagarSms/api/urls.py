from django.urls import path, include
from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    LogoutUserAPIView,
    ProfileAPIView,
    apiOverview,
    riskReportList,
    riskReportDetail,
    riskReportCreate,
    incidentAccidentList,
    incidentAccidentDetail,
    incidentAccidentCreate,
)

app_name = 'api'

urlpatterns = [
    # API ENTRY POINT
    path('', apiOverview, name="api-overview"),
    # API RISK REPORT MODEL RELEATED ACTIONS
    path('report-list/', riskReportList, name="report-list"),
	path('report-detail/<str:pk>/', riskReportDetail, name="report-detail"),
    path('report-create/', riskReportCreate, name="report-create"),
    # API INCIDENT/ACCIDENT MODEL RELEATED ACTIONS
    path('incident-accident-list/', incidentAccidentList, name="incident-accident-list"),
	path('incident-accident-detail/<str:pk>/', incidentAccidentDetail, name="incident-accident-detail"),
    path('incident-accident-create/', incidentAccidentCreate, name="incident-accident-create"),
    # API LOGIN AND AUTH
    url(r'^auth/login/$', obtain_auth_token, name='auth_user_login'),   
    url(r'^auth/logout/$', LogoutUserAPIView.as_view(), name='auth_user_logout'),
    url(r'^profile/$', ProfileAPIView.as_view(), name='user_profile')
]