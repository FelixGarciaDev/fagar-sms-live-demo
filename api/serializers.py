from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import User, SmsManager, Company, Employee, RiskReport, IncidentAccident, Task

class CreateUserSerializer(serializers.ModelSerializer):
    email    = serializers.CharField()
    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password'})

    class Meta:
        model = get_user_model()
        fields = ('email', 'password')
        write_only_fields = ('password')
        read_only_fields = ('is_staff', 'is_superuser', 'is_active',)

    def create(self, validated_data):
        user = super(CreateUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class RiskReportSerializer(serializers.ModelSerializer):
	class Meta:
		model = RiskReport
		fields ='__all__'

# The create serializer includes all fields except the ones that are auto generated or will filled later
# eg: the creation date or probability

class RiskReportCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = RiskReport
		fields = ['owner',
                'of_company',
                'date',
                'place',
                'type_of_risk',
                'description',
                'recmendations',
                ]

class IncidentAccidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentAccident
        fields ='__all__'

class IncidentAccidentCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = RiskReport
		fields = ['owner',
                'of_company',
                'date',
                'place',                
                'description',                
                ]