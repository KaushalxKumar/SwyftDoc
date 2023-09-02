from django.urls import path
from App.views import *

urlpatterns = [
    path('', index),
    path('upload_document', upload_document, name='upload_document')
]
