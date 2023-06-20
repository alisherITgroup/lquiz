from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('<str:username>/', profile, name='profile'),
    path('quiz/<str:url>/', quiz, name='quiz'),
    path('quiz/<str:url>/results/', results, name='results'),
    path('auth/login/', login_, name='login'),
]