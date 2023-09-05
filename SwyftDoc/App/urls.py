from django.urls import path
from App.views import *

urlpatterns = [
    path('', index),
    path('certify_document', certify_document, name='certify_document')
]
