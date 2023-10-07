from django.db import models
from django.contrib.auth.models import AbstractUser

from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import UnsupportedAlgorithm

import string
import random

# def generate_key_pair():
#     # Generate a new Ed25519 key pair
#     private_key = ed25519.Ed25519PrivateKey.generate()
#     public_key = private_key.public_key()
#
#     # Serialize the keys to store in the database
#     private_key_bytes = private_key.private_bytes(
#         encoding=serialization.Encoding.PEM,
#         format=serialization.PrivateFormat.PKCS8,
#         encryption_algorithm=serialization.NoEncryption()
#     )
#     public_key_bytes = public_key.public_bytes(
#         encoding=serialization.Encoding.PEM,
#         format=serialization.PublicFormat.SubjectPublicKeyInfo
#     )
#
#     return private_key_bytes, public_key_bytes
#
# def generate_email_verification_token():
#     characters = string.ascii_lowercase + string.digits
#     token = ''.join(random.choice(characters) for _ in range(32))
#     return token
#
# class Person(AbstractUser):
#     verified = models.BooleanField(default=False)
#     public_key = models.BinaryField(null=True, blank=True)
#     private_key = models.BinaryField(null=True, blank=True)
#     token = models.CharField(max_length=50, blank=True)
#
#     def __str__(self):
#         return self.username
#
#     def save(self, *args, **kwargs):
#         if not self.public_key or not self.private_key:
#             private_key, public_key = generate_key_pair()
#             self.private_key = private_key
#             self.public_key = public_key
#
#         if not self.token:
#             token = generate_email_verification_token()
#             self.token = token
#
#         super().save(*args, **kwargs)
#
#     def get_private_key(self):
#         if self.private_key:
#             try:
#                 return serialization.load_pem_private_key(self.private_key, password=None)
#             except UnsupportedAlgorithm:
#                 return None
#         return None
#
#     def get_public_key(self):
#         if self.public_key:
#             try:
#                 return serialization.load_pem_public_key(self.public_key)
#             except UnsupportedAlgorithm:
#                 return None
#         return None


##################################################################################################################
############################## SPHINCS +
##############################

# from DSA.package.sphincs import Sphincs
#
# def generate_key_pair():
#     sphincs = Sphincs()
#     private_key, public_key = sphincs.generate_key_pair()
#
#     return private_key, public_key
#
# def generate_email_verification_token():
#     characters = string.ascii_lowercase + string.digits
#     token = ''.join(random.choice(characters) for _ in range(32))
#     return token
#
# class Person(AbstractUser):
#     verified = models.BooleanField(default=False)
#     public_key = models.BinaryField(null=True, blank=True)
#     private_key = models.BinaryField(null=True, blank=True)
#     token = models.CharField(max_length=50, blank=True)
#
#     def __str__(self):
#         return self.username
#
#     def save(self, *args, **kwargs):
#         if not self.public_key or not self.private_key:
#             private_key, public_key = generate_key_pair()
#             self.private_key = private_key
#             self.public_key = public_key
#
#         if not self.token:
#             token = generate_email_verification_token()
#             self.token = token
#
#         super().save(*args, **kwargs)
#
#     def get_private_key(self):
#         if self.private_key:
#             return self.private_key
#         return None
#
#     def get_public_key(self):
#         if self.public_key:
#             return self.public_key
#         return None


##################################################################################################################
##############################     FALCON
##############################

from Falcon import falcon
def generate_email_verification_token():
    characters = string.ascii_lowercase + string.digits
    token = ''.join(random.choice(characters) for _ in range(32))
    return token

def generate_key_pair():
    private_key = falcon.SecretKey(128)
    public_key = falcon.PublicKey(private_key)

    return private_key, public_key

class Person(AbstractUser):
    verified = models.BooleanField(default=False)
    public_key = models.BinaryField(null=True, blank=True)
    private_key = models.BinaryField(null=True, blank=True)
    token = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.public_key or not self.private_key:
            private_key, public_key = generate_key_pair()
            self.private_key = private_key.to_bytes()
            self.public_key = public_key.to_bytes()

        if not self.token:
            token = generate_email_verification_token()
            self.token = token

        super().save(*args, **kwargs)

    def get_private_key(self):
        if self.private_key:
            return self.private_key
        return None

    def get_public_key(self):
        if self.public_key:
            return self.public_key
        return None
