from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('landing.urls')),
    path('',include('superuser.urls')),    
    path('',include('managers.urls')),
    path('',include('employees.urls')),
    #url(r'api/', include('api.urls')), 
]
