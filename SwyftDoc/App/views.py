# Django
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login

from App.forms import CreateUserForm

# Cryptography & PyPDF2
from PyPDF2 import PdfReader
import hashlib
from cryptography.hazmat.primitives.asymmetric import ed25519
from Interactions import certify, verify

# Create your views here.
def login_user(request):
    return render(request, 'login.html')

def register_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            print("Account Created")
            return redirect('index')
        else:
            # Form has errors
            print(form.errors)

    else:
        form = CreateUserForm()

    context = {'form': form}
    return render(request, 'register.html', context)

def index(request):
    return render(request, 'index.html')

def certify_document(request):
    if request.method == 'GET':
        return render(request, 'certify_document.html')

    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']

        # Check if the uploaded file is a PDF
        if not uploaded_file.name.endswith('.pdf'):
            return HttpResponse('Please upload a PDF file.')

        # Open the uploaded PDF file
        pdf = PdfReader(uploaded_file)

        # Initialize an empty string to store the extracted text
        text = ''

        # Iterate through each page of the PDF
        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]
            text += page.extract_text()

        # Hash the extracted text using SHA-256
        sha256_hash = hashlib.sha256()
        sha256_hash.update(text.encode('utf-8'))
        hashed_text = sha256_hash.digest()

        # Generate a private key and corresponding public key
        private_key = ed25519.Ed25519PrivateKey.generate()
        public_key = private_key.public_key().public_bytes_raw()

        # Sign the hashed text with the private key
        signature = private_key.sign(hashed_text)

        # Store on the blockchain
        certify.certify_document(signature, public_key, hashed_text)

        return HttpResponse('Document Certified')

def verify_document(request):
    if request.method == 'GET':
        return render(request, 'verify_document.html')

    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']

        # Check if the uploaded file is a PDF
        if not uploaded_file.name.endswith('.pdf'):
            return HttpResponse('Please upload a PDF file.')

        # Open the uploaded PDF file
        pdf = PdfReader(uploaded_file)

        # Initialize an empty string to store the extracted text
        text = ''

        # Iterate through each page of the PDF
        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]
            text += page.extract_text()

        # Hash the extracted text using SHA-256
        sha256_hash = hashlib.sha256()
        sha256_hash.update(text.encode('utf-8'))
        hashed_text = sha256_hash.digest()

        # Retrieve from blockchain
        owner, signature, public_key = verify.verify_document(hashed_text)

        public_key = ed25519.Ed25519PublicKey.from_public_bytes(public_key)

        try:
            public_key.verify(signature, hashed_text)
            verification_result = 'Signature verified: Hashes match.'
        except Exception as e:
            verification_result = 'Signature verification failed: Hashes do not match.'

        return HttpResponse(f'Signature: {signature.hex()}\nVerification Result: {verification_result}')
