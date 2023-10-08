from django.db import models
from django.contrib.auth.models import AbstractUser

from Falcon import falcon

import string
import random

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
