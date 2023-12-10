from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Entries(models.Model):
    name = models.TextField(max_length=20, blank=False, null=False)
    url = models.URLField(max_length=200, blank=True)
    username = models.TextField(max_length=40, blank=False, null=False)
    password = models.TextField(max_length=100, blank=False, null=False)
    From_User = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    encrypted = models.BooleanField(null=False, blank=False, default=False)
    created = models.DateTimeField(null=False, blank=False, default=timezone.now, editable=False)
    updated = models.DateTimeField(null=True, blank=True)
    otp = models.TextField(max_length=200, blank=True, null=True)
    otptype = models.CharField(max_length=4, 
                    choices=[
                            ('TOTP', 'TOTP'),
                            ('HOTP', 'HOTP'),
                            ], default='TOTP')
class Questions(models.Model):
    secquestions0 = models.CharField(
        max_length=2,
        choices=[
            ("Q0", "Place you want to visit."),
            ("Q1", "Name of your first pet."),
            ("Q2", "City were you born."),
            ("Q3", "Favorite Movie."),
            ("Q4", "Sport you practice or like the most."),
            ("Q5", "Name of your best childhood friend."),
            ("Q6", "Name of the first book you read."),
            ("Q7", "Food you prefer."),
            ("Q8", "Your mother's maiden name."),
            ("Q9", "Musical instrument you know how to play or would like to learn."),
        ],
        default="Q0",
    )

    secanwser0 = models.TextField(null=False)

    secquestions1 = models.CharField(
        max_length=2,
        choices=[
            ("Q0", "Place you want to visit."),
            ("Q1", "Name of your first pet."),
            ("Q2", "City were you born."),
            ("Q3", "Favorite Movie."),
            ("Q4", "Sport you practice or like the most."),
            ("Q5", "Name of your best childhood friend."),
            ("Q6", "Name of the first book you read."),
            ("Q7", "Food you prefer."),
            ("Q8", "Your mother's maiden name."),
            ("Q9", "Musical instrument you know how to play or would like to learn."),
        ],
        default="Q0",
    )

    secanwser1 = models.TextField(null=False)

    secquestions2 = models.CharField(
        max_length=2,
        choices=[
            ("Q0", "Place you want to visit."),
            ("Q1", "Name of your first pet."),
            ("Q2", "City were you born."),
            ("Q3", "Favorite Movie."),
            ("Q4", "Sport you practice or like the most."),
            ("Q5", "Name of your best childhood friend."),
            ("Q6", "Name of the first book you read."),
            ("Q7", "Food you prefer."),
            ("Q8", "Your mother's maiden name."),
            ("Q9", "Musical instrument you know how to play or would like to learn."),
        ],
        default="Q0",
    )
    secanwser2 = models.TextField(null=False)

    From_User = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)

    encrypted = models.BooleanField(null=False, blank=False, default=False)

class Incorrectban(models.Model):
    cont = models.IntegerField(null=False, blank=False, default=0)