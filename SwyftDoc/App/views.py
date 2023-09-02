from django.shortcuts import render
from django.http import HttpResponse

from PyPDF2 import PdfReader

import hashlib
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import hashes

# Create your views here.
def index(request):
    return render(request, 'index.html')

def upload_document(request):
    if request.method == 'GET':
        return render(request, 'upload_document.html')

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
        public_key = private_key.public_key()

        # Sign the hashed text with the private key
        signature = private_key.sign(hashed_text)

        other_hash = hashed_text  # Replace with the hash of the other document

        try:
            public_key.verify(signature, other_hash)
            verification_result = 'Signature verified: Hashes match.'
        except Exception as e:
            verification_result = 'Signature verification failed: Hashes do not match.'

        return HttpResponse(f'Signature: {signature.hex()}\nVerification Result: {verification_result}')

