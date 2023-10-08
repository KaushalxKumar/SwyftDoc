# Django
import traceback
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.urls import reverse
from urllib.parse import urljoin

from App.forms import CreateUserForm
from App.models import Person
from credentials import BASE_URL, FROM_EMAIL

# Cryptography & PyPDF2
from PyPDF2 import PdfReader
import hashlib

# DSA & Web3
from Falcon.falcon import *
from Interactions import certify, verify

# Create your views here.
"""
    Function to login user 
"""
def login_user(request):
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            context['message'] = "Invalid Credentials, Try Again"

    return render(request, 'login.html', context)


"""
    Function to register user 
"""
def register_user(request):
    context = {'form': CreateUserForm()}

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('index')

        else:
            context['message'] = "Invalid Credentials, Try Again"

    return render(request, 'register.html', context)


"""
    Function to logout user
"""
def logout_user(request):
    logout(request)
    return redirect('index')


"""
    Function to send verification email 
"""
@login_required(login_url='login')
def send_verify_email(request):
    user = request.user
    email = user.email
    token = user.token

    url = reverse('verify_email', kwargs={'token': token})
    email_url = urljoin(BASE_URL, url)

    send_mail(
        'SwyftDoc Email Verification',
        f'Click The Following Link to Verify Your Account: {email_url}',
        FROM_EMAIL,
        [email],
    )

    return render(request, 'profile.html')


"""
    Function to validate verification  
"""
@login_required(login_url='login')
def verify_email(request, token):
    # Check if the token is valid.
    if request.user.token == token:
        request.user.verified = True
        request.user.save()
        return render(request, 'email_verification.html', {'message': 'Successful'})

    return render(request, 'email_verification.html', {'message': 'Failed'})


"""
    Function to send reset password link  
"""
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = Person.objects.get(email=email)

        except Exception as e:
            return render(request, 'forgot_password.html', {'failed': 'Email Is Not Registered on SwyftDoc'})

        token = user.token
        url = reverse('reset_password', kwargs={'token': token})
        email_url = urljoin(BASE_URL, url)

        send_mail(
            'SwyftDoc Password Reset',
            f'Click The Following Link to Reset Your Password: {email_url}',
            FROM_EMAIL,
            [email],
        )

        return render(request, 'forgot_password.html', {'success': 'Password Reset Link Sent to Email'})

    return render(request, 'forgot_password.html')


"""
    Function to reset password
"""
def reset_password(request, token):
    if request.method == "POST":
        user = Person.objects.get(token=token)
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'password_reset.html', {'message': 'Passwords Do Not Match'})

        user.set_password(password1)
        user.save()
        return render(request, 'password_reset_success.html')

    return render(request, 'password_reset.html')


"""
    Function to display profile  
"""
@login_required(login_url='login')
def profile(request):
    return render(request, 'profile.html')


"""
    Function to display homepage  
"""
def index(request):
    return render(request, 'index.html')


"""
    Function to certify document
"""
@login_required(login_url='login')
def certify_document(request):
    if request.method == 'GET':
        return render(request, 'certify_document.html')

    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']

        # Check if the uploaded file is a PDF
        if not uploaded_file.name.endswith('.pdf'):
            return render(request, 'certify_document.html', {'file': 'Please Upload PDF Only'})

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

        # Retrieve users private key and public key
        user = request.user
        private_key = user.get_private_key()
        public_key = user.get_public_key()

        private_key_object = SecretKey.from_bytes(private_key)

        # Sign the hashed text with the private key
        signature = private_key_object.sign(hashed_text)

        # public_key_object = PublicKey.from_bytes(public_key)
        # return HttpResponse(public_key_object.verify(hashed_text, signature))

        # Store on the blockchain
        context = {'is_post': True}
        try:
            transaction_hash = certify.certify_document(signature, public_key, hashed_text)
            context['hash'] = transaction_hash
        except Exception as e:
            context['error'] = 'Document Previously Certified'
            traceback.print_exc()

        return render(request, 'certify_document.html', context)

    else:
        return render(request, 'certify_document.html', {'file': 'Please Select a PDF'})


"""
    Function to verify document
"""
@login_required(login_url='login')
def verify_document(request):
    if request.method == 'GET':
        return render(request, 'verify_document.html')

    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']

        # Check if the uploaded file is a PDF
        if not uploaded_file.name.endswith('.pdf'):
            return render(request, 'verify_document.html', {'file': 'Please Upload PDF Only'})

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
        try:
            owner, signature, public_key = verify.verify_document(hashed_text)

        except Exception as e:
            return render(request, 'verify_document.html', {'message': 'Document Not Certified'})

        public_key_object = PublicKey.from_bytes(public_key)
        result = public_key_object.verify(hashed_text, signature)

        if result:
            verification_result = 'Signature Verified | Hashes Match'
        else:
            verification_result = 'Signature Not Verified | Hashes Do Not Match'

        # Retrieve Certifier
        certifier = Person.objects.get(public_key=public_key)

        context = {
            'result': verification_result,
            'certifier': certifier,
            'verified': certifier.verified,
            'is_post': True
        }
        return render(request, 'verify_document.html', context)

    else:
        return render(request, 'verify_document.html', {'file': 'Please Select a PDF'})
