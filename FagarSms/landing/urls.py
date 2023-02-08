from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include, reverse_lazy

from .views import (
    LandingView,
	LoginView,
    LogoutView,        
)

app_name = 'landing'

urlpatterns = [
    path('', LandingView.as_view(), name='landing'),
    path('login/', LoginView.as_view(), name='login'),       
    path('logout/', LogoutView.as_view(), name='logout'),   
]