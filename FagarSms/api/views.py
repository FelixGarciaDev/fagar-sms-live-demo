from django.contrib.auth import get_user_model
from django.http import JsonResponse

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view


from api.serializers import (CreateUserSerializer,
							RiskReportSerializer,
							RiskReportCreateSerializer,
							IncidentAccidentSerializer,
							IncidentAccidentCreateSerializer,
							)

from users.models import User, SmsManager, Company, Employee, RiskReport, IncidentAccident, Task

class LogoutUserAPIView(APIView):
    queryset = get_user_model().objects.all()

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class ProfileAPIView(APIView):
   #queryset = get_user_model().objects.all()

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        user = request.user
        print(user)
        return user

# API ENTRY POINT
@api_view(['GET'])
def apiOverview(request):
	api_urls = {
		'Risk Report List':'/report-list/',
		'Risk Report Detail View':'/rerpot-detail/<str:pk>/',		
        'Risk Report Create':'/report-create/',
		'IncidentAccident List':'/incident-accident-list/',
		'IncidentAccident Detail View':'/incident-accident-detail/<str:pk>/',		
        'IncidentAccident Create':'/incident-accident-create/',
		}

	return Response(api_urls)
# RISK REPORT ACTIONS
@api_view(['GET'])
def riskReportList(request):
	reports = RiskReport.objects.all().order_by('-id')
	serializer = RiskReportSerializer(reports, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def riskReportDetail(request, pk):
	report = RiskReport.objects.get(id=pk)
	serializer = RiskReportSerializer(report, many=False)
	return Response(serializer.data)

@api_view(['POST'])
def riskReportCreate(request):
	serializer = RiskReportCreateSerializer(data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)

# INCIDENT ACCIDENT ACTIONS

@api_view(['GET'])
def incidentAccidentList(request):
	incidentsAccidents = IncidentAccident.objects.all().order_by('-id')
	serializer = IncidentAccidentSerializer(incidentsAccidents, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def incidentAccidentDetail(request, pk):
	incidentAccident = IncidentAccident.objects.get(id=pk)
	serializer = IncidentAccidentSerializer(incidentAccident, many=False)
	return Response(serializer.data)

@api_view(['POST'])
def incidentAccidentCreate(request):
	serializer = IncidentAccidentCreateSerializer(data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)