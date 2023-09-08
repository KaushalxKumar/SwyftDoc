from django.db import models
from django.contrib.auth.models import AbstractUser

from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import UnsupportedAlgorithm


def generate_key_pair():
    # Generate a new Ed25519 key pair
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    # Serialize the keys to store in the database
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_key_bytes, public_key_bytes


class Person(AbstractUser):
    verified = models.BooleanField(default=False)
    public_key = models.BinaryField(null=True, blank=True)
    private_key = models.BinaryField(null=True, blank=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.public_key or not self.private_key:
            private_key, public_key = generate_key_pair()
            self.private_key = private_key
            self.public_key = public_key

        super().save(*args, **kwargs)

    def get_private_key(self):
        if self.private_key:
            try:
                return serialization.load_pem_private_key(self.private_key, password=None)
            except UnsupportedAlgorithm:
                return None
        return None

    def get_public_key(self):
        if self.public_key:
            try:
                return serialization.load_pem_public_key(self.public_key)
            except UnsupportedAlgorithm:
                return None
        return None
