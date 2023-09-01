from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from PyPDF2 import PdfReader

from cryptography.fernet import Fernet

# Create your views here.
def index(request):
    return render(request, 'index.html')

def upload_document(request):
    file = request.FILES['file']
    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    document = PdfReader(filename)
    text = document.read().decode('utf-8')

    print(text)
    # signature = Fernet.generate_key().encode('utf-8')
    # encrypted_text = Fernet(signature).encrypt(text.encode('utf-8'))
    # return HttpResponse(encrypted_text)
