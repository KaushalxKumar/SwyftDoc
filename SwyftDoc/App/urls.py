from django.urls import path
from App.views import *

urlpatterns = [
    path('', index, name='index'),
    path('certify_document', certify_document, name='certify_document'),
    path('verify_document', verify_document, name='verify_document'),
    path('login', login_user, name='login'),
    path('register', register_user, name='register'),
    path('logout', logout_user, name='logout'),
]
